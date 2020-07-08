import json
import requests

class TendermintRPC:

    def __init(self, node_url):
        self.node_url = node_url

    def get_block_height(self):
        try:
            response = requests.get(self.node_url+ '/abci_info?')
            response.raise_for_status()
            data = response.json()
            return data['result']['response']['last_block_height']
        except Exception as err:
            print(f'An error occured retrieving the latest block height: {err}')

    def get_block(self, height):
        try:
            response = requests.get(self.node_url + '/block?height=' + str(height))
            response.raise_for_status()
            data = response.json()
            block = self.init_block(data['result'])

            block_results = self.get_block_results(height)
            
            # Capture transactions and underlying events
            block_transactions = self.get_transactions_by_block(height)
            if block_transactions['txs']:
                for tx in block_transactions['txs']:
                    block_tx = self.get_transactions_by_hash(tx['hash'])
                    block.add_transaction(block_tx)
            
            # Capture begin block events ()
            if block_results['results']['begin_block']:
                for event in block_results['results']['begin_block']['events']:
                    block.begin_block.append(event)
            
            block.end_block = block_results['results']['end_block']

            block_validators = self.get_block_validators(height)
            for validator in block_validators['validators']:
                block.validators.append(validator)

            return block
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

    # Need ANKR to turn on indexing at node level for this call to work properly
    def get_transactions_by_block(self, height):
        try:
            response = requests.get(self.node_url + '/tx_search?query=\"tx.height=' + str(height) + '\"&prove=true')
            response.raise_for_status()
            data = response.json()
            return data['result']
        except Exception as err:
            print(f'An error occured retrieving the transactions in block: {err}')

    def get_transactions_by_hash(self, tx_hash):
        try:
            response = requests.get(self.node_url + '/tx?hash=' + tx_hash)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as err:
            print(f'An error occured retrieving the transaction by hash: {err}')

    # Currently returning the following response "Height must be less than or equal to the current blockchain height"
    def get_block_validators(self, height):
        try:
            response = requests.get(self.node_url + '/validators?height=' + str(height))
            response.raise_for_status()
            data = response.json()
            return data['result']
        except Exception as err:
            print(f'An error occured retrieving the validators for block height: {err}')