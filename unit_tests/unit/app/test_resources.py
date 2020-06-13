import json

from unit_tests import base
from app import resource


class SomethingResourceTest(base.TestCase):

    @base.TestCase.mock.patch('app.resource.ResourceBase.cookies')
    @base.TestCase.mock.patch('app.resource.g')
    def test_get_return_not_auth(self, g_mock, cookies_mock):
        g_mock.authenticated = False
        g_mock.user = None
        something_resource = resource.SomethingResource()
        response = something_resource.get()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data), {"result": "Not Authorized"})
