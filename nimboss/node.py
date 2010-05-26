import urllib
import base64
import hmac
from hashlib import sha256
from libcloud.drivers.ec2 import EC2Connection, EC2NodeDriver

class NimbusConnection(EC2Connection):

    host = ''
    port = (80, 8444)
    secure = 1

    post_actions = ('RunInstances')
    """A set of actions which should use HTTP POST. Hackity hack hack."""

    def _get_aws_auth_param(self, params, secret_key, path='/'):
        """
        Creates the signature required for AWS, per
        http://bit.ly/aR7GaQ [docs.amazonwebservices.com]

        This method is copied from
        libcloud.drivers.ec2.EC2Connection._get_aws_auth_param and modified
        to use POST for specific Actions
        """
        keys = params.keys()
        keys.sort()
        pairs = []
        httpVerb = 'GET'
        for key in keys:
            pairs.append(urllib.quote(key, safe='') + '=' +
                         urllib.quote(params[key], safe='-_~'))
            if key == 'Action' and params[key] in self.post_actions:
                httpVerb = 'POST'

        qs = '&'.join(pairs)
        string_to_sign = '\n'.join((httpVerb, self.host, path, qs))

        b64_hmac = base64.b64encode(
            hmac.new(secret_key, string_to_sign, digestmod=sha256).digest()
        )
        return b64_hmac

    def request(self, action, params=None, data='', headers=None, method='GET'):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        # Extend default parameters
        params = self.add_default_params(params)
        # Extend default headers
        headers = self.add_default_headers(headers)
        # HACK: Some actions are actually HTTP POST
        if 'Action' in params and params['Action'] in self.post_actions:
            method = 'POST'
            data = urllib.urlencode(params)
            params = {}
            headers.update({'Content-Type':
                'application/x-www-form-urlencoded; charset=UTF-8'})
        # We always send a content length and user-agent header
        headers.update({'Content-Length': len(data)})
        headers.update({'User-Agent': self._user_agent()})
        headers.update({'Host': self.host})
        # Encode data if necessary
        if data != '':
            data = self.encode_data(data)
        url = '?'.join((action, urllib.urlencode(params)))
        # Removed terrible hack...this a less-bad hack that doesn't execute a
        # request twice, but it's still a hack.
        self.connect()
        self.connection.request(method=method, url=url, body=data,
                headers=headers)
        response = self.responseCls(self.connection.getresponse())
        response.connection = self
        return response

class NimbusNodeDriver(EC2NodeDriver):

    connectionCls = NimbusConnection
    name = "Nimbus"

    def _fixxpath(self, xpath):
        # Nimbus return types don't include namespace declaration in every
        # tag, unlike EC2. So we override this method to make xpath queries
        # just pass through instead of being ns-prefixed.
        return xpath
