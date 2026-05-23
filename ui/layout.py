from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt
from config import STYLE_SHEET

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Traffic Detect")
        MainWindow.resize(1300, 800)
        MainWindow.setStyleSheet(STYLE_SHEET)

        # 视频显示区
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background:black; color:white;")

        # 按钮
        self.btn_video = QPushButton("Open Video")
        self.btn_cam = QPushButton("Camera")
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")

        # 标签
        self.status_label = QLabel("no video")
        self.count_label = QLabel()

        # ================= 左侧下方的按钮组 =================
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.addWidget(self.btn_video, 0, 0)
        buttons_layout.addWidget(self.btn_cam, 0, 1)
        buttons_layout.addWidget(self.btn_start, 1, 0)
        buttons_layout.addWidget(self.btn_stop, 1, 1)

        self.btn_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_cam.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_stop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ================= 左右布局拼接 =================
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.video_label, stretch=8)
        left_layout.addLayout(buttons_layout, stretch=2)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.status_label)
        right_layout.addWidget(self.count_label)
        right_layout.addStretch()

        right_w = QWidget()
        right_w.setLayout(right_layout)
        right_w.setMaximumWidth(250)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=8)
        main_layout.addWidget(right_w, stretch=2)

        container = QWidget()
        container.setLayout(main_layout)
        MainWindow.setCentralWidget(container)