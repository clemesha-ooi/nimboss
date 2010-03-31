"""
This file/logic will be eventually accessed
from another module, possible outside of the
nimboss package.


"""

# using httplib2 for now even though it isn't in standard library.
# we can change this later if needed.
import httplib2 
import httplib # for status codes

try: import json
except: import simplejson as json

Connection = httplib2.Http

class BrokerClient(object):

    def __init__(self, broker_uri, key, secret):
        self.broker_uri = broker_uri
        self.connection = Connection()
        self.connection.add_credentials(key, secret)

    def create_context(self):
        """
        Creates a new context with broker.
        Returns (uri, context_info)
        """

        # creating a new context is a POST to the base broker URI
        # context URI is returned in Location header and info for VMs
        # is returned in body
        (resp, body) = self.connection.request('POST', self.broker_uri)
        if resp.status != httplib.CREATED:
            raise BrokerError("Failed to create new context")
        
        location = resp['location']
        body = json.loads(body)

        return ContextResource(location, body)

    def get_status(self, resource):
        """
        Checks the status of a context resource.
        Returns a dict full of status information. 
        But soon it will be a type?
        """
        
        (resp, body) = self.connection.request('GET', str(resource))
        if resp.status != httplib.OK:
            raise BrokerError("Failed to get status of context")
        return json.loads(body)

class ContextResource(dict):
    """
    A context created on the broker. Used in generation of userdata.
    Needs a better name?
    """
    def __init__(self, uri, body):
        for key, value in body.iteritems():
            self[key] = value
        self.uri = str(uri)
        self.broker_uri = self['broker_uri']
        self.context_id = self['context_id']
        self.secret = self['secret']
    def __str__(self):
        return self.uri
