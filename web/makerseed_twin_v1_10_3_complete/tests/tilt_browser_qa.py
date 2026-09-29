import asyncio, json, math, os, shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'standalone.html').read_text(encoding='utf-8')
OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)

SAMPLES = [
    ('IMG_0237', -0.91, -0.01, 0.21),
    ('IMG_0238',  0.00, -1.05, 0.10),
    ('IMG_0239',  0.19,  0.71, 0.72),
    ('IMG_0241',  0.29, -0.82, 0.60),
    ('IMG_0242', -0.82, -0.06, 0.41),
    ('IMG_0243',  0.94, -0.07, 0.34),
]

async def main():
    async with async_playwright() as p:
        exe=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome') or shutil.which('chrome')
        launch_args=dict(headless=True,args=['--disable-gpu-sandbox','--use-gl=swiftshader','--enable-webgl'])
        if exe: launch_args['executable_path']=exe
        browser = await p.chromium.launch(**launch_args)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.set_content(HTML, wait_until='load')
        await page.evaluate('window.__tiltKit=window.GuardianModel.build()')

        canonical = await page.evaluate('''() => {
          const k=window.__tiltKit;
          const a=k.mapAccelToModelVector(0,0,1,new THREE.Vector3());
          const b=k.mapAccelToModelVector(1,0,0,new THREE.Vector3());
          const c=k.mapAccelToModelVector(0,1,0,new THREE.Vector3());
          return {zUp:a.toArray(),xAxis:b.toArray(),yAxis:c.toArray()};
        }''')

        rows=[]
        for name,ax,ay,az in SAMPLES:
            r=await page.evaluate('''({name,ax,ay,az}) => {
              const k=window.__tiltKit;
              const s={ax,ay,az,accelSync:true,knob:512,button:false,led:false,oled:''};
              k.resetTiltReference(s);
              k.update(s);
              const d=k.getTiltDebug();
              const mapped=k.mapAccelToModelVector(ax,ay,az,new THREE.Vector3()).normalize();
              const aligned=mapped.clone().applyQuaternion(k.root.quaternion);
              const up=new THREE.Vector3(0,1,0);
              const angle=THREE.MathUtils.radToDeg(aligned.angleTo(up));
              return {name,ax,ay,az,norm:Math.hypot(ax,ay,az),mapped:mapped.toArray(),aligned:aligned.toArray(),residualDeg:angle,quality:d.tiltQuality,q:d.quaternion};
            }''', {'name':name,'ax':ax,'ay':ay,'az':az})
            rows.append(r)

        calibration = await page.evaluate('''() => {
          const k=window.__tiltKit;
          const ref={ax:0.19,ay:0.71,az:0.72,accelSync:true,knob:512,button:false,led:false,oled:''};
          const next={ax:-0.82,ay:-0.06,az:0.41,accelSync:true,knob:512,button:false,led:false,oled:''};
          k.calibrateTiltReference(ref);
          const q0=k.root.quaternion.toArray();
          k.resetTiltFilter(next);
          k.update(next);
          const d=k.getTiltDebug();
          const cur=k.mapAccelToModelVector(next.ax,next.ay,next.az,new THREE.Vector3()).normalize();
          const refv=k.mapAccelToModelVector(ref.ax,ref.ay,ref.az,new THREE.Vector3()).normalize();
          const aligned=cur.clone().applyQuaternion(k.root.quaternion);
          return {qAtCalibration:q0,qAfterMove:k.root.quaternion.toArray(),residualToReferenceDeg:THREE.MathUtils.radToDeg(aligned.angleTo(refv)),debug:d};
        }''')

        sync_off = await page.evaluate('''() => {
          const k=window.__tiltKit;
          const s={ax:-0.91,ay:-0.01,az:0.21,accelSync:false,knob:512,button:false,led:false,oled:''};
          k.update(s); return k.root.quaternion.toArray();
        }''')

        result={'canonical':canonical,'samples':rows,'calibration':calibration,'syncOffQuaternion':sync_off}
        (OUT/'tilt_browser_qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False,indent=2))

        assert canonical['zUp'] == [0,1,0]
        assert canonical['xAxis'] == [0,0,1]
        assert canonical['yAxis'] == [1,0,0]
        assert all(r['residualDeg'] < 1e-4 for r in rows)
        assert calibration['residualToReferenceDeg'] < 1e-4
        assert max(abs(x) for x in sync_off[:3]) < 1e-7 and abs(sync_off[3]-1) < 1e-7
        await browser.close()

asyncio.run(main())
