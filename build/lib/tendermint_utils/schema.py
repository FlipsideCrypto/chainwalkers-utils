class BlockSchema(object):

    def __init__(self, data):
        self.hash = data['block_meta']['hash']
        self.chain_id = data['block_meta']['header']['chain_id']
        self.height = data['block_meta']['header']['height']
        self.timestamp = data['block_meta']['header']['time']
        self.parts = data['block_meta']['block_id']['parts']
        self.num_txs = data['block_meta']['header']['num_txs']
        self.total_txs_onchain = data['block_meta']['header']['total_txs']
        self.parent_hash = data['block_meta']['header']['last_block_id']['hash']
        self.last_commit_hash = data['block_meta']['header']['last_commit_hash']
        self.data_hash = data['block_meta']['header']['data_hash']
        self.validators_hash = data['block_meta']['header']['validators_hash']
        self.next_validators_hash = data['block_meta']['header']['next_validators_hash']
        self.consensus_hash = data['block_meta']['header']['consensus_hash']
        self.app_hash = data['block_meta']['header']['app_hash']
        self.last_results_hash = data['block_meta']['header']['last_results_hash']
        self.evidence_hash = data['block_meta']['header']['evidence_hash']
        self.proposer_address = data['block_meta']['header']['proposer_address']
        self.encoded_txs = data['block']['data']['txs']
        self.evidence = data['block']['evidence']['evidence']
        self.transactions = []
        self.precommits = data['block']['last_commit']['precommits']
        self.validators =[]
        self.begin_block = []
        self.end_block = {}

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def __repr__(self):
        header = "block height: %d, tx count %d" % (int(self.height), len(self.transactions))
        transactions = []
        for tx in self.transactions:
            transactions.append(str(tx))
        return "\n".join([header] + transactions)
