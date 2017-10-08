import falcon
import json

class Resource(object):

    def on_get(self, req, resp):
        if req.path == '/':
            doc = {'version':'0.1'}
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200


        if req.path == '/health':
            resp.body = ('OK')
            resp.status = falcon.HTTP_200

        if req.path =='/test':
            resp.body = ('testing...')
            resp.status = falcon.HTTP_200



def myapp():
    app = falcon.API()
    resource = Resource()
    app.add_route('/', resource)
    app.add_route('/health', resource)
    app.add_route('/test', resource)
    return app

if __name__ == '__main__':
    from wsgiref import simple_server
    wsgi_app = myapp()
    httpd = simple_server.make_server('127.0.0.1', 8080, wsgi_app)
    httpd.serve_forever()
