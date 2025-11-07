# C盘空间管理助手 (C Drive Space Manager)

C盘空间管理助手是一款面向 Windows 用户的磁盘空间管理工具原型，提供扫描、清理、迁移和优化等能力的图形界面。该项目使用 **Python 3.9+** 与 **Tkinter** 实现跨平台桌面界面，并整合 `psutil` 等库完成磁盘统计。

## 功能概览

- **磁盘扫描**：调用 `core.scanner.scan_drive` 快速计算目录占用比例。
- **安全清理**：在 `core.cleaner` 中定义常用的临时目录并支持模拟清理。
- **目录迁移**：通过 `core.mover.migrate_directory` 预估大目录迁移位置。
- **系统优化**：`core.optimizer` 列出常用命令并支持模拟执行。
- **智能推荐**：`core.analyzer.generate_insights` 根据阈值生成处理建议。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

默认所有破坏性操作都以 **dry-run** 模式运行，确保在未获得管理员权限和用户确认前不会修改系统。

## 项目结构

```
C_Cleaner/
├── core/             # 核心业务模块
├── ui/               # Tkinter 图形界面
├── assets/           # 图标与样式资源占位
├── configs/          # 配置文件
├── logs/             # 操作日志
└── main.py           # 程序入口
```

## 测试

项目内置了一组单元测试用于验证核心模块的行为，包括磁盘扫描、清理、迁移、优化与智能分析。可通过以下命令运行：

```bash
python -m unittest discover -s tests
```

## 注意事项

- 部分命令仅适用于 Windows 平台，非 Windows 环境下会自动进入模拟模式。
- 若需执行真实的清理、迁移或优化操作，请以管理员身份运行，并将 `dry_run=True` 调整为 `False`。
