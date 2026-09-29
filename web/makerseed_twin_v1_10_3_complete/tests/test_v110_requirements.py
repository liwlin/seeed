from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'standalone.html').read_text(encoding='utf-8')
FW = (ROOT / 'firmware' / 'AI_Guardian_TwinBridge_V1_10_2_Full.ino').read_text(encoding='utf-8')


def test_accel_sync_switch_defaults_off():
    assert 'accelSync:false' in HTML
    assert 'id="accelSync"' in HTML
    assert 'state.accelSync' in HTML


def test_temperature_and_pressure_have_no_simulation_sliders():
    assert "slider('temp'" not in HTML
    assert "slider('hum'" not in HTML
    assert "slider('pressure'" not in HTML
    assert '等待真机温湿度数据' in HTML
    assert '等待真机气压数据' in HTML


def test_oled_uses_browser_bitmap_protocol_for_unicode():
    assert 'renderOledBitmap' in HTML
    assert 'sendOledBitmap' in HTML
    assert "`OT ${seq} ${row} ${tileX}" in HTML
    assert 'u8x8.drawTile' in FW
    assert 'strncmp(line, "OT ", 3)' in FW
    assert '中文' in HTML


def test_bridge_supports_old_and_new_environment_sensors():
    assert '#include "Seeed_BMP280.h"' in FW
    assert 'DHT dht11(DHT11_PIN, DHT11);' in FW
    assert 'TEMP_DHT20' in FW and 'TEMP_DHT11' in FW
    assert 'PRESS_SPA06' in FW and 'PRESS_BMP280' in FW
    assert 'tempKindText()' in FW
    assert 'pressureKindText()' in FW


def test_pressure_has_freshness_counter():
    assert 'pressureSeq' in FW
    assert 'tempSeq' in FW
    assert 'pressureSeq' in HTML
    assert 'tempSeq' in HTML
