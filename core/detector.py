import cv2
from ultralytics import YOLO
from config import VEHICLE_CLASSES

class VehicleTracker:
    def __init__(self, model_path="weight/yolov8n.pt"):
        self.model = YOLO(model_path)
        self.vehicle_count = 0
        self.track_history = {}
        self.tracked_ids = set()

    def reset(self):
        """清空所有追踪记录和计数"""
        self.vehicle_count = 0
        self.track_history = {}
        self.tracked_ids = set()

    def get_side(self, px, py, x1, y1, x2, y2):
        """数学方法：判断点在直线的哪一侧"""
        return (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)

    def process_frame(self, frame, lines, line_pts):
        """
        处理每一帧：执行 YOLO 推理，绘制框，判断过线
        """
        frame_stats = {"car": 0, "motorcycle": 0, "bus": 0, "truck": 0, "total": 0}
        
        # YOLO 推理
        results = self.model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)
        frame_out = results[0].plot()

        # ================= 1. UI 绘制逻辑 (无论有无车辆都画线) =================
        for line in lines:
            if len(line) == 2:
                x1, y1 = line[0]
                x2, y2 = line[1]
                cv2.line(frame_out, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 画好的固定线(红)

        if len(line_pts) == 2:
            x1, y1 = line_pts[0]
            x2, y2 = line_pts[1]
            cv2.line(frame_out, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 正在拖拽的临时线(绿)

        # ================= 2. 车辆统计与多线过线判断 =================
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy
            ids = results[0].boxes.id
            clses = results[0].boxes.cls

            # 统计当前帧的车辆
            for cls in clses:
                cls = int(cls)
                if cls in VEHICLE_CLASSES:
                    name = VEHICLE_CLASSES[cls]
                    frame_stats[name] += 1
                    frame_stats["total"] += 1

            # 遍历所有画好的线，判断是否跨线
            for i, line in enumerate(lines):
                if len(line) == 2:
                    x1, y1 = line[0]
                    x2, y2 = line[1]

                    for box, tid in zip(boxes, ids):
                        tid = int(tid)
                        x1b, y1b, x2b, y2b = box.tolist()
                        cx = int((x1b + x2b) / 2)
                        cy = int((y1b + y2b) / 2)

                        curr = self.get_side(cx, cy, x1, y1, x2, y2)
                        
                        # 【核心修复】：将 车辆ID 和 线段ID 组合成唯一的主键
                        track_key = f"{tid}_line_{i}"
                        prev = self.track_history.get(track_key, None)

                        if prev is not None:
                            if prev * curr < 0: # 符号发生变化，说明穿过了线
                                # 同样，确保同一辆车穿过同一条线只计数一次
                                cross_key = f"{tid}_crossed_{i}"
                                if cross_key not in self.tracked_ids:
                                    self.vehicle_count += 1
                                    self.tracked_ids.add(cross_key)

                        self.track_history[track_key] = curr

        return frame_out, frame_stats, self.vehicle_count