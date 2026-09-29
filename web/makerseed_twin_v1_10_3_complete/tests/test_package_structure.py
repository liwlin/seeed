from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_complete_project_structure():
    expected = [
        'standalone.html', 'README.md', 'VERSION.txt', 'CHANGELOG.md', 'start_server.bat', 'start_server.ps1',
        'AI_Guardian_TwinBridge_V1_10_2_Full.ino',
        'firmware/AI_Guardian_TwinBridge_V1_10_2_Full.ino',
        'tests/test_v110_requirements.py', 'tests/browser_qa.py',
        'tests/test_tilt_sync_v1103.py', 'tests/test_tilt_algorithm_math.py',
        'tests/test_tilt_filter_response.py', 'tests/tilt_browser_qa.py',
        'evidence/tilt_algorithm_validation.md', 'evidence/tilt_algorithm_validation.json',
    ]
    missing = [p for p in expected if not (ROOT / p).exists()]
    assert not missing, f'missing files: {missing}'


def test_root_and_firmware_copy_match():
    a = (ROOT / 'AI_Guardian_TwinBridge_V1_10_2_Full.ino').read_bytes()
    b = (ROOT / 'firmware/AI_Guardian_TwinBridge_V1_10_2_Full.ino').read_bytes()
    assert a == b
