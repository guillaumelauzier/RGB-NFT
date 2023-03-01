import os
import time
from binascii import hexlify
from rgb.schema import Schema
from rgb import AssetDefinitionManager, ContractManager, IssueMode
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Connect to the Bitcoin RPC interface
rpc_user = 'user'
rpc_password = 'password'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@localhost:{rpc_port}/')

# Define the new asset
asset_name = 'MyNFT'
asset_symbol = 'NFT'
asset_metadata = {'artist': 'John Smith', 'year': 2023, 'medium': 'Oil on canvas'}
asset_definition = {
    'name': asset_name,
    'ticker': asset_symbol,
    'supply': 1,
    'metadata': asset_metadata,
    'precision': 0
}

# Set up RGB
manager = AssetDefinitionManager()
manager.set_api_endpoint('http://localhost:5000')
manager.set_rpc_proxy(rpc_connection)
contract_manager = ContractManager()

# Register the new asset definition
schema = Schema.from_dict(asset_definition)
manager.register_asset_definition(schema)

# Issue the new asset
mode = IssueMode.ISSUE_ONCE
address = 'myaddress'
asset_id = hexlify(schema.hash().digest()).decode()
value = 1
fee = 1000
contract_manager.issue(
    mode, address, asset_id, value, fee, issuance_utxo=None, issuance_entropy=None
)

print(f'Asset {asset_name} issued.')
