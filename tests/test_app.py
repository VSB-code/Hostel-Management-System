import unittest
from unittest.mock import Mock, patch

from app import create_app
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


if __name__ == '__main__':
    unittest.main()
