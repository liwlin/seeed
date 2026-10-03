# AI 碉楼守护者 · 教学材料

当前公开 **Part 1：数字孪生实验室** 的教学材料与稳定工具，以及 **Part 2：Mission Center V0.4 网页预览版**。Part1 为75分钟：碉楼故事20分钟、真实硬件与Web数字孪生探索55分钟。

## 课程海报

<p align="center">
  <img src="课程海报/AI碉楼守护者_课程海报.png" alt="AI碉楼守护者课程全景海报" width="680">
</p>

[下载海报原图](课程海报/AI碉楼守护者_课程海报.png)。三阶段课程全景中，已公开 Part1 课程与 Part2 网页预览；Part3 仍在开发中。

## Part1 数字孪生网页

![作者提供的数字孪生网页截图](课程海报/Part1_数字孪生网页截图.png)

点选十个硬件模块，认识位置、原理与状态；连接真板后观察真实输入、反控实体输出，并理解加速度与倾斜的对应关系。

截图为`SIM · 未连接真机`界面，不作为实板验收结果。[稳定版启动说明](../web/makerseed_twin_v1_10_3_complete/README.md) · [下载截图原图](课程海报/Part1_数字孪生网页截图.png)

## Part2 Mission Center 网页预览

![Part2任务引导与七步导航](Part2_建造AI碉楼守护者/网页截图/01_任务引导.png)

以任务操作区为主线，提供三章十关、可直接切换的七步引导、可编辑 Prompt、先评分后按需润色，以及按勾选实时生成的多元件接线图。主板保持居中和固定比例，默认完整显示。

[Part2 入口与截图](Part2_建造AI碉楼守护者/README.md) · [单文件网页](../web/Part2_AI_Guardian_MissionCenter_V0.4.html) · [使用说明](../web/Part2_AI_Guardian_MissionCenter_V0.4_说明.md)

Mission Center 不连接开发板。学员通过 CodeCraft 生成、编译和烧录程序，再记录真板结果。AI评分评价提示词表达，不能代替硬件验证。

## 三部分课程架构

**Part 1：数字孪生实验室**——真实硬件 ⇄ Web 实时交互，认识全部硬件；3D 板卡用于空间定位，输入以真板操作为证据、输出反控实物；LIS3DHTR 显示真实 XYZ，并可选择将实体板的重力倾斜同步到整块 3D 板卡。

**Part 2：CodeCraft AI 编程主线**——Mission Center只提供碉楼故事、任务和要求，不连接硬件；学员通过CodeCraft AI完成OLED、LED、蜂鸣器、光线、声音、按键、旋钮、温湿度、气压、加速度等编程学习。

**Part 3：守护者训练场**——Web实时交互重新回来；课程方预制Controller Lab、Game Engine和4个游戏场景，学员负责设计实体硬件控制器和游戏规则。

## 发布范围

| 部分 | 状态 | 入口 |
|---|---|---|
| Part1：数字孪生实验室 | 已发布课程材料与Web工具 | [课程入口](Part1_认识守护者/README.md) |
| Part2：CodeCraft AI编程主线 | V0.4 网页预览、截图与接口参考已公开；完整课件仍在完善 | [网页入口](Part2_建造AI碉楼守护者/README.md) |
| Part3：守护者训练场 | 未完善，暂不发布，仅空目录占位 | [占位目录](Part3_守护者训练场/) |

Part2 仅公开此处列出的网页入口、截图和接口参考；完整讲义、PPT与制作数据仍保留本地。Part3 继续仅保留 `.gitkeep` 占位。

## Part1 备课材料

- [教师讲义](Part1_认识守护者/教师讲义.md)、[学员任务册](Part1_认识守护者/学员任务册.md)
- [18页教学课件](Part1_认识守护者/教学课件.pptx)
- [两页A4记录单](Part1_认识守护者/打印材料/课堂记录单_双面A4.pdf)
- [Web V1.10.3说明](../web/makerseed_twin_v1_10_3_complete/README.md)

正式授课前按教师讲义核对真板输入、实体输出与设备交接。网页截图和课程文档不能代替实板验收。

内部方案、开发记录与制作数据仅保留本地，不随课程材料发布。

## 来源与许可

本课程改编自《柴火创客学园 M0 · 零基础智能硬件入门》（https://github.com/mouseart2025/courses-M0，CC BY 4.0）。本版本由 MakerSeed / 种子创客工坊进行了主题、课程结构、教学活动与数字孪生工具等修改。完整署名见 [ATTRIBUTION.md](../ATTRIBUTION.md)，许可与第三方说明见 [LICENSE.md](../LICENSE.md) 与 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)。
