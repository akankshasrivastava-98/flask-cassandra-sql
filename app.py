import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from API import blueprint as api


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(api, url_prefix='/api')

# app.run(debug=True
if __name__ == '__main__':
    app.run(port=5000, debug=True)