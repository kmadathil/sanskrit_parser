# -*- coding: utf-8 -*-

"""
Repurpose old class to create the database that is included
with package

"""

import os
from collections import defaultdict
from io import BytesIO
import pickle
import logging
import sqlite3
import marisa_trie
import struct

from tqdm import tqdm
from lxml import etree
import requests


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
        """ Create the database """

        '''
        The custom database format has two parts:
            1. A pickle file that contains a list of stems and
               a list of tags
            2. A trie that maps each form to a sequence of bytes which
               encodes the index of the stem in 2 bytes followed by the
               indices of the tags

        To lookup the tag for a form, we retrieve the list of 
        tag sets from the trie. For each item in the list, we then decode 
        the bytes to get the index of the stem and the indices of the tags.
        These are used to lookup the right stem and tag in
        the list of stems and tags loaded from the pickle file
        '''

        # List + dict to map tags/stem to an int index
        tag_list = []
        tag_dict = {}
        stem_list = []
        stem_dict = {}

        def get_index_val(k, f_list, f_dict):
            if k not in f_dict:
                f_list.append(k)
                f_dict[k] = len(f_list) - 1
            return f_dict[k]

        entries = []
        packer = struct.Struct("<h")
        num_tags = 0
        for form in tqdm(self.forms):
            tags = self._xml_to_tags(form)
            num_tags += len(tags)
            for stem, tag_set in tags:
                s = get_index_val(stem, stem_list, stem_dict)
                t = []
                for tag in tag_set:
                    t_index = get_index_val(tag, tag_list, tag_dict)
                    t.append(t_index)
                entry = (form, packer.pack(s) + bytes(t))
                entries.append(entry)

        print(f'Len(tags) = {len(tag_list)}, len(stems) = {len(stem_list)}')
        print(f'Number of tags = {num_tags}')

        pkl_path = os.path.join(output_path, 'inria_stems_tags.pkl')
        with open(pkl_path, 'wb') as f:
            pickle.dump(tuple(stem_list), f)
            pickle.dump(tuple(tag_list), f)

        trie = marisa_trie.BytesTrie(entries)
        trie.save("inria_db.marisa")
        

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(root_dir, 'sanskrit_parser',
                               'data')
    print(f'Saving INRIA database to {output_path}')
    wrapper = InriaXMLWrapper()
    wrapper.create_mapped_db(output_path)
