# 统计图生成器

## 功能

以 CSV 为输入生成统计图的桌面界面与绘图逻辑。

## 技术栈

Python、Arcade、Tkinter、Pandas、NumPy、Matplotlib、Pillow。依赖版本以现有清单和上游兼容要求为准，早期代码可能需要历史版本。

## 目录

main.py 界面与绘图；files/ 合成示例数据。

## 启动

在本仓库目录执行；Python 示例需先激活自行创建的虚拟环境。

```sh
python3 -m venv .venv
# 激活虚拟环境后
python3 -m pip install arcade pandas numpy matplotlib pillow
python3 main.py
```

## 公开范围与许可

仅包含脱敏文本源码，不含原 Git 历史、私人绝对路径、凭据、用户数据库/聊天日志、未经逐张审阅的原始图片或二进制媒体。未发布资源不在许可证授权范围内。详见 [LICENSE](LICENSE) 与 [ATTRIBUTION.md](ATTRIBUTION.md)。

维护者有权授权的自有实现代码采用 MIT。第三方依赖、参考实现、团队内容、角色设定与未发布素材不由此重新许可；请同时遵守 ATTRIBUTION.md 所列来源边界。

## 替代资源

为减少缺图引用，提供新绘制的纯几何占位图片；原始图片均未复制。图片清单、生成方式与授权见 [ASSETS.md](ASSETS.md)。这不会恢复原游戏美术或保证历史图形 API 兼容。

## 验证与限制

原 CSV 已换成合成数据；原界面图片未包含，使用新绘制的占位图片。Tkinter 需要图形桌面。

本次执行静态语法/JSON 检查和独立密钥扫描；结果记录在 `VALIDATION.md`。静态通过不代表界面、依赖安装、硬件或端到端运行成功。缺失资源须使用自行创建或获得授权的替代品，不能从原个人素材库自动恢复。

用户选择的背景仅保存到被 Git 忽略的 `runtime/`，图表输出保存在被忽略的 `out/`；不要将含私人内容的输入文件提交到仓库
