from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FW = (ROOT / "firmware" / "AI_Guardian_TwinBridge_V1_10_2_Full.ino").read_text(encoding="utf-8")

def test_bmp280_101_uses_no_argument_init():
    assert "bmp.init(address)" not in FW
    assert "address == 0x77 && bmp.init()" in FW

def test_bmp280_pressure_path_still_reports_kind_and_address():
    assert "pressureKind = PRESS_BMP280;" in FW
    assert "pressureAddress = address;" in FW
