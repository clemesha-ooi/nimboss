import os
import sys
sys.path.insert(0, os.path.abspath("../"))

import unittest

from nimboss.nimbus import NimbusClusterDocument
from nimboss.broker import ContextResource


class TestClusterDocLoadParse(unittest.TestCase):

    def setUp(self):
        self.clusterdoc = open("test_clusterdoc.xml").read()
        self.context_uri = "http://example.com/"
        self.context_body = {
            'broker_uri':'test_broker_uri', 
            'context_id':'test_context_id', 
            'secret':'test_secret'
        }

    def test_loadparse(self):
        nimbuscd = NimbusClusterDocument(self.clusterdoc)
        self.assertEqual(len(nimbuscd.members), 2)
        self.assertEqual(nimbuscd.members[0].quantity, 1)
        self.assertEqual(nimbuscd.members[1].quantity, 2)

    def test_build_specs(self):
        nimbuscd = NimbusClusterDocument(self.clusterdoc)
        ctx = ContextResource(self.context_uri, self.context_body)
        specs = nimbuscd.build_specs(ctx)
        self.assertEqual(len(specs), 2)
        self.assertEqual(specs[0].count, 1)
        self.assertEqual(specs[1].count, 2)
        self.assertEqual(specs[0].image, "ami-b48765dd")


if __name__ == '__main__':
    unittest.main()
