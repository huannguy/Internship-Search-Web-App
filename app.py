import flask
from flask.views import MethodView
import os
from flask import Flask

from operations import Index, Search, Display, ManualAdd, Manage

app = flask.Flask(__name__)     #Initializes the Flask application.
app.secret_key = os.urandom(24) #Sets a random secret key for session security.

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/search',
                 view_func=Search.as_view('search'),
                 methods=['GET', 'POST'])

app.add_url_rule('/display',
                 view_func=Display.as_view('display'),
                 methods=['GET', 'POST'])

app.add_url_rule('/manual-add',
                 view_func=ManualAdd.as_view('manual-add'),
                 methods=['GET', 'POST'])

app.add_url_rule('/manage',
                 view_func=Manage.as_view('manage'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
