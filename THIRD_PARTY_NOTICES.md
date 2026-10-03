# Third-Party Notices / 第三方来源与许可

本文件记录当前公开版本中明确使用、依赖或引用的主要第三方内容。它不是对所有操作系统、浏览器、Arduino IDE 或工具链依赖的穷尽清单。

## 1. 柴火创客学园 M0 课程

- 项目：柴火创客学园 M0 · 零基础智能硬件入门
- 来源：https://github.com/mouseart2025/courses-M0
- 许可：CC BY 4.0
- 上游许可说明：https://github.com/mouseart2025/courses-M0/blob/main/LICENSE-README.md
- 上游法律文本：https://github.com/mouseart2025/courses-M0/blob/main/LICENSE.md
- 用途：本课程的教学法、课程骨架与部分上游课程内容来源。
- 修改：本项目已进行主题、结构、教学活动和数字孪生工具等改编；完整修改说明见 `ATTRIBUTION.md`。

上游明确要求署名、许可链接并说明是否修改；其许可不授予商标权，也不意味着对改编版的官方背书。

## 2. Three.js

- 项目：https://github.com/mrdoob/three.js
- 许可：MIT
- Copyright © 2010-2026 three.js authors
- 用途：数字孪生网页的 WebGL / 3D 场景、向量与 Quaternion 计算。

Three.js MIT 许可要求保留版权声明和许可声明。

## 3. U8g2 / U8x8

- 项目：https://github.com/olikraus/u8g2
- 许可：U8g2lib 代码为 BSD-2-Clause
- Copyright (c) 2016, olikraus@gmail.com
- 用途：Arduino Bridge 驱动 128×64 OLED。

U8g2 仓库中的字体可能采用不同许可。当前固件通过 U8x8 使用库内字体；若未来把字体数据复制或直接嵌入本仓库，应单独核对对应字体许可。

## 4. Grove Temperature And Humidity Sensor

- 项目：https://github.com/Seeed-Studio/Grove_Temperature_And_Humidity_Sensor
- 许可：MIT
- Copyright (c) 2016 Seeed Studio
- 用途：DHT11 / DHT20 温湿度读取。

## 5. Seeed Arduino SPA06

- 项目：https://github.com/Seeed-Studio/Seeed_Arduino_SPA06
- 许可：GNU GPL v3
- 用途：SPA06-003 气压传感器读取。

由于当前 Twin Bridge 固件依赖该 GPLv3 库，本仓库将完整 Arduino Bridge 固件按 GPL-3.0-only 发布，而不是把它错误标记为 MIT。

## 6. Grove - Barometer Sensor BMP280

- 项目：https://github.com/Seeed-Studio/Grove_BMP280
- 许可：MIT
- Copyright (c) 2016 Seeed Technology Inc.
- 用途：兼容旧版 Grove Beginner Kit 的 BMP280 气压计。

## 7. Grove LIS3DHTR

- 项目：https://github.com/Seeed-Studio/Seeed_Arduino_LIS3DHTR
- 许可：MIT
- Copyright (c) 2019 Seeed Studio
- 用途：LIS3DHTR 三轴加速度读取。

## 8. Seeed Studio / Grove Beginner Kit 产品资料

课程中可能使用 Seeed Studio 官方 Grove Beginner Kit 产品照片或硬件布局图来帮助学员识别器件。

- 产品页：https://www.seeedstudio.com/Grove-Beginner-Kit-for-Arduino-p-4549.html
- 文档：https://wiki.seeedstudio.com/Grove-Beginner-Kit-For-Arduino/

这些第三方图片、商标和产品资料**不因本仓库的 CC BY 4.0 声明而被重新许可**。其版权、商标和使用条件仍由原权利人决定。下游若将这些图片脱离本项目重新发布，应自行确认相应授权条件。

## 9. Arduino 平台

Twin Bridge 面向 Arduino-compatible / Seeeduino Lotus 环境编译。Arduino IDE、Arduino AVR Core 和工具链属于外部依赖，本仓库不重新分发这些项目本身；请以 Arduino 官方仓库和发行包中的许可为准。

## 10. Part2 Mission Center 的图像与参考

Part2 单文件 HTML 内嵌了课程 V0.4 内容包中的场景图、地图和 MakerSeed 标识，以及 Seeed 官方新版实物照片与旧版硬件布局参考。软件代码许可不将这些第三方照片、产品标识或商标重新许可。

- 硬件照片与版本参考：[Grove Beginner Kit 官方资料](https://wiki.seeedstudio.com/Grove-Beginner-Kit-For-Arduino/)。
- 旧版布局图：[Seeed Parts.jpg](https://files.seeedstudio.com/wiki/Grove-Beginner-Kit-For-Arduino/img/Parts.jpg)，它是布局示意，不是实物照片。
- SVG 教学接线图为本项目绘制，参考 [Fritzing Breadboard View 的表达方式](https://fritzing.org/learning/tutorials/building-circuit)，没有嵌入 Fritzing 程序或零件库。
- README 中的 Part2 图片是该网页的真实界面截图；提示词示例、教师模式图示与课程插画不构成真实课堂或设备运行证据。

## 商标说明

Seeed、Grove、Arduino、Three.js、U8g2、柴火创客学园 / Chaihuo Maker Academy 等名称与标识属于各自权利人。引用仅用于说明兼容性、来源或依赖，不代表赞助、认可或官方合作关系。
