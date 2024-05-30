import math
import threading
import random

import cv2

from .communication.communicator import DroneDataService
from .analysis.analysist import DroneAnalysisService
from datetime import datetime


class DroneCoreService:
    def __init__(self, mavlink_address, stream_host, stream_port, model_path, dem_path):
        self.data_service = DroneDataService(mavlink_address, stream_host, stream_port)
        self.analysis_service = DroneAnalysisService(
            model_path,
            dem_path
        )

        self.colors = [(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)) for j in range(1000)
        ]

        self.latest = None
        self.running = False

        self.analysis_thread = threading.Thread(target=self.run_analysis)
        self.analysis_thread.start()
        self.start_analysis()

    def start_analysis(self):
        self.running = True

    def stop_analysis(self):
        self.running = False

    def execute_command(self, command_dictionary):
        command = command_dictionary["COMMAND"]
        arguments = command_dictionary["ARGUMENTS"]
        if command == "ARM":
            pass

        elif command == "DISARM":
            pass

        elif command == "TAKEOFF":
            pass

        elif command == "LAND":
            pass

        elif command == "POINT_CAMERA":
            self.data_service.mavlink_connection.gimbal.set_angles(
                float(arguments["ROLL"]),
                float(arguments["PITCH"]),
                float(arguments["YAW"])
            )

        elif command == "SET_ROI":
            self.data_service.mavlink_connection.gimbal.set_roi_location(
                float(arguments["LATITUDE"]),
                float(arguments["LONGITUDE"]),
                float(arguments["ALTITUDE"])
            )

        elif command == "DISABLE_ROI":
            self.data_service.mavlink_connection.gimbal.disable_roi()

        elif command == "GO_TO":
            pass

        elif command == "CIRCLE_AROUND":
            pass

        elif command == "POINT_DRONE":
            pass

    def update_settings(self, detection_threshold, iou_threshold, max_detections, classes_excluded):
        self.analysis_service.detection_threshold = detection_threshold
        self.analysis_service.iou_threshold = iou_threshold
        self.analysis_service.max_detections = max_detections
        self.analysis_service.classes = [key for key in self.analysis_service.model.names.keys() if key not in classes_excluded]

    def get_drone_data(self):
        drone_data = self.data_service.get_drone_data()

        camera_frame = drone_data.camera.frame
        image_width = drone_data.camera.width
        image_height = drone_data.camera.height
        fov_horizontal = drone_data.camera.fov
        fov_vertical = 2 * math.atan(math.tan(fov_horizontal / 2) * (image_height / image_width))

        return camera_frame, image_width, image_height, fov_horizontal, fov_vertical

    def get_mavlink_data(self):
        mavlink_data = self.data_service.get_mavlink_data()

        gimbal = mavlink_data["gimbal"]
        attitude = mavlink_data["attitude"]
        global_position = mavlink_data["position"]

        return gimbal, attitude, global_position

    def paint_info(self, image, frame, track_id):
        color = self.colors[track_id % len(self.colors)]

        x1, y1, x2, y2 = frame
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        cv2.circle(
            image,
            (cx, cy),
            3,
            color,
            -1
        )

        cv2.putText(
            image,
            f"ID: {track_id}",
            (cx + 10, cy),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1
        )

        return image

    def run_analysis(self):
        self.running = True
        while self.running:
            camera_frame, image_width, image_height, fov_horizontal, fov_vertical = self.get_drone_data()
            gimbal_data, attitude_data, global_position_data = self.get_mavlink_data()

            gimbal_roll, gimbal_pitch, gimbal_yaw = gimbal_data.quaternion.to_euler()
            analysis_result = {
                "timestamp": datetime.now(),
                "drone": {
                    "location": {
                        "latitude": global_position_data.latitude,
                        "longitude": global_position_data.longitude,
                        "altitude": global_position_data.altitude
                    },
                    "attitude": {
                        "roll": attitude_data.roll,
                        "pitch": attitude_data.pitch,
                        "yaw": attitude_data.yaw
                    },
                    "camera": {
                        "frame": camera_frame,
                        "width": image_width,
                        "height": image_height,
                        "fov_horizontal": fov_horizontal,
                        "fov_vertical": fov_vertical
                    },
                    "gimbal": {
                        "roll": gimbal_roll,
                        "pitch": gimbal_pitch,
                        "yaw": gimbal_yaw
                    }
                },
                "analysis": {
                    "tracks": [],
                    "frame": None
                }
            }

            detections = self.analysis_service.predict(camera_frame)

            tracks = self.analysis_service.update_tracker(camera_frame, detections)

            tracks_locations = self.analysis_service.geospatial_analysis(
                tracks,
                image_width, image_height,
                fov_horizontal, fov_vertical,
                gimbal_data, attitude_data, global_position_data
            )

            for track in tracks:
                x1, y1, x2, y2 = map(int, track.to_tlbr())
                track_id = track.track_id
                class_id = track.class_id

                track_latitude, track_longitude, track_altitude = tracks_locations[track_id]

                track_results = {
                    "track_id": track_id,
                    "class_id": class_id,
                    "location": {
                        "latitude": track_latitude,
                        "longitude": track_longitude,
                        "altitude": track_altitude
                    },
                    "frame": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2
                    }
                }

                analysis_result["analysis"]["tracks"].append(track_results)

                self.paint_info(camera_frame, [x1, y1, x2, y2], track_id)

            analysis_result["analysis"]["frame"] = camera_frame

            self.latest = analysis_result

    def get_analysis(self):
        return self.latest
