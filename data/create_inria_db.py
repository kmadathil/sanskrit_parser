# -*- coding: utf-8 -*-

"""
Repurpose old class to create the database that is included
with package

"""

import requests
import os
from lxml import etree
from collections import defaultdict
from io import BytesIO
import logging
from tqdm import tqdm
import pickle


class InriaXMLWrapper():
    """
    Class to interface with the INRIA XML database released
    by Prof. Gerard Huet
    https://gitlab.inria.fr/huet/Heritage_Resources
    """
    base_url = "https://raw.githubusercontent.com/drdhaval2785/inriaxmlwrapper/master/"
    xml_files = ["roots", "nouns", "adverbs", "final", "parts", "pronouns", "upasargas", "all"]

    def __init__(self, files_list=['all'], logger=None):
        for f in files_list:
            if f not in self.xml_files:
                raise Exception(f + "is not a valid file name")
        self.files = files_list
        self.files.sort()
        self.pickle_file = "_".join(self.files) + ".pickle"
        if ["all"] == self.files:
            self.files = self.xml_files[:-1]
            self.pickle_file = "_all.pickle"
        self.logger = logger or logging.getLogger(__name__)
        self._load_forms()

    def _get_files(self):
        """ Download files if not present in cache """
        for f in self.files:
            filename = "SL_" + f + ".xml"
            if not os.path.exists(filename):
                self.logger.debug("%s not found. Downloading it", filename)
                r = requests.get(self.base_url + filename, stream=True)
                with open(filename, "wb") as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)

    def _generate_dict(self):
        """ Create dict with mapping
            form : set([<tag 1>, ... , <tag n>])
            and pickle it
        """
        self._get_files()
        self.logger.info("Parsing files into dict for faster lookup")
        self.forms = defaultdict(list)
        for f in tqdm(self.files):
            filename = "SL_" + f + ".xml"
            self.logger.debug("Parsing %s", filename)
            tree = etree.parse(filename)
            for elem in tree.iterfind('f'):
                form = elem.get('form')
                self.forms[form].append(etree.tostring(elem).strip())

    def _load_forms(self):
        """ Load/create dict of tags for forms """
        self._generate_dict()

    def _xml_to_tags(self, word):
        # FIXME - This is currently from sanskritmark. Check if this can be simplified
        if word in self.forms:
            tags = self.forms[word]
            results = []
            for tag in tags:
                root = etree.parse(BytesIO(tag)).getroot()
                # The next two steps require explanation. In Gerard's XML files,
                # All possible attributes are given as children of 'f'. The last
                # child is always 's' which stores the stem. All other children
                # are the various possible word attributes. Given as 'na' or 'v'
                # etc. Gio
                children = root.getchildren()[:-1]  # attributes
                baseword = root.getchildren()[-1].get('stem').strip()  # 's' stem
                attributes = []
                for child in children:
                    taglist = child.xpath(
                        './/*')  # Fetches all elements (abbreviations) of a particular verb / word characteristics.
                    output = [child.tag]  # The first member of output list is the tag of element 'v', 'na' etc.
                    output = output + [tagitem.tag for tagitem in
                                       taglist]  # Other tags (abbreviations) and add it to output list.
                    attributes.append(output)
                for attrib in attributes:
                    results.append((baseword, set(attrib)))
            return results
        else:
            return None

    def create_mapped_db(self, output_path):
        """ Quick and dirty function to map each tag/stem to
            an integer and store the integers along with an
            index of the mapping
        """
        # Index list of each tag/form we encounter
        index = []
        # A dict to map a given tag/form to its index entry
        index_dict = {}

        def get_index_val(k):
            if k not in index_dict:
                index.append(k)
                index_dict[k] = len(index) - 1
            return index_dict[k]

        new_forms = defaultdict(tuple)

        for form in tqdm(self.forms):
            tags = self._xml_to_tags(form)
            new_tags = []
            for stem, tag_set in tags:
                s = get_index_val(stem)
                t = [s]
                for tag in tag_set:
                    s = get_index_val(tag)
                    t.append(s)
                new_tags.append(t)
            new_forms[form] += tuple(new_tags)

        with open(output_path, 'wb') as f:
            pickle.dump(new_forms, f)
            pickle.dump(tuple(index), f)

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(root_dir, 'sanskrit_parser',
                               'data', 'inria_forms.pickle')
    print(f'Saving INRIA database to {output_path}')
    InriaXMLWrapper().create_mapped_db(output_path)