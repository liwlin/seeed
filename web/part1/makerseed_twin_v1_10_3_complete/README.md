# AI 碉楼守护者 · Part 1 数字孪生 V1.10.3

这是 Grove Beginner Kit 第一部分的当前完整交付版。**V1.10.3 重点修正 LIS3DHTR 倾斜姿态同步算法**，并完整继承 V1.10.2 已通过真机测试的 OLED 可靠传输、Web Serial、选中框和环境传感器功能。

## V1.10.3 新增 / 修正

- 修正实物 LIS3DHTR 与 Three.js 模型的坐标轴映射：
  - `Sensor X → Model Z`
  - `Sensor Y → Model X`
  - `Sensor Z → Model Y（PCB 正面法线）`
- 删除旧版两个 `atan2` 欧拉角硬算方式，改为 **重力向量 + Quaternion**。
- “同步实体姿态”改名为更准确的 **“同步实体倾斜姿态”**。
- 姿态同步仍然**默认关闭**；XYZ 真机读数始终显示。
- 新增 90 ms 一阶指数低通，降低手持抖动；20 Hz 数据下约 150 ms 完成 >80% 阶跃响应。
- 新增加速度合量质量判断；`<0.55 g` 或 `>1.45 g` 时暂不把该帧用于姿态，避免快速运动把线性加速度误当重力。
- 新增 **“当前姿态设为 0° 倾斜基准”** 与 **“恢复默认基准”**。
- 页面明确说明物理边界：三轴加速度计不能单独确定绕重力轴的 **Yaw / 航向**。
- 加入基于用户 `IMG_0237`～`IMG_0243` 实测数据的算法验证与浏览器数值回放。

## 继承自 V1.10.2 的稳定功能

- 3D 元器件本地坐标选中框，不再出现世界坐标包围框“歪着套住”的问题；
- 真机 Web Serial 连接 / 断线状态；
- 旋钮、光线、声音、按键真机输入；
- LED、蜂鸣器网页反控；
- 温湿度、气压只显示真机数据，无仿真滑动条；
- 自动兼容 DHT20 / DHT11 与 SPA06-003 / BMP280；
- OLED 中文 / 英文浏览器栅格化；
- OLED `OBEGIN → 64×OT逐块ACK → OEND` 可靠传输、超时重发和 64/64 完整确认。

## 固件说明

**V1.10.3 没有改动串口或 Arduino Bridge 协议。** 因此如果你的板子已经烧录并验证通过：

```text
AI_Guardian_TwinBridge_V1_10_2_Full.ino
```

则**无需重新烧录**，只需替换 `standalone.html` 即可。

完整交付包仍附带这份稳定 Bridge，方便新电脑 / 新开发板重新烧录。

## 工程结构

```text
makerseed_twin_v1_10_3_complete/
├─ firmware/
│  └─ AI_Guardian_TwinBridge_V1_10_2_Full.ino   # 协议未变，沿用稳定版
├─ tests/
│  ├─ browser_qa.py
│  ├─ tilt_browser_qa.py
│  ├─ test_tilt_sync_v1103.py
│  ├─ test_tilt_algorithm_math.py
│  ├─ test_tilt_filter_response.py
│  ├─ test_oled_reliable_transfer.py
│  ├─ test_selection_local_frame.py
│  ├─ test_v110_requirements.py
│  ├─ test_bmp280_api_compat.py
│  ├─ test_protocol_version_ui.py
│  └─ test_package_structure.py
├─ evidence/
│  ├─ tilt_algorithm_validation.md
│  ├─ tilt_algorithm_validation.json
│  ├─ tilt_browser_qa.json
│  └─ browser_qa_v1103.json
├─ README.md
├─ standalone.html
├─ start_server.bat
├─ start_server.ps1
└─ AI_Guardian_TwinBridge_V1_10_2_Full.ino
```

## Arduino IDE 依赖

板型：**Arduino Uno**；串口：**115200 baud**。

1. `Grove Temperature And Humidity Sensor`（Seeed Studio；已兼容 2.0.2）
2. `Seeed Arduino SPA06`
3. `Grove - Barometer Sensor BMP280`（已兼容 1.0.1 的无参数 `bmp.init()`）
4. `Grove-3-Axis-Digital-Accelerometer-2g-to-16g-LIS3DHTR`
5. `U8g2`

## 运行顺序

1. 已使用 V1.10.2 Bridge 的开发板可直接保留；新板烧录 `firmware/AI_Guardian_TwinBridge_V1_10_2_Full.ino`。
2. 若用 Arduino 串口监视器检查数据，检查后必须关闭串口监视器。
3. 双击 `start_server.bat`。
4. Chrome / Edge 打开 `http://127.0.0.1:8080/standalone.html`。
5. 点击“连接真实开发板”，选择对应 COM 口。

## 倾斜姿态同步算法

### 1. 坐标映射

```text
modelGravity = normalize([sensorY, sensorZ, sensorX])
```

默认模型 PCB 位于 XZ 平面，`Model +Y` 是正面法线。板子正面水平朝上时 LIS3DHTR 约为 `(0,0,+1)`，映射后正好是 `(0,+1,0)`，因此模型保持默认平放。

### 2. Quaternion

```text
q = Quaternion.setFromUnitVectors(filteredGravity, referenceGravity)
```

不再分别计算两个 Euler 角，因此组合倾斜与正反面翻转更稳定。

### 3. 低通

```text
alpha = 1 - exp(-dt / 90 ms)
filtered = normalize(lerp(filtered, sample, alpha))
```

### 4. 当前姿态校准

点击“当前姿态设为 0° 倾斜基准”后：

```text
referenceGravity = 当前 filteredGravity
```

此时当前姿态在网页里成为 0° 倾斜。它用于补偿安装基准和教学演示，不会伪造航向。

### 5. Yaw 边界

LIS3DHTR 只有三轴加速度。当板子保持相同倾斜、只绕重力轴旋转时，XYZ 重力分量可以完全不变，因此网页无法从该传感器唯一判断航向角。V1.10.3 明确保留这个物理边界。

## 算法验证

`tests/test_tilt_algorithm_math.py` 与 `tests/tilt_browser_qa.py` 使用用户实测照片里的以下数据回放：

- `IMG_0237`: `(-0.91, -0.01, 0.21)`
- `IMG_0238`: `(0.00, -1.05, 0.10)`
- `IMG_0239`: `(0.19, 0.71, 0.72)`
- `IMG_0241`: `(0.29, -0.82, 0.60)`
- `IMG_0242`: `(-0.82, -0.06, 0.41)`
- `IMG_0243`: `(0.94, -0.07, 0.34)`

验证内容：坐标映射、Quaternion 对齐残差、校准零姿态、同步关闭时单位 Quaternion、Yaw 不可观测性、滤波响应。

完整结果见：`evidence/tilt_algorithm_validation.md`。

## OLED 可靠传输

保持 V1.10.2 机制不变：

```text
OBEGIN → ACK
OT #0 → ACK
...
OT #63 → ACK
OEND → ACK
```

单块超时最多重试 3 次；OLED 会话期间暂停状态上报和环境 I²C 采样，避免 AVR 串口缓冲与 I²C 总线拥塞。

## 许可与来源

- MakerSeed 自研 Web / 测试脚本：MIT
- Arduino Twin Bridge：GPL-3.0-only
- 课程内容与说明文档：CC BY 4.0
- 根许可：[../../../LICENSE.md](../../../LICENSE.md)
- 课程来源：[../../../ATTRIBUTION.md](../../../ATTRIBUTION.md)
- 第三方依赖：[../../../THIRD_PARTY_NOTICES.md](../../../THIRD_PARTY_NOTICES.md)

## 测试边界

- 自动测试可以验证数学算法、Web Serial 模拟协议、OLED 重试和网页 DOM 交互。
- 当前自动化容器无法创建 WebGL 上下文，因此最终视觉方向仍需在你当前 Chrome + 真板环境做最后一轮人工姿态核对。
- V1.10.3 不宣称完整 6DoF / 航向跟踪；未来若需真正 Yaw，应改用带陀螺仪的 6 轴 IMU 并做传感器融合。
