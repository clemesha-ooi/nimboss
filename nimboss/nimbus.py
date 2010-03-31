import xml.etree.ElementTree as ET

class NimbusClusterDocument(object):
    """
    Given a Nimbus cluster document, parse enough
    to access all parameters for a Node instance.
    """

    public_nic_prefix=None
    local_nic_prefix=None

    def __init__(self, doc, 
            public_nic_prefix="public", local_nic_prefix="private"):
        
        # these are ugly. Used in nic matching process; they must
        # be in place before parse.
        self.public_nic_prefix = public_nic_prefix
        self.local_nic_prefix = local_nic_prefix

        self.parse(doc)

    def parse(self, doc):
        self.tree = ET.fromstring(doc)

        if self.tree.tag != 'cluster':
            raise ValidationError("Root element must be 'cluster'")

        members = self.tree.findall('workspace')
        if members is None:
            raise ValidationError("Must have at least one 'workspace' element")

        self.members = [_ClusterMember(self, node) for node in members]

    def build_specs(self, context):
        """
        Produces userdata launch information for cluster document, using the
        specified context.
        """

        ctx_tree = ET.Element('NIMBUS_CTX')
        ctx_tree.append(create_contact_element(context))
        ctx_tree.append(self.tree)

        specs = []
        for member in self.members:
            userdata = None
            if member.needs_contextualization:
                member.set_active_state(True)
                userdata = ET.tostring(ctx_tree)
                member.set_active_state(False)
            s = ClusterNodeSpec(member.image, member.quantity, userdata)
            specs.append(s)
        return specs

def create_contact_element(context):
    """
    Produces a <contact> element for a Context resource
    """
    elem = ET.Element('contact')
    ET.SubElement(elem, 'brokerURL').text = context.broker_uri
    ET.SubElement(elem, 'contextID').text = context.context_id
    ET.SubElement(elem, 'secret').text = context.secret
    return elem

class _ClusterMember(object):
    """
    A single 'workspace' of a cluster document. For internal use only.
    """

    def __init__(self, document, element):
        self.document = document
        self.element = element

        self.image = _get_one_subelement(element, 'image').text.strip()
        quantity = _get_one_subelement(element, 'quantity')
        try:
            self.quantity = int(quantity.text)
        except ValueError:
            raise ValidationError("Workspace quantity must be an integer")

        #TODO validate NICs/doctor ctx

        if element.find('active') is not None:
            raise ValidationError("Workspace may not have an 'active' element")
        self._active_element = ET.SubElement(element, 'active')
        self._active_element.text = 'false'

        # TODO determine this value for reals
        self.needs_contextualization = True

    def set_active_state(self, state):
        self._active_element.text = state and 'true' or 'false'

def _get_one_subelement(element, tag):
    result = element.findall(tag)
    if result is None or len(result) != 1:
        raise ValidationError(
                "There must be exactly one '%s' element per workspace" % tag) 
    if not result[0].text.strip():
        raise ValidationError("The '%s' element must have a value" % tag)
    return result[0]

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
