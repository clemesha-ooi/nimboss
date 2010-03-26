"""
This file/logic will be eventually accessed
from another module, possible outside of the
nimboss package.


"""

#from nimbus.rest import Connection
from cpe_demo_code import UsefulThings

Connection = UsefulThings.Connection #lol


class ContextBroker(object):

    def __init__(self, uri):
        self.uri = uri
        self.connection = Connection(uri)

    def create_new_context(self, cluster_uuid, path="context"):
        resource = self.uri + path
        data = cluster_uuid #XXX more data is probably needed
        resp = self.connection.call(resource, data)
        return resp

    def query(self, cluster_uuid, path="state")
        resource = self.uri + "/" + path
        resp = self.connection.call(resoucre)
        return resp

