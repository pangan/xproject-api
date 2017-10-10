import falcon
import json

class Resource(object):

    def on_get(self, req, resp):
        if req.path == '/':
            doc = {
                'project': 'xproject-api',
                'version':'0.1'
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200

        elif req.path == '/health':
            resp.body = ('OK')
            resp.status = falcon.HTTP_200

        elif req.path =='/test':
            resp.body = ('testing...')
            resp.status = falcon.HTTP_200

        else:
            resp.status = falcon.HTTP_405


    def on_post(self, req, resp):

        try:
            if 'application/json' not in req.content_type:
                raise ValueError('Not json content-type!')
            request_data = req.stream.read()
            json.loads(request_data)
            resp.body = request_data
            resp.status = falcon.HTTP_200
        except ValueError, e:
            resp.body = e.message
            resp.status = falcon.HTTP_400






def myapp():
    app = falcon.API()
    resource = Resource()
    app.add_route('/', resource)
    app.add_route('/health', resource)
    app.add_route('/test', resource)
    app.add_route('/post_metrics', resource)
    return app

if __name__ == '__main__':
    from wsgiref import simple_server
    wsgi_app = myapp()
    httpd = simple_server.make_server('0.0.0.0', 8080, wsgi_app)
    httpd.serve_forever()
