import os
from nimboss.broker import BrokerClient
from nimboss.cluster import NimbusClusterDriver

BROKER_URI = "http://mybroker.edu"


def main():
    key, secrect = os.environ["BROKER_KEY"], os.environ["BROKER_SECRET"]
    brokerclient = BrokerClient(BROKER_URI, key, secret)
    cdriver = NimbusClusterDriver(brokerclient)

    clusterdoc = open("/path/to/myclusterdoc.xml").read()
    cdriver.create_cluster(clusterdoc)
    print "Starting cluster...."
    while 1:
        time.sleep(5)
        print "Cluster status => ", cdriver.get_status(BROKER_URI+"/status")


if __name__ == "__main__":
    main()

