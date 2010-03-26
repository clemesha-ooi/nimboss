# Nimbus Specific logic


class NimbusClusterFile(object):
    """
    Given a Nimbus cluster file, parse enough
    to access all parameters for a Node instance.

    The main idea is here, but does not feel right yet...
    """


    def __init__(self, clusterfile):
        self.clusterfile = clusterfile

    def get_node_specs(self):
        nodes_specs = self._cluser_file_to_node_spec()
        return node_specs

    def _cluser_file_to_node_spec(self):
        #parse clusterfile, get in form to pass to Node objects.
        return do_parse_magic(self.clusterfile)
