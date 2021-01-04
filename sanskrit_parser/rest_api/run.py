#!/usr/bin/python3 -u

# This web app may be run in two modes. See bottom of the file.

import logging
import os.path
import sys
from logging.handlers import RotatingFileHandler

# Add parent directory to PYTHONPATH, so that sanskrit_parser module can be found.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
logging.debug(sys.path)


from sanskrit_parser.rest_api.flask_helper import app  # noqa: E402
from sanskrit_parser.rest_api import api_v1  # noqa: E402

LOG_FILENAME = "SanskritParserApi.log"
LOG_FORMAT = "%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
formatter = logging.Formatter(LOG_FORMAT)
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logging.getLogger(' ').addHandler(handler)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger(' ').addHandler(console)

params = {
    'port': 9000,
}


def setup_app():
    app.register_blueprint(api_v1.api_blueprint, url_prefix="/sanskrit_parser")


def main(argv):
    setup_app()
    app.run(
      host="0.0.0.0",
      debug=False,
      port=params["port"],
      use_reloader=False
    )


if __name__ == "__main__":
    logging.info("Running in stand-alone mode.")
    main(sys.argv[1:])
else:
    logging.info("Likely running as a WSGI app.")
    setup_app()
