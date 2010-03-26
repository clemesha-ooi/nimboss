import hashlib

from nimboss.nimbus import NimbusClusterFile

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

    def create(self, cluster_spec):
        self.driver.create(self, cluster_spec)

    def get_uuid(self):
        return hashlib.sha1("%s:%d" % (self.id, self.driver.type)).hexdigest()

    def __repr__(self):
        args = (self.uuid, self.name, len(self.nodes.keys()))
        return 'Cluster: uuid=%s, name=%s, total nodes=%d' % args



class ClusterDriver(object):
    """Logic to manage a Cluster.

    Key parts:
        - the 'Cluster' (comprised of Nodes) 
        - the 'ContextBroker'
    """

    def __init__(self, context_broker, cluster_uuid=None, cluster_spec=None):
        self.context_broker = context_broker
        self.cluster_spec = cluster_spec
        self.cluster_uuid = cluster_uuid
        self.cluster = Cluster(cluster_uuid)

    def create(self, cluster_spec):
        if isinstance(cluster_spec, list):
            nodes_specs = cluster_spec # list of AMI ids? 
        else:
            nimbuscf = NimbusClusterFile(cluster_spec) 
            nodes_specs = nimbuscf.get_node_specs()

        new_context = self.context_broker.create_new_context(self, cluster_data)

        for spec in nodes_specs:
            node_data = self._create_node_data(spec, new_context)
            node = Node(node_data) #XXX make this clean / consi
            self.cluster.add_node(node)

    def _create_node_data(self, spec, new_context):
        #XXX what to do here? 
        return {'the':the, 'data':data}

    def destroy(self):
        for (id, node) in self.cluster.nodes.iteritems():
            node.destroy()

    def reboot(self)
        for (id, node) in self.cluster.nodes.iteritems():
            node.destroy()

    def query(self, request):
        resp = self.context_broker.query(self.cluster_uuid)
        return resp


