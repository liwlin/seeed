# [AI碉楼守护者](https://github.com/liwlin/seeed/tree/main/AI%E7%A2%89%E6%A5%BC%E5%AE%88%E6%8A%A4%E8%80%85 "AI碉楼守护者")

本仓库发布柴火课程的教学材料与配套Web工具，供教师和学员使用。

**Part1 当前正式发布：v0.01** · [GitHub Release](https://github.com/liwlin/seeed/releases/tag/v0.01) · [发布说明](RELEASE_NOTES_v0.01.md)

## 课程海报

<p align="center">
  <img src="AI碉楼守护者/课程海报/AI碉楼守护者_课程海报.png" alt="AI碉楼守护者课程全景海报" width="680">
</p>

[下载海报原图](AI碉楼守护者/课程海报/AI碉楼守护者_课程海报.png)。海报呈现三阶段课程全景；当前公开 Part1 教学材料与稳定工具，以及 Part2 Mission Center V0.4 网页预览；Part3 仍在开发中。

## Part 1 特色工具：数字孪生网页

![Part1数字孪生网页实际界面](AI碉楼守护者/课程海报/Part1_数字孪生网页截图.png)

通过网页点选硬件模块，查看板上位置、工作原理和当前状态。连接真板后，学员操作真实输入，观察网页变化；也能从网页控制实体LED、蜂鸣器和OLED，并借助加速度数据理解倾斜姿态。

截图由课程作者提供，画面处于`SIM · 未连接真机`状态。海报中的电脑画面是情境设计；上图展示课程实际网页，两者不作为实板验收结果。

[下载截图原图](AI碉楼守护者/课程海报/Part1_数字孪生网页截图.png) · [稳定版工具与启动说明](web/part1/makerseed_twin_v1_10_3_complete/README.md) · [网页源码](web/part1/makerseed_twin_v1_10_3_complete/standalone.html)

## Part 1：5 分钟开始

1. 准备一块 Grove Beginner Kit for Arduino；已烧录 V1.10.2 Twin Bridge 的板子可直接使用。
2. 新板烧录 `web/part1/makerseed_twin_v1_10_3_complete/firmware/AI_Guardian_TwinBridge_V1_10_2_Full.ino`。
3. 关闭 Arduino 串口监视器，双击 `start_server.bat`。
4. 使用桌面 Chrome / Edge 打开 `http://127.0.0.1:8080/standalone.html`。
5. 点击“连接真实开发板”，选择对应 COM 口，先验证一项真实输入，再验证一个实体输出。

没有开发板时仍可浏览 3D 模型和硬件工作原理；**真实输入、环境传感器和实体输出验收必须使用真板**。

## Part 2 特色工具：Mission Center V0.4

**任务引导 → 学员写 Prompt → 先评分、再按需润色 → CodeCraft 编程 → 真板验证 → V2 复测。**

![Part2 Mission Center 任务引导界面](AI碉楼守护者/Part2_建造AI碉楼守护者/网页截图/01_任务引导.png)

- **三章十关、七步引导**：故事、任务目标、作品预期和具体动作在主区展示，地图辅助查看进度；七个步骤可直接点击切换。
- **提示词学习**：可编辑草稿，配置 LLM API 后按六项标准评分，再按需润色；比较修改原因并手动采用。M10 由学员独立写出完整系统需求。
- **实时硬件图**：勾选哪些模块，就用 JavaScript + SVG 同时绘出哪些元件和连线。主板保持比例并居中，元件自动环绕排布；默认完整显示，可切换原尺寸、放大或下载 SVG。
- **接口说明**：区分数字 IO、模拟 ADC、I²C 与 DHT11 单线时序，按板卡版本切换 DHT11 / DHT20；明确 USB 上传调试与传感器接口的区别。

<details>
<summary>查看提示词学习界面</summary>

![Part2 可编辑提示词、评分与AI润色入口](AI碉楼守护者/Part2_建造AI碉楼守护者/网页截图/02_提示词学习.png)

先评价自己的表达，再决定是否借助 AI 润色。截图为未配置 API 的真实界面，没有展示虚构评分。

</details>

<details>
<summary>查看多元件实时接线界面</summary>

![Part2 主板居中、十模块同时显示的接线图](AI碉楼守护者/Part2_建造AI碉楼守护者/网页截图/03_实时接线图.png)

教师模式演示十个模块的图示选择。图片是板内连接的等效展开；完整 Grove 套件课堂只需接 USB。

</details>

[Part2 入口与课程结构](AI碉楼守护者/Part2_建造AI碉楼守护者/README.md) · [单文件网页](web/part2/Part2_AI_Guardian_MissionCenter_V0.4.html) · [使用说明](web/part2/README.md) · [接口与引脚参考](AI碉楼守护者/Part2_建造AI碉楼守护者/教学素材/硬件图/传感器接口与引脚说明.md)

下载仓库后，用桌面 Chrome / Edge 打开 `web/part2/Part2_AI_Guardian_MissionCenter_V0.4.html` 即可；图片与脚本已内嵌。GitHub 文件页用于查看或下载源码，不直接运行 HTML。

**Part2 网页不连接硬件、不编译、不烧录。** 真实程序与开发板由 CodeCraft 负责。LLM 评分与润色需要自行配置兼容接口；API Key 仅保留在本次页面会话。网页已做交互、布局和模拟 API 流程检查，真实模型调用、CodeCraft 烧录与课堂硬件验证仍需在实际环境完成。

## 三部分课程架构

### Part 1：数字孪生实验室（已经完成）

真实硬件 ⇄ Web 实时交互，认识全部硬件。3D 仿真板卡中，输入以真板操作为证据，输出由网页反控实物；LIS3DHTR 持续显示真实 XYZ，并可选择把**实体板的重力倾斜同步到整块 3D 板卡**。该功能只表示倾斜，不宣称 Yaw 航向跟踪。

### Part 2：CodeCraft AI 编程主线（网页预览版 V0.4 已公开）

Mission Center 是 **任务与提示词学习工作台**：以三章十关、七步引导组织碉楼守护任务，学员通过 CodeCraft AI 学习 OLED、LED、蜂鸣器、光线、声音、按键、旋钮、温湿度、气压和加速度等硬件编程。

网页支持 **可编辑 Prompt → 六项评分 → 自行改进或按需 AI 润色 → 对比并手动采用 → 真板验证与 V2 复测**。硬件面板根据勾选实时绘制全部模块及线路，主板居中、元件自适应排布，默认完整显示；M10 由学员自主设计系统需求。

Mission Center 不连接开发板，程序生成、编译和烧录由 CodeCraft 负责。[Part2 网页与使用说明](web/part2/README.md) · [任务与截图](AI碉楼守护者/Part2_建造AI碉楼守护者/README.md)

### Part 3：守护者训练场（开发中...）

Web实时交互重新回来。课程方预制Controller Lab、Game Engine和4个游戏场景；学员负责设计实体硬件控制器和游戏规则。

## 当前公开内容

目前公开 **Part1 教学材料与稳定 Web 工具**，以及 **Part2 Mission Center V0.4 网页预览、截图与接口参考**。Part2 完整讲义和 PPT 仍在完善，Part3 尚未发布。

### Part 1：数字孪生实验室

75分钟，碉楼故事20分钟、真实硬件与Web数字孪生探索55分钟。材料包含十模块探索任务、教师逐段讲义、学员任务册、18页图文课件和两页A4记录单。

- [Part 1课程入口](AI碉楼守护者/Part1_认识守护者/README.md)
- [教学PPTX](AI碉楼守护者/Part1_认识守护者/教学课件.pptx)
- [两页A4打印记录单](AI碉楼守护者/Part1_认识守护者/打印材料/课堂记录单_双面A4.pdf)
- [V1.10.3 Web工具说明](web/part1/makerseed_twin_v1_10_3_complete/README.md)，含网页、配套固件、启动脚本、自动测试与姿态算法验证。

Web工具请下载或克隆到本地，按随包说明运行 `start_server.bat`，再用桌面 Chrome / Edge 打开本地页面。GitHub文件预览用于阅读源码，不是课程交互网页的运行入口。网页与固件须使用兼容版本；课程截图不能代替真实板课堂验收。

V1.10.3 是当前稳定版工具。实际课堂需核对真实输入、实体输出和设备交接；三轴加速度计不能单独确定航向。

### Part 2：Mission Center V0.4 网页预览

- [网页项目与使用说明](web/part2/README.md)：任务导航、提示词评分与润色、进度保存和实时多模块接线图。
- [单文件 HTML](web/part2/Part2_AI_Guardian_MissionCenter_V0.4.html)：下载后用桌面 Chrome / Edge 打开，图片与脚本已内嵌。
- [Part2 课程结构与界面截图](AI碉楼守护者/Part2_建造AI碉楼守护者/README.md)：三章十关和七步学习流程。
- [传感器接口与引脚说明](AI碉楼守护者/Part2_建造AI碉楼守护者/教学素材/硬件图/传感器接口与引脚说明.md)：数字 IO、模拟 ADC、I²C 与新旧温湿度接口。

网页预览已公开；AI 评分需要自行配置接口，代码与实物效果仍由 CodeCraft 和真实开发板验证。

## 许可与来源

- 课程与教学材料：**CC BY 4.0**
- MakerSeed Web 与测试脚本：**MIT**
- Arduino Twin Bridge：**GPL-3.0-only**（当前依赖 GPLv3 的 Seeed Arduino SPA06）
- 课程来源与修改说明：[ATTRIBUTION.md](ATTRIBUTION.md)
- 完整许可：[LICENSE.md](LICENSE.md)
- 第三方软件、图片、商标来源：[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- v0.01 发布说明：[RELEASE_NOTES_v0.01.md](RELEASE_NOTES_v0.01.md)

## 仓库内容

- [AI 碉楼守护者课程](AI碉楼守护者/README.md)：公开 Part1 课程与 Part2 网页预览入口；Part3 保留目录占位。
- [web/part1/](web/part1/README.md)：Part1 数字孪生稳定项目、固件和启动脚本。
- [web/part2/](web/part2/README.md)：Part2 Mission Center 单文件网页与使用说明。

`web/` 按 `part1/`、`part2/` 分别管理两个网页项目。旧版本目录与 ZIP 不纳入当前发布。

Part2 完整讲义、PPT、制作数据等课程草稿继续保留本地；此次仅发布网页、使用入口、截图及接口参考。Part3、内部开发记录与参考资料继续排除。

