# V1.10.3 Final QA Summary

Date: 2026-09-29

## Automated regression

- `python -m pytest tests -q` → **25 passed**
- Three JavaScript blocks extracted from `standalone.html` → `node --check` **3/3 passed**
- `tests/tilt_browser_qa.py` → actual Three.js `Vector3` / `Quaternion` model math verified.
- `tests/browser_qa.py` → DOM / Web Serial mock / pressure freshness / OLED reliable transfer verified.

## Tilt algorithm acceptance

Coordinate mapping:

```text
Sensor X → Model Z
Sensor Y → Model X
Sensor Z → Model Y
```

All six physical test samples (`IMG_0237`, `0238`, `0239`, `0241`, `0242`, `0243`) produce **0° numerical residual** after Quaternion gravity alignment in the Three.js math replay.

Observed norms: **0.919–1.057 g**, all inside the static/slow-motion trust range.

Current-pose calibration produces an identity Quaternion at capture; disabling sync returns the model to identity tilt.

## Preserved V1.10.2 regression

- OLED: `OBEGIN → 64 tile ACK/retry → OEND`
- Forced loss of tile #17 ACK caused exactly one retry; **64/64 unique tiles arrived**.
- Temperature and pressure live views contain **0 simulation sliders**.
- Selection highlight uses the local component frame; the old application-level world-AABB selection implementation is not used.

## Automation limitation

The container Chromium cannot create a WebGL rendering context. Browser protocol/DOM tests still pass, and the exact Three.js vector/quaternion math is exercised without a renderer. Final visual orientation therefore remains a physical Chrome + real-board acceptance check.

## Scope boundary

LIS3DHTR is a three-axis accelerometer. V1.10.3 synchronizes gravity-derived tilt (pitch/roll/front-back orientation) and intentionally does **not** claim yaw/heading observability.
