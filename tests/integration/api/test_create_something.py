# -*- coding: utf-8 -*-

from tests.integration import base
# from app.domains import my_domain


class TestGetAreas(base.TestCase):
    url = '/api/something'

    @base.mock.patch('app.resource.g')
    def test_buy_a_car(self, g_mock):
        some_object = base.read_json('something', 'create_json')
        self.payload = some_object
        g_mock.authenticated = True
        g_mock.user = {'id': 1, "email": 'user@elsys.com.br'}
        response = self.response_post
        self.assertEqual(response.status_code, 200)

        # Here the ideia is to go to the data base and really create and check for the data inserted

        # something = my_domain.Something.create_from_id(1)
        # self.assertEqual(something.id, 1)
        # self.assertEqual(something.name, 'Walter White')
