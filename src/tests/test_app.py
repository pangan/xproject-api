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

    def test_info(self):
        """Testing info"""
        doc = {
            'project': 'xproject-api',
            'version':'0.1'}
        result = self.simulate_get('/')
        self.assertEqual(result.json, doc)


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

    def test_posting_data(self):
        """Test posting data"""
        result = self.simulate_post('/post_metrics')
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_not_posting_data_without_post(self):
        """Test not posting data without post"""
        result = self.simulate_get('/post_metrics')
        self.assertEqual(result.status, falcon.HTTP_405)

        result = self.simulate_put('/post_metrics')
        self.assertEqual(result.status, falcon.HTTP_405)
