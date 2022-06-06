from Messenger.common.variables import *
from Messenger.server import process_client_message

import unittest


# Класс с тестами
class TestServer(unittest.TestCase):
    error_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        self.assertEqual(process_client_message({TIME: '1', USER: {ACCOUNT_NAME: 'Guest'}}), self.error_dict)

    def test_no_user(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: '1'}), self.error_dict)

    def test_no_time(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_dict)

    def test_any_user(self):
        self.assertEqual(process_client_message({TIME: '1', ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'User'}}),
                         self.error_dict)

    def test_bad_action(self):
        self.assertEqual(process_client_message({ACTION: 'Leave', TIME: '1', USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.error_dict)

    def test_ok(self):
        self.assertEqual(process_client_message({TIME: '1', ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.ok_dict)


if __name__ == '__main__':
    unittest.main()
