import math

# Coordinate mapping inferred from the physical-board tests in IMG_0237..IMG_0243:
# sensor X -> model Z, sensor Y -> model X, sensor Z -> model Y.
def map_sensor_to_model(ax, ay, az):
    return (ay, az, ax)


def norm(v):
    return math.sqrt(sum(x*x for x in v))


def normalize(v):
    n = norm(v)
    return tuple(x/n for x in v)


def quat_from_unit_vectors(a, b):
    # Mirrors THREE.Quaternion.setFromUnitVectors for normalized vectors.
    ax, ay, az = normalize(a)
    bx, by, bz = normalize(b)
    r = ax*bx + ay*by + az*bz + 1.0
    if r < 1e-8:
        if abs(ax) > abs(az):
            q = (-ay, ax, 0.0, 0.0)
        else:
            q = (0.0, -az, ay, 0.0)
    else:
        cx = ay*bz - az*by
        cy = az*bx - ax*bz
        cz = ax*by - ay*bx
        q = (cx, cy, cz, r)
    qn = math.sqrt(sum(x*x for x in q))
    return tuple(x/qn for x in q)


def rotate(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    # q * v * q^-1, expanded
    tx = 2*(y*vz - z*vy)
    ty = 2*(z*vx - x*vz)
    tz = 2*(x*vy - y*vx)
    return (
        vx + w*tx + (y*tz - z*ty),
        vy + w*ty + (z*tx - x*tz),
        vz + w*tz + (x*ty - y*tx),
    )


def angle_deg(a, b):
    a, b = normalize(a), normalize(b)
    d = max(-1.0, min(1.0, sum(x*y for x, y in zip(a, b))))
    return math.degrees(math.acos(d))


def test_canonical_axis_mapping():
    assert map_sensor_to_model(0, 0, 1) == (0, 1, 0)  # board front-up -> model front-up
    assert map_sensor_to_model(1, 0, 0) == (0, 0, 1)
    assert map_sensor_to_model(0, 1, 0) == (1, 0, 0)


def test_quaternion_aligns_measured_gravity_to_reference_up():
    samples = [
        (-0.91, -0.01, 0.21), # IMG_0237
        ( 0.00, -1.05, 0.10), # IMG_0238
        ( 0.19,  0.71, 0.72), # IMG_0239
        ( 0.29, -0.82, 0.60), # IMG_0241
        (-0.82, -0.06, 0.41), # IMG_0242
        ( 0.94, -0.07, 0.34), # IMG_0243
    ]
    ref = (0.0, 1.0, 0.0)
    for s in samples:
        mapped = normalize(map_sensor_to_model(*s))
        q = quat_from_unit_vectors(mapped, ref)
        aligned = rotate(q, mapped)
        assert angle_deg(aligned, ref) < 1e-5


def test_photo_samples_have_plausible_static_gravity_magnitude():
    samples = [
        (-0.91, -0.01, 0.21),
        ( 0.00, -1.05, 0.10),
        ( 0.19,  0.71, 0.72),
        ( 0.29, -0.82, 0.60),
        (-0.82, -0.06, 0.41),
        ( 0.94, -0.07, 0.34),
    ]
    for s in samples:
        g = norm(s)
        assert 0.85 <= g <= 1.15, (s, g)


def test_yaw_is_mathematically_underdetermined_from_gravity_only():
    # Once tilt quaternion aligns local gravity with world-up, any additional rotation
    # about world-up still aligns gravity. This proves yaw cannot be recovered from
    # accelerometer gravity alone.
    s = normalize(map_sensor_to_model(0.19, 0.71, 0.72))
    up = (0.0, 1.0, 0.0)
    q = quat_from_unit_vectors(s, up)
    aligned = rotate(q, s)
    assert angle_deg(aligned, up) < 1e-5

    half = math.radians(63)/2
    qyaw = (0.0, math.sin(half), 0.0, math.cos(half))
    # compose qyaw*q
    ax,ay,az,aw=qyaw; bx,by,bz,bw=q
    q2=(
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
        aw*bw - ax*bx - ay*by - az*bz,
    )
    aligned2=rotate(q2,s)
    assert angle_deg(aligned2, up) < 1e-5
