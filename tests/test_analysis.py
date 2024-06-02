import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from control.analysis.analysist import DroneAnalysisService


class TestDroneAnalysisService(unittest.TestCase):

    @patch('control.analysis.analysist.YOLO')
    @patch('control.analysis.analysist.ResNetConfiguration')
    @patch('control.analysis.analysist.Extractor')
    @patch('control.analysis.analysist.Tracker')
    @patch('control.analysis.analysist.GEOSpatial')
    def setUp(self, MockGEOSpatial, MockTracker, MockExtractor, MockResNetConfig, MockYOLO):
        self.mock_yolo = MockYOLO.return_value
        self.mock_geospatial = MockGEOSpatial.return_value
        self.mock_tracker = MockTracker.return_value

        self.service = DroneAnalysisService(
            model_path="control/analysis/yolov8n-visdrone.pt",
            dem_path="control/analysis/S36E149.hgt"
        )

    def test_predict(self):
        frame = np.zeros((480, 640, 3))
        detections = self.service.predict(frame)
        expected_detections = []
        self.assertEqual(detections, expected_detections)

    def test_update_tracker(self):
        frame = np.zeros((480, 640, 3))
        detections = [[100, 200, 300, 400, 0.9, 0]]
        mock_track = MagicMock()
        mock_track.to_tlbr.return_value = [100, 200, 300, 400]
        mock_track.track_id = 1
        mock_track.class_id = 0
        self.mock_tracker.tracks = [mock_track]

        tracks = self.service.update_tracker(frame, detections)
        self.assertEqual(tracks, [mock_track])

    def test_geospatial_analysis(self):
        mock_track = MagicMock()
        mock_track.to_tlbr.return_value = [100, 200, 300, 400]
        mock_track.track_id = 1
        tracks = [mock_track]

        image_width = 640
        image_height = 480
        fov_horizontal = 1.0
        fov_vertical = 1.0

        gimbal_data = MagicMock()
        gimbal_data.quaternion.to_euler.return_value = (0.0, 0.0, 0.0)

        attitude_data = MagicMock()
        attitude_data.roll = 0.0
        attitude_data.pitch = 0.0
        attitude_data.yaw = 0.0

        global_position_data = MagicMock()
        global_position_data.heading = 0.0
        global_position_data.latitude = 0.0
        global_position_data.longitude = 0.0
        global_position_data.altitude = 0.0

        self.mock_geospatial.detection_angles.return_value = (0.0, 0.0)
        self.mock_geospatial.calculate_direction_vector.return_value = (0.0, 0.0, 0.0)
        self.mock_geospatial.find_target_location.return_value = (0.0, 0.0, 0.0)

        tracks_locations = self.service.geospatial_analysis(
            tracks, image_width, image_height, fov_horizontal, fov_vertical,
            gimbal_data, attitude_data, global_position_data
        )

        expected_locations = {1: (0.0, 0.0, 0.0)}
        self.assertEqual(tracks_locations, expected_locations)


if __name__ == '__main__':
    unittest.main()
