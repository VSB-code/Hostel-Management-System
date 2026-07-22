import unittest
from decimal import Decimal
from unittest.mock import Mock, patch

from app import create_app
from mysql.connector.errors import DatabaseError
from services.student_service import create_or_update_student


class HostelAppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_page_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_secret_key_is_configured(self):
        self.assertTrue(self.app.secret_key)

    @patch('services.student_service.get_db_connection')
    def test_create_or_update_student_uses_expected_schema(self, mock_get_db_connection):
        conn = Mock()
        cursor = Mock()
        conn.cursor.return_value = cursor
        mock_get_db_connection.return_value = conn

        create_or_update_student(7, 'Alice', roll_number='24CS1001', email='alice@example.com')

        conn.commit.assert_called_once()
        cursor.execute.assert_called_once()
        sql = cursor.execute.call_args[0][0]
        self.assertIn('INSERT INTO Students', sql)
        self.assertIn('full_name', sql)
        self.assertIn('roll_number', sql)
        self.assertEqual(cursor.execute.call_args[0][1], (7, '24CS1001', 'Alice', 'alice@example.com'))

    @patch('routes.student_routes.allocate_room')
    def test_boom_alias_returns_booking_response(self, mock_allocate_room):
        mock_allocate_room.return_value = (True, 'Success! Room assigned', None)

        response = self.client.post('/book', data={'student_id': '24CS1001', 'student_name': 'Test User'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Success! Room assigned', response.get_data(as_text=True))

    @patch('models.db.get_db_connection')
    def test_api_occupancy_serializes_decimal_values(self, mock_get_db_connection):
        conn = Mock()
        cursor = Mock()
        cursor.fetchall.return_value = [{
            'hostel_id': 1,
            'hostel_name': 'A',
            'total_rooms': 2,
            'total_beds': Decimal('4'),
            'occupied_beds': Decimal('2'),
            'available_beds': Decimal('2')
        }]
        conn.cursor.return_value = cursor
        mock_get_db_connection.return_value = conn

        response = self.client.get('/api/occupancy')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['success'])
        self.assertEqual(response.get_json()['stats'][0]['total_beds'], 4)

    @patch('services.student_service.get_db_connection')
    def test_create_or_update_student_retries_on_lock_timeout(self, mock_get_db_connection):
        conn = Mock()
        cursor = Mock()
        conn.cursor.return_value = cursor
        conn.commit.return_value = None
        conn.rollback.return_value = None
        cursor.execute.side_effect = [DatabaseError("Lock wait timeout exceeded", 1205), None]
        mock_get_db_connection.return_value = conn

        create_or_update_student(7, 'Alice', roll_number='24CS1001', email='alice@example.com')

        self.assertEqual(cursor.execute.call_count, 2)
        conn.rollback.assert_called_once()
        conn.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
