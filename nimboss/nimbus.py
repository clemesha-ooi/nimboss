# Nimbus Specific logic


class NimbusClusterDocument(object):
    """
    Given a Nimbus cluster document, parse enough
    to access all parameters for a Node instance.

    """

    def __init__(self, clusterdoc):
        self.clusterdoc = clusterdoc

    def get_node_specs(self):
        nodes_specs = self._cluser_doc_to_node_spec()
        return node_specs

    def _cluser_file_to_node_spec(self):
        #TODO parse clusterdoc, get in form to pass to Node objects.
        return do_parse_magic(self.clusterdoc)
