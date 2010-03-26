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
        self.nodes = {}

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
        - the 'Cluster' (comprised of Nodes) 
        - the 'ContextBroker'
    """

    nodeDriver = None

    def __init__(self, context_broker, cluster_uuid):
        self.context_broker = context_broker
        self.cluster = Cluster(cluster_uuid)

    def create_cluster(self, clusterdoc):
        nimbuscd = NimbusClusterDocument(clusterdoc) 
        nodes_specs = nimbuscd.get_node_specs()
        new_context = self.context_broker.create_new_context(self, cluster_data)

        for spec in nodes_specs:
            node_data = self._create_node_data(spec, new_context)
            node = Node(node_data) #XXX a "libcloud Node" instance. 
            self.cluster.add_node(node)

    def _create_node_data(self, spec, new_context):
        #XXX what to do here? 
        return {'the':the, 'data':data}

    def destroy_cluster(self):
        for (id, node) in self.cluster.nodes.iteritems():
            node.destroy()

    def reboot_cluster(self)
        for (id, node) in self.cluster.nodes.iteritems():
            node.destroy()

    def query_cluster(self, request):
        resp = self.context_broker.query(self.cluster.uuid)
        return resp



class NimbusClusterDriver(ClusterDriver):
    nodeDriver = NimbusNodeDriver
    create_node = nodeDriver.create_node
    destroy_node = nodeDriver.destroy_node


class EC2ClusterDriver(ClusterDriver):
    nodeDriver = EC2NodeDriver
    create_node = nodeDriver.create_node
    destroy_node = nodeDriver.destroy_node
