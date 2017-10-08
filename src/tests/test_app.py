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

    def test_health(self):
        """Testing health"""
        result = self.simulate_get('/health')
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(result.text, 'OK')

    def test_testing(self):
        """Testing testing"""
        result = self.simulate_get('/test')
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(result.text, 'testing...')