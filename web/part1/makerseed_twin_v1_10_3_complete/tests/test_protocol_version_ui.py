from pathlib import Path
HTML=(Path(__file__).resolve().parents[1]/'standalone.html').read_text(encoding='utf-8')

def test_protocol_version_comes_from_hello_frame():
    assert 'protocolVersion:0' in HTML
    assert 'serialLink.protocolVersion=Number(frame.version)||0' in HTML
    assert "MakerSeed Twin Text v${serialLink.protocolVersion||'?'}" in HTML
    assert "'MakerSeed Twin Text v3'" not in HTML
