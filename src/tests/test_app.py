
from falcon import testing
from faker import Faker
import falcon
import json
import influxdb

from ..app.app import myapp, INFLUX_HOST
from ..app.utils import write_to_influxdb

fake = Faker()


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
        self.assertDictEqual(result.json, doc)

    def test_health(self):
        """Testing health"""
        result = self.simulate_get('/health')
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(result.text, 'OK and running!')

    def test_testing(self):
        """Testing testing"""
        result = self.simulate_get('/test')
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(result.text, 'testing...')

    def test_posting_data(self):
        """Test posting data"""
        sending_data = {
            fake.text(): fake.text(),
            fake.text(): fake.text()
        }
        headers = {"Content-Type": "application/json"}
        result = self.simulate_post(path='/post_metrics', body=json.dumps(sending_data), headers=headers)
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertDictEqual(sending_data, result.json)

    def test_return_error_if_post_header_is_not_json(self):
        """Test return error if post header is not json"""
        sending_data = {
            'aa': 'bb'
        }
        headers = {'Content-Type': 'application/{0}'.format(fake.user_name())}
        result = self.simulate_post(path='/post_metrics', body=json.dumps(sending_data), headers=headers)
        self.assertEqual(result.status, falcon.HTTP_400)

    def test_return_error_if_post_data_is_not_json(self):
        """Test return error if post data is not json"""
        sending_data = fake.text()
        headers = {'Content-Type': 'application/json'.format(fake.user_name())}
        result = self.simulate_post(path='/post_metrics', body=sending_data, headers=headers)
        self.assertEqual(result.status, falcon.HTTP_400)

    def test_not_posting_data_without_post(self):
        """Test not posting data without post"""
        result = self.simulate_get('/post_metrics')
        self.assertEqual(result.status, falcon.HTTP_405)

        result = self.simulate_put('/post_metrics')
        self.assertEqual(result.status, falcon.HTTP_405)

    # it should be moved to utils test!
    def test_write_influx(self):
        """Test writing into the influxdb"""

        client = influxdb.InfluxDBClient(
            host=INFLUX_HOST,
            port=80, database='xproject_test')
        client.drop_database('xproject_test')

        rs = self.simulate_get('/write_test',query_string='database=xproject_test&value=12.5&host=localhost')
        a = rs.status
        #write_to_influxdb(influx_host_params, data_params)
        result = client.query('select value from temp')

        returned_value = list(result.get_points('temp'))
        self.assertEquals(returned_value[0]['value'], 12.5)
        client.drop_database('xproject_test')
