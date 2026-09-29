from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'standalone.html').read_text(encoding='utf-8')


def test_legacy_euler_atan2_pose_is_removed():
    assert 'root.rotation.x=Math.atan2' not in HTML
    assert 'root.rotation.z=-Math.atan2' not in HTML


def test_accel_axis_mapping_and_quaternion_pose_exist():
    assert 'function mapAccelToModelVector' in HTML
    assert '.set(ay,az,ax)' in HTML.replace(' ', '')
    assert 'setFromUnitVectors' in HTML
    assert 'root.quaternion' in HTML


def test_pose_sync_is_truthfully_named_and_defaults_off():
    assert 'accelSync:false' in HTML
    assert '同步实体倾斜姿态到 3D 模型' in HTML
    assert '同步实体姿态到 3D 模型' not in HTML
    assert 'Yaw' in HTML or '航向' in HTML


def test_tilt_reference_calibration_controls_exist():
    assert 'id="accelCalibrate"' in HTML
    assert 'id="accelResetCalibration"' in HTML
    assert 'calibrateTiltReference' in HTML
    assert 'resetTiltReference' in HTML


def test_filter_and_quality_gate_exist():
    assert 'TILT_FILTER_TAU_MS=90' in HTML
    assert 'TILT_VALID_G_MIN=.55' in HTML and 'TILT_VALID_G_MAX=1.45' in HTML
    assert 'accelNorm' in HTML
    assert 'tiltQuality' in HTML
