# Changelog

## V1.10.3 — 2026-09-29

### Tilt synchronization
- Fixed LIS3DHTR → Three.js coordinate mapping from the physical-board data set.
- Replaced the two-Euler-angle `atan2` implementation with gravity-vector Quaternion alignment.
- Added 90 ms exponential low-pass filtering.
- Added gravity-magnitude validity gate (`0.55–1.45 g`).
- Added current-tilt calibration and reset-to-default reference.
- Renamed the feature to “实体倾斜姿态同步” and documented the yaw limitation.
- Added numerical validation based on IMG_0237/0238/0239/0241/0242/0243.

### Preserved from V1.10.2
- Local oriented selection frames.
- Web Serial live mode.
- Real temperature/humidity and pressure paths.
- OLED Unicode rasterization + per-tile ACK/retry transfer.

### Firmware
- No Bridge protocol change. Existing V1.10.2 firmware remains compatible and does not need reflashing.
