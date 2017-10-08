from falcon import testing
import falcon

from ..app.app import myapp


class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.API` instance.
        self.app = myapp()


class TestMyApp(MyTestCase):
    def test_get_message(self):
        doc = {u'message': u'Hello world!'}

        result = self.simulate_get('/health')
        self.assertEqual(result.status, falcon.HTTP_200)