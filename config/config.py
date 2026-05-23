VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

STYLE_SHEET = """
QWidget {
    font-family: "Microsoft YaHei", "Segoe UI", "PingFang SC", sans-serif;
}

QMainWindow {
    background-color: #FFFFF0; 
}

QLabel {
    color: #333333; 
    font-size: 24px;
    font-weight: bold; 
}

QPushButton {
    background-color: #2d89ef;
    color: white; 
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-size: 20px;
    font-weight: bold;  
    min-height: 60px;
}

QPushButton:hover {
    background-color: #3ea0ff;
}

QPushButton:pressed {
    background-color: #1b5fbf;
}
"""