# v0.01 Release Notes

**AI 碉楼守护者 · Part 1 首个公开预发布版本**

本 Release 面向教师、创客空间和希望复用课程的开发者，发布当前已完成并经真机迭代的 Part 1：数字孪生实验室。

## 包含内容

### 课程材料
- Part 1 教师讲义
- 学员任务册
- 18 页教学课件
- 双面 A4 课堂记录单
- 课程海报与实际网页截图

### 数字孪生工具
- MakerSeed Digital Twin Web **V1.10.3**
- Grove Beginner Kit 3D 模型与硬件说明
- Web Serial 真机连接
- 旋钮 / 光线 / 声音 / 按键实时输入
- 温湿度 / 气压真机读取
- LED / 蜂鸣器 / OLED 网页反控
- OLED 中文位图 + 64/64 ACK 可靠传输
- LIS3DHTR 重力向量 + Quaternion 倾斜同步
- 90 ms 低通、动态加速度保护与当前姿态校准

### Twin Bridge
- 配套 Bridge：**V1.10.2**
- V1.10.3 未改变 Bridge 协议，因此已烧录 V1.10.2 的开发板无需重刷

## 快速开始

1. 准备 Grove Beginner Kit for Arduino。
2. 新开发板烧录 `web/makerseed_twin_v1_10_3_complete/firmware/AI_Guardian_TwinBridge_V1_10_2_Full.ino`。
3. 关闭 Arduino 串口监视器。
4. 双击 `start_server.bat`。
5. 使用桌面 Chrome / Edge 打开 `http://127.0.0.1:8080/standalone.html`。
6. 点击“连接真实开发板”，选择对应 COM 口。

## 许可与来源

- 教学内容：CC BY 4.0
- MakerSeed Web / 测试代码：MIT
- Arduino Twin Bridge：GPL-3.0-only
- 上游课程来源与第三方许可：见 `ATTRIBUTION.md` 与 `THIRD_PARTY_NOTICES.md`

## 已知边界

- 当前公开发布仅包含 Part 1；Part 2 / Part 3 仍在开发。
- LIS3DHTR 只能由重力估算倾斜，不能单独提供 Yaw / 航向。
- 最终课堂使用仍需在真实电脑、真实开发板和实际 USB 环境中完成课前验收。
