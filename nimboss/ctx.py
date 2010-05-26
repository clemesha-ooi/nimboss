import httplib2 # Not in standard library, change later if needed.
import httplib # for status codes

try: 
    import json
except: 
    import simplejson as json

Connection = httplib2.Http

class ContextClient(object):
    """Broker connection management and utility functionality.

    """

    def __init__(self, broker_uri, key, secret):
        self.broker_uri = broker_uri
        self.connection = Connection()
        self.connection.add_credentials(key, secret)

    def create_context(self):
        """Create a new context with Broker.

        @return: instance of type C{ContextResource}
        """

        # creating a new context is a POST to the base broker URI
        # context URI is returned in Location header and info for VMs
        # is returned in body
        (resp, body) = self.connection.request(self.broker_uri, 'POST')
        if resp.status != httplib.CREATED:
            raise BrokerError("Failed to create new context")
        
        location = resp['location']
        body = json.loads(body)

        return ContextResource(location, body)

    def get_status(self, resource):
        """Status of a Context resource.

        Returns a dict full of status information. 
        But soon it will be a type?
        """
        
        (resp, body) = self.connection.request(str(resource), 'GET')
        if resp.status != httplib.OK:
            raise BrokerError("Failed to get status of context")
        return json.loads(body)

class ContextResource(dict):
    """Context created on the broker. 

    Used in generation of userdata.
    Needs a better name?
    """
    def __init__(self, uri, body):
        for key, value in body.iteritems():
            self[key] = value
        self.uri = str(uri)
        self.broker_uri = self['brokerUri']
        self.context_id = self['contextId']
        self.secret = self['secret']
    def __str__(self):
        return self.uri

class BrokerError(Exception):
    """Error response from Context Broker.
    """
    def __init(self, reason):
        self.reason = reason
        Exception.__init__(self, reason)

