import torch
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


from ui import Ui_MainWindow
from core import VehicleTracker

class TrafficApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 初始化 UI 界面

        # 初始化 YOLO 逻辑引擎
        self.tracker = VehicleTracker("weight/yolov8n.pt")

        # 视频及定时器设置
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # 画线交互状态
        self.line_pts = []
        self.drawing = False
        self.scale_w = 1.0
        self.scale_h = 1.0

        # 初始化显示文字
        self.update_stats_label({"car": 0, "motorcycle": 0, "bus": 0, "truck": 0, "total": 0}, 0)

        # 绑定按钮事件
        self.btn_video.clicked.connect(self.open_video)
        self.btn_cam.clicked.connect(self.open_cam)
        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)

        # 绑定鼠标事件 (覆盖 QLabel 原有的鼠标方法)
        self.video_label.setMouseTracking(True)
        self.video_label.mousePressEvent = self.mouse_press
        self.video_label.mouseMoveEvent = self.mouse_move
        self.video_label.mouseReleaseEvent = self.mouse_release


    # ================= 业务控制逻辑 =================
    def open_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Video")
        if path:
            self.cap = cv2.VideoCapture(path)
            self.status_label.setText("Video loaded")

    def open_cam(self):
        self.cap = cv2.VideoCapture(0)
        self.status_label.setText("Camera opened")

    def start(self):
        if self.cap:
            self.timer.start(30)
            self.status_label.setText("Running")

    def stop(self):
        self.timer.stop()
        self.status_label.setText("Stopped")

    def update_stats_label(self, stats_dict, crossed_count):
        """统一负责更新界面的文字"""
        stats_text = (
            f"Car: {stats_dict['car']}\n"
            f"Motor: {stats_dict['motorcycle']}\n"
            f"Bus: {stats_dict['bus']}\n"
            f"Truck: {stats_dict['truck']}\n"
            f"Total: {stats_dict['total']}\n"
            f"Crossed: {crossed_count}\n"
        )
        self.count_label.setText(stats_text)


    # ================= 视频刷新处理 =================
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # 更新图片的缩放比例（用于画线交互）
        h, w = frame.shape[:2]
        self.scale_w = w / self.video_label.width()
        self.scale_h = h / self.video_label.height()

        # 【核心】：将图片交给独立的 detector 去处理
        frame_out, frame_stats, crossed = self.tracker.process_frame(frame, self.line_pts)

        # 更新UI界面文字
        self.update_stats_label(frame_stats, crossed)
        
        # 显示图片
        self.display(frame_out)

    def display(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        qimg = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)
        pix = pix.scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video_label.setPixmap(pix)


    # ================= 鼠标画线交互 =================
    def map_point(self, event):
        x = int(event.pos().x() * self.scale_w)
        y = int(event.pos().y() * self.scale_h)
        return x, y

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            x, y = self.map_point(event)
            self.drawing = True
            self.line_pts = [(x, y)]
        elif event.button() == Qt.RightButton:
            self.line_pts = []
            self.drawing = False
            self.status_label.setText("Line cleared")

    def mouse_move(self, event):
        if self.drawing:
            x, y = self.map_point(event)
            if len(self.line_pts) == 1:
                self.line_pts.append((x, y))
            else:
                self.line_pts[1] = (x, y)

    def mouse_release(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            x, y = self.map_point(event)
            if len(self.line_pts) == 1:
                self.line_pts.append((x, y))
            self.drawing = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TrafficApp()
    win.show()
    sys.exit(app.exec_())