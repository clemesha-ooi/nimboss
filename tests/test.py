import os
import sys
sys.path.insert(0, os.path.abspath("../"))

import unittest

from nimboss.nimbus import NimbusClusterDocument
from nimboss.broker import ContextResource, BrokerClient
from nimboss.node import NimbusNodeDriver, EC2NodeDriver
from nimboss.cluster import Cluster, ClusterDriver


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


class TestEC2Cluster(unittest.TestCase):

    def setUp(self):
        self.clusterdoc = open("test_clusterdoc.xml").read()
        self.context_uri = "http://example.com/"
        self.context_body = {
            'broker_uri':'test_broker_uri', 
            'context_id':'test_context_id', 
            'secret':'test_secret'
        }
        self.broker_uri = "http://example.com/"
        self.broker_key = "broker_key"
        self.broker_secret = "broker_secret"
        self.cloud_key = os.environ["AWS_KEY"]
        self.cloud_secret = os.environ["AWS_SECRET"]

    def test_start_cluster(self):
        broker_client = BrokerClient(self.broker_uri, self.broker_key, self.broker_secret)  

        node_driver = EC2NodeDriver(self.cloud_key, self.cloud_secret)
        cluster_driver = ClusterDriver(broker_client, node_driver)
        cluster = Cluster(self.context_uri, cluster_driver)

        fake_context = ContextResource(self.context_uri, self.context_body)
        cluster.create_cluster(self.clusterdoc, context=fake_context)



if __name__ == '__main__':
    unittest.main()
