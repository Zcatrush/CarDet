# 🚗 Traffic Detect System (交通流量实时监控系统)

基于 YOLOv8 与 PyQt5 的交通检测与车辆跨线计数系统。

## ✨ 核心功能

* **支持本地视频与摄像头输入**：选择视频文件或开启实时摄像头流。
* **车辆识别与分类**：检测 Car、Motorcycle、Bus、Truck 四类车辆。
* **可视化线路交互**：鼠标左键拖拽绘制检测线，右键清除线段。
* **跨线计数逻辑**：同一辆车穿过同一条线时只计数一次，避免重复计数。
* **实时统计面板**：显示每类车辆数量、总数与过线计数。

---

## 📂 项目结构

```text
CarDet/
├── main.py             # 程序入口，启动 PyQt5 窗口
├── config/
│   └── config.py       # 车辆类别与 UI 样式配置
├── control/
│   └── control.py      # 应用控制器：UI 事件绑定、视频读取、画面刷新
├── core/
│   └── detector.py     # YOLOv8 目标检测、追踪与跨线判断
├── ui/
│   └── layout.py       # PyQt5 UI 布局定义
└── weight/
    └── yolov8n.pt      # YOLOv8 模型权重文件
```

## 🧠 模块说明

* `main.py`
  - 程序入口。
  - 创建 `QApplication` 并显示 `TrafficApp` 窗口。

* `control/control.py`
  - 构建主窗口逻辑。
  - 处理视频源、开始/停止、鼠标绘制线段、UI 更新与显示。

* `core/detector.py`
  - 使用 `ultralytics.YOLO` 进行目标检测与 `track()` 追踪。
  - 根据检测框中心点与画线位置计算车辆是否穿过检测线。
  - 维护每辆车与每条线的状态，避免重复计数。

* `ui/layout.py`
  - 定义视频显示区、按钮布局与统计面板。
  - 应用统一的 CSS 样式表。

* `config/config.py`
  - 定义车辆类别映射 `VEHICLE_CLASSES`。
  - 提供 UI 样式 `STYLE_SHEET`。

## 🚀 运行指南

### 1. 安装依赖

请在项目根目录下创建并激活 Python 虚拟环境，然后安装依赖：

```bash
py -3.10 -m venv venv310
venv310\Scripts\activate
python -m pip install --upgrade pip
pip install ultralytics opencv-python PyQt5 lap
```

### 2. 启动程序

```bash
python main.py
```

### 3. 使用说明

1. 点击 `Open Video` 选择本地视频文件，或点击 `Camera` 打开电脑摄像头。
2. 点击 `Start` 开启检测，点击 `Stop` 停止。
3. 在视频区按住鼠标左键拖动来绘制检测线。
4. 右键点击视频区可删除最近的一条检测线。
5. 右侧面板显示当前各车种数量、总数和跨线计数。

## ⚠️ 注意事项

* 请确保 `weight/yolov8n.pt` 模型文件存在。
* 如果出现摄像头无法打开，请检查系统权限和设备状态。
* 若要使用自定义模型，可替换 `weight/yolov8n.pt` 并修改 `VehicleTracker` 初始化路径。

---

## 📌 特色亮点

* 简洁模块化架构：UI、控制逻辑、检测算法分离。
* 基于 YOLOv8 与 ByteTrack 的实时追踪与过线计数。
* 支持交互式检测线绘制与动态统计显示。
