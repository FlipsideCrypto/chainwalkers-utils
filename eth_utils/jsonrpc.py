import requests
import json
import base64
import time

class RpcCallFailedException(Exception):
    pass

class JsonRpcCaller(object):

    def __init__(self, node_url, user=None, password=None, tls=False, tlsVerify=False):
        self.url = node_url
        self.user = user
        self.password = password
        self.tls = tls
        self.tlsVerify = tlsVerify

    def _make_rpc_call(self, headers, payload, json):
        try:
            response = requests.post(
                self.url,
                headers=headers,
                data=payload,
                json=json,
                verify=(self.tls and self.tlsVerify)
            )
        except Exception as e:
            raise RpcCallFailedException(e)

        if response.status_code != 200:
            raise RpcCallFailedException("Invalid status code: %s" % response.status_code)

        responseJson = response.json(parse_float=lambda f: f)

        if type(responseJson) != list:
            if "error" in responseJson and responseJson["error"] is not None:
                raise RpcCallFailedException("RPC call error: %s" % responseJson["error"])
            else:
                return responseJson.get('result')
        else:
            result = []
            for subResult in responseJson:
                if "error" in subResult and subResult["error"] is not None:
                    raise RpcCallFailedException("RPC call error: %s" % subResult["error"])
                else:
                    result.append(subResult["result"])
            return result

    def call(self, method, params=None, query=None):
        if params is None:
            params = []
        headers = {'content-type': 'application/json'}
        payload = json.dumps({"jsonrpc": "2.0", "id": "0", "method": method, "params": params})
        if query: # GQL Hack
            return self._make_rpc_call(headers, payload=None, json={'query': query})
        return self._make_rpc_call(headers, payload, json=None)

    def bulk_call(self, methodParamsTuples):
        headers = {'content-type': 'application/json'}
        payload = json.dumps([{"jsonrpc": "2.0", "id": "0", "method": method, "params": params}
                              for method, params in methodParamsTuples])
        return self._make_rpc_call(headers, payload)