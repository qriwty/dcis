import math
import unittest
from unittest.mock import patch, MagicMock
from control.core import DroneCoreService


class TestDroneCoreService(unittest.TestCase):

    @patch('control.core.DroneDataService')
    @patch('control.core.DroneAnalysisService')
    def setUp(self, MockDroneAnalysisService, MockDroneDataService):
        self.mock_data_service = MockDroneDataService.return_value
        self.mock_analysis_service = MockDroneAnalysisService.return_value

        self.core_service = DroneCoreService(
            mavlink_address="udp:0.0.0.0:14550",
            stream_host="192.168.0.107",
            stream_port=5588,
            model_path="control/analysis/yolov8n-visdrone.pt",
            dem_path="control/analysis/S36E149.hgt"
        )

    def test_start_and_stop_analysis(self):
        self.core_service.start_analysis()
        self.assertTrue(self.core_service.running)

        self.core_service.stop_analysis()
        self.assertFalse(self.core_service.running)

    def test_execute_command(self):
        command_dictionary = {
            "COMMAND": "ARM",
            "ARGUMENTS": {}
        }
        result = MagicMock()
        result.result = 0
        self.mock_data_service.mavlink_connection.drone.arming.return_value = result

        response = self.core_service.execute_command(command_dictionary)
        self.assertEqual(response, "SUCCESS")

    def test_get_drone_data(self):
        mock_drone_data = MagicMock()
        mock_drone_data.camera.frame = "mock_frame"
        mock_drone_data.camera.width = 640
        mock_drone_data.camera.height = 480
        mock_drone_data.camera.fov = 1.0
        self.mock_data_service.get_drone_data.return_value = mock_drone_data

        camera_frame, image_width, image_height, fov_horizontal, fov_vertical = self.core_service.get_drone_data()
        self.assertEqual(camera_frame, "mock_frame")
        self.assertEqual(image_width, 640)
        self.assertEqual(image_height, 480)
        self.assertEqual(fov_horizontal, 1.0)
        self.assertEqual(fov_vertical, 2 * math.atan(math.tan(1.0 / 2) * (480 / 640)))

    def test_get_mavlink_data(self):
        self.mock_data_service.get_mavlink_data.return_value = {
            "gimbal": "gimbal_data",
            "attitude": "attitude_data",
            "position": "position_data"
        }

        gimbal, attitude, global_position = self.core_service.get_mavlink_data()
        self.assertEqual(gimbal, "gimbal_data")
        self.assertEqual(attitude, "attitude_data")
        self.assertEqual(global_position, "position_data")

    # def tearDown(self):
    #     self.core_service.stop_analysis()
    #     self.core_service.analysis_thread.join()


if __name__ == '__main__':
    unittest.main()
