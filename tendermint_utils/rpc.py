import json
import requests
class TendermintRPC:

    def __init__(self, node_url):
        self.node_url = node_url

    def get_block_height(self):
        try:
            response = requests.get(self.node_url+ '/abci_info?')
            data = response.json()
            return data['result']['response']['last_block_height']
        except Exception as err:
            print(f'An error occured retrieving the latest block height: {err}')

    def get_block(self, height):
        try:
            response = requests.get(self.node_url + '/block?height=' + str(height))
            data = response.json()
            return data['result']
        except Exception as err:
            print(f'An error occured retrieving block: {err}')

    def get_block_results(self, height):
        try:
            response = requests.get(self.node_url + '/block_results?height=' + str(height))
            response.raise_for_status()
            data = response.json()
            return data['result']
        except Exception as err:
            print(f'An error occured retrieving the results of block height: {err}')

    def get_transactions_by_block(self, height, limit=None, page=1):
        if limit is not None:
            response = requests.get(self.node_url + '/tx_search?query=\"tx.height=' + str(height) + '\"&prove=true&per_page=' + str(limit) + '&page=' + str(page))
        else:
            response = requests.get(self.node_url + '/tx_search?query=\"tx.height=' + str(height) + '\"&prove=true&page=' + str(page))
        data = response.json()
        return data['result']

    def get_transactions_by_hash(self, tx_hash, hex_prefix=False):
        try:
            if hex_prefix:
                tx_hash = '0x' + tx_hash
            response = requests.get(self.node_url + '/tx?hash=' + tx_hash)
            data = response.json()
            return data['result']
        except Exception as err:
            print(f'An error occured retrieving the transaction by hash: {err}')

    def get_block_validators(self, height):
        try:
            response = requests.get(self.node_url + '/validators?height=' + str(height))
            data = response.json()
            return data['result']
        except Exception as err:
            print(f'An error occured retrieving the validators for block height: {err}')
