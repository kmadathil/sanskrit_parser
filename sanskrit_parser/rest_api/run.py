#!/usr/bin/python3 -u

# This web app may be run in two modes. See bottom of the file.

import logging
import os.path
import sys

from sanskrit_parser.rest_api.flask_helper import app
from sanskrit_parser.rest_api import api_v1
from sanskrit_parser import enable_file_logger, enable_console_logger

enable_console_logger(level=logging.INFO)
enable_file_logger(level=logging.DEBUG)
print(logging.getLogger('sanskrit_parser').getEffectiveLevel())

#logging.basicConfig(
#      level=logging.INFO,
#      filename="SanskritParserApi.log",
#      filemode='w',
#      format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
# )

#console = logging.StreamHandler()
#console.setLevel(logging.INFO)
## set a format which is simpler for console use
#formatter = logging.Formatter('%(levelname)-8s %(message)s')
## tell the handler to use this format
#console.setFormatter(formatter)
## add the handler to the root logger
#logging.getLogger(' ').addHandler(console)


# Add parent directory to PYTHONPATH, so that sanskrit_parser module can be found.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
logging.debug(sys.path)

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
