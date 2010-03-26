import sys
import ConfigParser


def getconfig(filepath):
    config = ConfigParser.SafeConfigParser()
    config.read(filepath)
    return config

def getlogging(config, opts):
    #TODO do logging setup
    return logger


def start_cluster(**kwargs):
    """
    "Example usage." (Probably missing A LOT).

    Does this make sense at all???

    """
    from nimboss.broker import ContextBroker
    from nimboss.cluster import Cluster, ClusterDriver
    context_broker = ContextBroker(kwargs)
    driver = ClusterDriver(kwargs)
    id = kwargs.get("id")
    cluster = Cluster(id, driver)
    cluster_spec = kwargs.get("cluster_spec")
    cluster.create(cluster_spec)


def main():
    config = getconfig("nimboss.conf")
    opts = get_opts()
    getlogging(config, opts)
    kwargs = config + args
    return start_cluster(kwargs)

if __name__ == "__main__":
    main()
