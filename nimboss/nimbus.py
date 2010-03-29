# Nimbus Specific logic

import xml.etree.ElementTree as ET

class NimbusClusterDocument(object):
    """
    Given a Nimbus cluster document, parse enough
    to access all parameters for a Node instance.
    """

    def __init__(self, doc):

        self.parse(doc)

    def parse(self, doc):
        tree = ET.fromstring(doc)

        root = tree.getroot()
        if root.tag != 'cluster':
            raise ValidationError("Root element must be 'cluster'")

        members = tree.findall('workspace')
        if len(members) == 0:
            raise ValidationError("Must have at least one 'workspace' element")

    def build_specs(self, context, local_nic_prefix=None, 
            public_nic_prefix=None):
        """
        Produces userdata launch information for cluster document, using the
        specified context.
        """
        pass

class _ClusterMember(object):
    """
    A single 'workspace' of a cluster document. For internal use only.
    """
    def __init__(self, element):
        pass # do some parsing
        

class ValidationError(Exception):
    """
    Problem validating structure of cluster document.
    """
    def __init(self, reason):
        self.reason = reason
        Exception.__init__(self, reason)

class ClusterNodeSpec(object):
    """
    Information needed to launch a single cluster member.
    Image name (ami), node count, and userdata.
    """

    def __init__(self, image, count, userdata=None):
        self.image = image
        self.count = int(count)
        self.userdata = userdata
