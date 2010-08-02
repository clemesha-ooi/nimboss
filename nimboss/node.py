from libcloud.drivers.ec2 import EC2Connection, EC2NodeDriver

class NimbusConnection(EC2Connection):

    host = ''
    port = (80, 8444)
    secure = 1

class NimbusNodeDriver(EC2NodeDriver):

    connectionCls = NimbusConnection
    name = "Nimbus"

    def _fixxpath(self, xpath):
        # Nimbus return types don't include namespace declaration in every
        # tag, unlike EC2. So we override this method to make xpath queries
        # just pass through instead of being ns-prefixed.
        return xpath
