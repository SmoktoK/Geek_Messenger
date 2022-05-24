from Messenger.common.variables import *
from Messenger.client import create_presence, process_ans

import unittest


# Класс с тестами
class TestClient(unittest.TestCase):
    #  Проверка соединения
    def test_def_presence(self):
        test = create_presence('Guest')
        test[TIME] = 1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_username(self):
        username = create_presence()
        self.assertEqual(username['user'], {ACCOUNT_NAME: 'Guest'})
        # print(username['user'])

    def test_action(self):
        action = create_presence()
        self.assertEqual(action[ACTION], PRESENCE)

    #  Проверка доступности
    def test_200(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_400(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')


if __name__ == '__main__':
    unittest.main()
