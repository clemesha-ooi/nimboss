from libcloud.drivers.ec2 import EC2Connection, EC2NodeDriver


class NimbusConnection(EC2Connection):

    #host = "https://tp-vm1.ci.uchicago.edu"
    host = "128.135.125.124"
    port = (80, 8444) 
    secure = 1


class NimbusNodeDriver(EC2NodeDriver):

    connectionCls = NimbusConnection
    name = "Nimbus"

