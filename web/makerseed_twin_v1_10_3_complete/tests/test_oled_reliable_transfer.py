from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'standalone.html').read_text(encoding='utf-8')
FW = (ROOT / 'firmware' / 'AI_Guardian_TwinBridge_V1_10_2_Full.ino').read_text(encoding='utf-8')


def test_web_uses_begin_tile_end_ack_protocol():
    assert "OBEGIN\\n" in HTML
    assert "OEND\\n" in HTML
    assert 'pendingAck' in HTML
    assert 'waitForHardwareAck' in HTML or 'sendCommandWithAck' in HTML
    assert '`OT ${seq} ${row} ${tileX} ${hex}\\n`' in HTML


def test_web_does_not_use_fixed_sleep_as_oled_flow_control():
    start = HTML.index('async function sendOledBitmap')
    end = HTML.index('function bind', start)
    fn = HTML[start:end]
    assert 'sleep(8)' not in fn
    assert 'sleep(15)' not in fn
    assert '64/64' in fn
    assert '重试' in fn or 'retry' in fn.lower()


def test_firmware_supports_reliable_oled_session():
    assert 'oledTransferActive' in FW
    assert 'strcmp(line, "OBEGIN")' in FW
    assert 'strcmp(line, "OEND")' in FW
    assert 'sendAckWithSeq' in FW
    assert 'char* seqToken = strtok(args, " ")' in FW
    assert 'if (!oledTransferActive)' in FW


def test_firmware_ot_ack_contains_sequence_number():
    assert '\"seq\"' in FW
    assert 'sendAckWithSeq(F("OT"), seq' in FW
