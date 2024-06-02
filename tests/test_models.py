import unittest
from models.user import User
from models.flight import Flight
from models.detection import Detection
from models.flight_snapshot import FlightSnapshot
from models.image import Image
from models.object import Object
from models.point import Point
from models.setting import Setting
from models.task import Task
from datetime import datetime


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user = User(name='testuser', email='test@example.com')
        self.user.set_password('FlaskIsAwesome')

    def test_user_creation(self):
        self.assertEqual(self.user.name, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_password_hashing(self):
        self.assertTrue(self.user.check_password('FlaskIsAwesome'))
        self.assertFalse(self.user.check_password('wrongpassword'))


class TestFlightModel(unittest.TestCase):

    def setUp(self):
        self.flight = Flight(user_id=1, start_time=datetime.utcnow())

    def test_flight_creation(self):
        self.assertEqual(self.flight.user_id, 1)
        self.assertIsNotNone(self.flight.start_time)

    def test_flight_relationship(self):
        user = User(name='testuser', email='test@example.com')
        user.set_password('FlaskIsAwesome')
        self.flight.user = user
        self.assertEqual(self.flight.user.name, 'testuser')
        self.assertEqual(self.flight.user.email, 'test@example.com')


class TestDetectionModel(unittest.TestCase):

    def setUp(self):
        self.detection = Detection(point_id=1, image_id=1, object_id=1, class_name='test_class', frame='frame_data')

    def test_detection_creation(self):
        self.assertEqual(self.detection.point_id, 1)
        self.assertEqual(self.detection.image_id, 1)
        self.assertEqual(self.detection.object_id, 1)
        self.assertEqual(self.detection.class_name, 'test_class')
        self.assertEqual(self.detection.frame, 'frame_data')


class TestFlightSnapshotModel(unittest.TestCase):

    def setUp(self):
        self.flight_snapshot = FlightSnapshot(timestamp=datetime.utcnow(), flight_id=1, point_id=1, roll=0.0, pitch=0.0, yaw=0.0, gimbal_roll=0.0, gimbal_pitch=0.0, gimbal_yaw=0.0)

    def test_flight_snapshot_creation(self):
        self.assertIsNotNone(self.flight_snapshot.timestamp)
        self.assertEqual(self.flight_snapshot.flight_id, 1)
        self.assertEqual(self.flight_snapshot.point_id, 1)
        self.assertEqual(self.flight_snapshot.roll, 0.0)
        self.assertEqual(self.flight_snapshot.pitch, 0.0)
        self.assertEqual(self.flight_snapshot.yaw, 0.0)
        self.assertEqual(self.flight_snapshot.gimbal_roll, 0.0)
        self.assertEqual(self.flight_snapshot.gimbal_pitch, 0.0)
        self.assertEqual(self.flight_snapshot.gimbal_yaw, 0.0)


class TestImageModel(unittest.TestCase):

    def setUp(self):
        self.image = Image(flight_snapshot_id=1, image=b'binarydata', width=640, height=480, fov_horizontal=90.0, fov_vertical=60.0)

    def test_image_creation(self):
        self.assertEqual(self.image.flight_snapshot_id, 1)
        self.assertEqual(self.image.image, b'binarydata')
        self.assertEqual(self.image.width, 640)
        self.assertEqual(self.image.height, 480)
        self.assertEqual(self.image.fov_horizontal, 90.0)
        self.assertEqual(self.image.fov_vertical, 60.0)


class TestObjectModel(unittest.TestCase):

    def setUp(self):
        self.object = Object(flight_id=1, track_id=123)

    def test_object_creation(self):
        self.assertEqual(self.object.flight_id, 1)
        self.assertEqual(self.object.track_id, 123)


class TestPointModel(unittest.TestCase):

    def setUp(self):
        self.point = Point(latitude=50.0, longitude=30.0, altitude=100.0)

    def test_point_creation(self):
        self.assertEqual(self.point.latitude, 50.0)
        self.assertEqual(self.point.longitude, 30.0)
        self.assertEqual(self.point.altitude, 100.0)


class TestSettingModel(unittest.TestCase):

    def setUp(self):
        self.setting = Setting(flight_id=1, parameter='param', value='value')

    def test_setting_creation(self):
        self.assertEqual(self.setting.flight_id, 1)
        self.assertEqual(self.setting.parameter, 'param')
        self.assertEqual(self.setting.value, 'value')


class TestTaskModel(unittest.TestCase):

    def setUp(self):
        self.task = Task(flight_id=1, command='command', created=datetime.utcnow(), status=0)

    def test_task_creation(self):
        self.assertEqual(self.task.flight_id, 1)
        self.assertEqual(self.task.command, 'command')
        self.assertIsNotNone(self.task.created)
        self.assertEqual(self.task.status, 0)


if __name__ == '__main__':
    unittest.main()
