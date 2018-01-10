from influxdb import InfluxDBClient

def write_to_influxdb(host_params, data_param):
    client = InfluxDBClient(host=host_params['host'],
                            port=host_params['port'],
                            database=host_params['database'])
    client.create_database(host_params['database'])
    client.write_points(data_param)
