import os

from flask import Flask

from application.rest.views import api_blueprint
from application.web.views import web_blueprint

app = Flask(__name__, static_url_path='/')
app.register_blueprint(web_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    # Used only for local development from docker-compose.yml
    app.run(host='0.0.0.0', port=os.environ['PORT'], debug=True)
