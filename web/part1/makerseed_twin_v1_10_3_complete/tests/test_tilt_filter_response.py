import math

TAU_MS = 90.0

def alpha(dt_ms):
    return 1.0 - math.exp(-dt_ms / TAU_MS)

def test_filter_has_responsive_20hz_step_response():
    a = alpha(50.0)
    # After 3 sensor frames / 150 ms, an exponential filter should have crossed 80%.
    response_150 = 1.0 - (1.0 - a) ** 3
    assert 0.80 < response_150 < 0.90

def test_filter_is_stable_and_bounded_for_normal_frame_intervals():
    for dt in (10, 20, 50, 100, 200, 250):
        a = alpha(dt)
        assert 0.0 < a < 1.0
