import hashlib

from nimboss.nimbus import NimbusClusterFile
from nimboss.node import NimbusNodeDriver, EC2NodeDriver

class Cluster(object):
    """A Cluster is a collection of Nodes.
    """

    def __init__(self, id, driver, cluster_type=None, name=None):
        self.id = id
        self.driver = driver
        self.cluster_type = cluster_type
        self.name = name or ''
        self.uuid = self.get_uuid()
        self.nodes = {} #XXX if the cluster (unique by 'id') exists, populate this?

    def add_node(self, node):
        self.nodes[node.id] = node

    def create_cluster(self, clusterdoc):
        self.driver.create_cluster(self, clusterdoc)

    def get_uuid(self):
        return hashlib.sha1("%s:%d" % (self.id, self.driver.type)).hexdigest()

    def __repr__(self):
        args = (self.uuid, self.name, len(self.nodes.keys()))
        return "Cluster: uuid=%s, name=%s, total nodes=%d" % args



class ClusterDriver(object):
    """Logic to manage a Cluster.

    Key parts:
        - 'nodeDriver' attribute
        - 'BrokerClient' instance.
    """

    nodeDriver = None

    def __init__(self, broker_client):
        self.broker_client = broker_client

    def create_cluster(self, clusterdoc):
        nimbuscd = NimbusClusterDocument(clusterdoc) 
        new_context = self.broker_client.create_context()
        nodes_specs = nimbuscd.build_specs(new_context)

        for spec in nodes_specs:
            node_data = self._create_node_data(spec)
            new_node = self._create_node(node_data)

    def _create_node(self, **kwargs):
        newnode = self.nodeDriver.create_node(kwargs)

    def _create_node_data(self, spec):
        #XXX what to do here? 
        return {}

    def destroy_cluster(self, cluster):
        for (id, node) in cluster.nodes.iteritems():
            node.destroy()

    def reboot_cluster(self, cluster):
        for (id, node) in cluster.nodes.iteritems():
            node.destroy()

    def get_status(self, context_uri):
        resp = self.broker_client.get_status(context_uri)
        return resp



class NimbusClusterDriver(ClusterDriver):
    nodeDriver = NimbusNodeDriver
    create_node = nodeDriver.create_node
    destroy_node = nodeDriver.destroy_node


class EC2ClusterDriver(ClusterDriver):
    nodeDriver = EC2NodeDriver
    create_node = nodeDriver.create_node
    destroy_node = nodeDriver.destroy_node
