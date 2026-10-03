# License / 许可说明

本仓库是一个**多许可证（multi-license）**项目。不同类型的内容采用不同许可，第三方材料继续受其原始许可或权利约束。

## 1. 课程与教学内容 — CC BY 4.0

除第三方材料和另有说明的代码外，以下教学内容采用 **Creative Commons Attribution 4.0 International（CC BY 4.0）**：

- `AI碉楼守护者/` 下的教师讲义、学员任务册、课堂记录单、课程说明、原创教学图文；
- 仓库根目录及 Web 工具中的说明性文档、验证报告和发布说明。

完整法律文本见：`LICENSES/CC-BY-4.0.txt`  
官方链接：https://creativecommons.org/licenses/by/4.0/

### 来源与改编署名

本课程改编自《柴火创客学园 M0 · 零基础智能硬件入门》：

- 来源：https://github.com/mouseart2025/courses-M0
- 上游许可：CC BY 4.0
- 上游许可说明：https://github.com/mouseart2025/courses-M0/blob/main/LICENSE-README.md

本仓库在原课程基础上进行了主题、课程结构、数字孪生 Web 工具、真机 Bridge 协议、硬件探索流程和教学活动等修改。详细署名见 `ATTRIBUTION.md`。

## 2. Web 与测试代码 — MIT

以下由本项目新增的代码采用 **MIT License**，第三方嵌入代码除外：

- `web/makerseed_twin_v1_10_3_complete/standalone.html` 中 MakerSeed 自研部分；
- `web/makerseed_twin_v1_10_3_complete/tests/`；
- `web/Part2_AI_Guardian_MissionCenter_V0.4.html` 中项目原创的任务交互、提示词教练和 SVG 接线图代码；
- `start_server.bat`、`start_server.ps1`；
- 其他明确标注为 MIT 的项目代码。

完整文本见：`LICENSES/MIT.txt`。

> `standalone.html` 使用/包含 Three.js。Three.js 自身继续按其 MIT License 授权，见 `THIRD_PARTY_NOTICES.md`。

## 3. Arduino Twin Bridge 固件 — GPL-3.0-only

以下固件采用 **GNU General Public License v3.0 only（GPL-3.0-only）**：

- `web/makerseed_twin_v1_10_3_complete/AI_Guardian_TwinBridge_V1_10_2_Full.ino`
- `web/makerseed_twin_v1_10_3_complete/firmware/AI_Guardian_TwinBridge_V1_10_2_Full.ino`

原因：当前固件依赖 Seeed Studio 的 `Seeed_Arduino_SPA06`，其上游仓库采用 GPL-3.0。为避免对下游造成错误的“全部 MIT”预期，本仓库将当前完整 Bridge 固件按 GPL-3.0-only 发布。

完整 GPL v3 文本见：`LICENSES/GPL-3.0-only.txt`。

## 4. 第三方材料与商标

本仓库不对第三方材料授予超出其原始许可或授权范围的权利。尤其包括：

- Seeed Studio / Grove Beginner Kit 的产品照片、硬件图和产品名称；
- 柴火创客学园 / Chaihuo Maker Academy 的名称与上游课程材料；
- Three.js、U8g2、Seeed Arduino libraries 等第三方软件；
- 各权利人的商标、Logo 和品牌标识。

详细来源、许可证和链接见 `THIRD_PARTY_NOTICES.md`。

“柴火创客学园”“Seeed”“Grove”“Arduino”“Three.js”“U8g2”等名称和标识属于其各自权利人。本仓库的署名或引用不表示这些权利人对本项目的赞助、认可或官方背书。

## 5. 许可证冲突时

如某个文件顶部、其所在第三方目录、原始素材说明或 `THIRD_PARTY_NOTICES.md` 中明确给出不同许可，以该文件适用的原始许可为准。本 `LICENSE.md` 不会重新许可本项目无权重新许可的第三方内容。
