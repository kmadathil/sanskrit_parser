import logging
import os
from base64 import b64encode

import flask
from flask_cors import CORS

from sanskrit_parser.rest_api import api_v1


# Filter some logs to make it easier to focus on overall progress
logging.disable(logging.DEBUG)
# logging.getLogger("sanskrit_parser.base.sanskrit_base").setLevel(logging.INFO)
# logging.getLogger("sanskrit_parser.parser.sandhi").setLevel(logging.INFO)
# logging.getLogger("sanskrit_parser.parser.datastructures").setLevel(logging.INFO)
# logging.getLogger("sanskrit_parser.parser.sandhi_analyzer").setLevel(logging.INFO)
# logging.getLogger("sanskrit_parser.util.inriaxmlwrapper").setLevel(logging.INFO)
# logging.getLogger("sanskrit_parser.util.sanskrit_data_wrapper").setLevel(logging.INFO)
# logging.getLogger("sanskrit_parser.util.lexical_scorer").setLevel(logging.INFO)
# logging.getLogger("sanskrit_parser.util.normalization").setLevel(logging.INFO)
# logging.getLogger("sanskrit_util.analyze").setLevel(logging.INFO)

app = flask.Flask(
  # We pass the root module name - sets root directory.
  import_name="sanskrit_parser.rest_api.run")

# Let Javascsipt hosted elsewhere access our API.
CORS(app=app,
     # injects the `Access-Control-Allow-Credentials` header in responses.
     # This allows cookies and credentials to be submitted across domains.
     supports_credentials=True)
logging.info(str(app))

app.config.update(
  DEBUG=True,
  # Used to encrypt session cookies.
  SECRET_KEY=b64encode(os.urandom(24)).decode('utf-8'),
)

app.register_blueprint(api_v1.api_blueprint, url_prefix="/sanskrit_parser")


@app.route('/')
def index():
    flask.session['logstatus'] = 1
    return flask.redirect('/ui/index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
