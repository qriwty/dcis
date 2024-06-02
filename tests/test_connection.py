import unittest
from unittest.mock import patch, MagicMock
from control.communication.communicator import DroneDataService


class TestDroneDataService(unittest.TestCase):

    @patch('control.communication.communicator.MAVLinkController')
    @patch('control.communication.communicator.DataAcquisitionThread')
    @patch('control.communication.communicator.StreamReceiver')
    @patch('control.communication.communicator.AttitudeProcessor')
    @patch('control.communication.communicator.GlobalPositionProcessor')
    @patch('control.communication.communicator.GimbalProcessor')
    def setUp(self, MockGimbalProcessor, MockGlobalPositionProcessor, MockAttitudeProcessor, MockStreamReceiver, MockDataAcquisitionThread, MockMAVLinkController):
        self.mock_mavlink = MockMAVLinkController.return_value
        self.mock_attitude_processor = MockAttitudeProcessor.return_value
        self.mock_global_position_processor = MockGlobalPositionProcessor.return_value
        self.mock_gimbal_processor = MockGimbalProcessor.return_value
        self.mock_data_acquisition_thread = MockDataAcquisitionThread.return_value
        self.mock_stream_receiver = MockStreamReceiver.return_value

        self.service = DroneDataService(
            mavlink_connection_str="udp:0.0.0.0:14550",
            host="192.168.0.107",
            port=5588
        )

    def test_get_mavlink_data(self):
        self.mock_attitude_processor.get_data.return_value = "attitude_data"
        self.mock_global_position_processor.get_data.return_value = "position_data"
        self.mock_gimbal_processor.get_data.return_value = "gimbal_data"

        mavlink_data = self.service.get_mavlink_data()

        self.assertEqual(mavlink_data["attitude"], "attitude_data")
        self.assertEqual(mavlink_data["position"], "position_data")
        self.assertEqual(mavlink_data["gimbal"], "gimbal_data")


if __name__ == '__main__':
    unittest.main()
