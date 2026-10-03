import asyncio, json, os, shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'standalone.html').read_text(encoding='utf-8')
OUT=ROOT/'evidence'
OUT.mkdir(exist_ok=True)

async def main():
    async with async_playwright() as p:
        exe=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome') or shutil.which('chrome')
        launch_args=dict(headless=True,args=['--disable-gpu-sandbox','--use-gl=swiftshader','--enable-webgl'])
        if exe: launch_args['executable_path']=exe
        browser = await p.chromium.launch(**launch_args)
        page = await browser.new_page(viewport={"width":1600,"height":1000})
        errors=[]
        page.on('console', lambda msg: errors.append(f'{msg.type}: {msg.text}') if msg.type in ('error','warning') else None)
        await page.set_content(HTML, wait_until='load')
        await page.wait_for_timeout(1200)
        title=await page.title()
        ready=await page.evaluate('window.GuardianDebug && window.GuardianDebug.ready')
        await page.evaluate('window.__testKit=window.GuardianModel.build()')

        # Simulate new V1.10 bridge and real sensor stream.
        await page.evaluate('''() => {
          const d=window.GuardianDebug;
          d.serial.connected=true;
          window.__writes=[];
          window.__oledAttempts={};
          d.serial.writer={write:async data=>{
            const text=new TextDecoder().decode(data);
            window.__writes.push(text);
            for(const line of text.trim().split(String.fromCharCode(10))){
              if(!line)continue;
              if(line==='OBEGIN')setTimeout(()=>d.handleSerialFrame({type:'ack',cmd:'OBEGIN',value:1}),4);
              else if(line==='OEND')setTimeout(()=>d.handleSerialFrame({type:'ack',cmd:'OEND',value:1}),4);
              else if(line==='OLEDCLR')setTimeout(()=>d.handleSerialFrame({type:'ack',cmd:'OLEDCLR',value:1}),4);
              else if(line.startsWith('OT ')){
                const seq=Number(line.split(' ')[1]);
                window.__oledAttempts[seq]=(window.__oledAttempts[seq]||0)+1;
                // Deliberately drop the first ACK for tile #17 to prove retry behavior.
                if(seq===17&&window.__oledAttempts[seq]===1)continue;
                setTimeout(()=>d.handleSerialFrame({type:'ack',cmd:'OT',seq,value:1}),4);
              }
            }
          }};
          d.handleSerialFrame({type:'hello',protocol:'makerseed-twin',version:4,board:'Grove Beginner Kit / Seeeduino Lotus',capTemp:1,tempKind:'DHT11',capDht20:0,capPressure:1,pressureKind:'BMP280',pressureAddr:119,capAccel:1,capOled:1});
          d.handleSerialFrame({type:'state',knob:600,light:700,sound:120,soundRaw:500,button:0,led:0,buzzer:0,temp:27.3,hum:66.4,tempSeq:3,pressure:1006.72,pressureSeq:12,ax:0.42,ay:-0.18,az:0.89});
        }''')

        # Temperature has no simulation slider and is live.
        await page.evaluate("window.GuardianDebug.select('th')")
        await page.wait_for_timeout(80)
        th_ranges=await page.locator('#detail input[type=range]').count()
        th_text=await page.locator('#detail').inner_text()

        # Pressure has no simulation slider and exposes freshness counter.
        await page.evaluate("window.GuardianDebug.select('pressure')")
        await page.wait_for_timeout(80)
        p_ranges=await page.locator('#detail input[type=range]').count()
        p_text=await page.locator('#detail').inner_text()

        # Accel pose sync defaults off, then applies when switched on.
        await page.evaluate("window.GuardianDebug.select('accel')")
        await page.wait_for_timeout(80)
        checked=await page.locator('#accelSync').is_checked()
        accel_label=await page.locator('#detail').inner_text()
        calibrate_count=await page.locator('#accelCalibrate').count()
        reset_cal_count=await page.locator('#accelResetCalibration').count()
        rot_before=await page.evaluate('''() => { __testKit.update(GuardianDebug.state); return {x:__testKit.root.rotation.x,z:__testKit.root.rotation.z}; }''')
        await page.locator('#accelSync').check()
        await page.wait_for_timeout(80)
        rot_after=await page.evaluate('''() => { __testKit.update(GuardianDebug.state); return {x:__testKit.root.rotation.x,z:__testKit.root.rotation.z}; }''')

        # Unicode OLED path generates 64 safe tile commands + clear.
        await page.evaluate("window.GuardianDebug.select('oled')")
        await page.locator('#oledInput').fill('你好 MakerSeed\n数字孪生')
        await page.locator('#oledSend').click()
        await page.wait_for_function("document.querySelector('#oledTransferStatus') && document.querySelector('#oledTransferStatus').textContent.includes('64/64')", timeout=7000)
        writes=await page.evaluate('window.__writes')
        lines=''.join(writes).splitlines()
        ot=[x for x in lines if x.startswith('OT ')]
        seqs=[int(x.split()[1]) for x in ot]
        nonzero=any(set(x.split()[-1]) != {'0'} for x in ot)
        attempts=await page.evaluate('window.__oledAttempts')

        await page.screenshot(path=str(OUT/'v1103_oled_unicode.png'), full_page=False)

        result={
          'title':title,'webgl_ready':ready,'console_errors':errors,
          'temperature_range_count':th_ranges,'temperature_text_has_live':('DHT11' in th_text and '27.3' in th_text),
          'pressure_range_count':p_ranges,'pressure_text':p_text[:500],
          'accel_default_checked':checked,'accel_label_has_tilt':('倾斜姿态' in accel_label),'accel_calibrate_controls':(calibrate_count,reset_cal_count),'rotation_before':rot_before,'rotation_after':rot_after,
          'oled_total_lines':len(lines),'oled_tile_lines':len(ot),'oled_unique_tiles':len(set(seqs)),'oled_retry_seq17':attempts.get('17') or attempts.get(17),'oled_nonzero_bitmap':nonzero,
        }
        print(json.dumps(result,ensure_ascii=False,indent=2))
        assert title
        assert th_ranges == 0
        assert 'DHT11' in th_text and '27.3' in th_text
        assert p_ranges == 0
        assert 'BMP280' in p_text and '1006.72' in p_text and '更新 #12' in p_text
        assert checked is False
        assert '倾斜姿态' in accel_label
        assert calibrate_count == 1 and reset_cal_count == 1
        assert abs(rot_before['x']) < 1e-6 and abs(rot_before['z']) < 1e-6
        assert abs(rot_after['x']) > 0.01 or abs(rot_after['z']) > 0.01
        assert len(set(seqs)) == 64
        assert len(ot) == 65
        assert (attempts.get('17') or attempts.get(17)) == 2
        assert any(x == 'OBEGIN' for x in lines)
        assert any(x == 'OEND' for x in lines)
        assert nonzero
        await browser.close()

asyncio.run(main())
