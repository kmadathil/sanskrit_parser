'''
Convert dhAtu-pATha-kRShNAchArya.tsv to json

'''

from __future__ import print_function

import logging
import os
import codecs

from tinydb import TinyDB

from sanskrit_parser.base.sanskrit_base import SanskritObject

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: {%(filename)s:%(lineno)d}: %(message)s "
)


def generate_db(tsv_file, db_file):
        """ Create db from tsv file """
        logger.info("Converting tsv %s to db file %s", tsv_file, db_file)
        if os.path.exists(db_file):
            os.remove(db_file)
        db = TinyDB(db_file)
        with codecs.open(tsv_file, "rb", encoding="utf-8") as f:
            row = f.readline().split("\t")
            headers = [SanskritObject(x).canonical() for x in row[0:8]]
            logger.info("Found dhatu tsv headers: {}".format(str(headers)))
            # FIXME - Rewrite from here
            for row in f:
                entries = row.split("\t")[:len(headers)]
                entries = [SanskritObject(e).canonical() for e in entries]
                j = dict(zip(headers, entries))
                db.insert(j)
        db.close()
        logger.info("Saved dhatus database")


if __name__ == "__main__":
    tsv_file = "dhAtu-pATha-kRShNAchArya.tsv"
    db_file = os.path.splitext(tsv_file)[0] + ".json"
    generate_db(tsv_file, db_file)
