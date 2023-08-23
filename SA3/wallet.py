from web3 import Web3
import time

ganacheUrl = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganacheUrl))

class Account():
    def __init__(self):
        self.account = web3.eth.account.create()
        self.address = self.account.address
        self.privateKey = self.account.key.hex()
        print("privatekey", self.privateKey)

class Wallet():
    def checkConnection(self):
        if web3.is_connected():
           return True
        else:
            return False
        
    def getBalance(self, address):
        balance = web3.eth.get_balance(address)
        return web3.from_wei(balance, 'ether')
    
    def makeTransactions(self, senderAddress, receiverAddress, amount, senderType, privateKey = None):
        web3.eth.defaultAccount = senderAddress

        if(senderType == 'ganache'):
            tnxHash = web3.eth.send_transaction({
                "from": senderAddress,
                "to": receiverAddress,
                "value": web3.to_wei(amount, "ether")  
                })
        else:
            transaction = {
                "to": receiverAddress,
                "value": web3.to_wei(amount, "ether"),
                "nonce": web3.eth.get_transaction_count(senderAddress), 
                "gasPrice": web3.to_wei(10, 'gwei'),
                "gas": 21000 
            }

            signedTx = web3.eth.account.sign_transaction(transaction, privateKey)
            tnxHash = web3.eth.send_raw_transaction(signedTx.rawTransaction)

    # Define getTransactions() method that takes current user address as address
    def getTransactions(self, address):
        # Use web3.eth.block_number to get latest block number and store it in latestBlockNumber
        latestBlockNumber = web3.eth.block_number
        # Create an empty list allBlockTransactionHashes
        allBlockTransactionHashes = []
        # Run a for loop from latestBlockNumber to 0 index 
        for i in range(latestBlockNumber, 0, -1):
            # Use web3.eth.get_block(i) to get a block and store the block in BlockData variable
            blockData = web3.eth.get_block(i)
            # Run loop for each tnxHash in transactions of blockData i.e blockData["transactions"]
            for tnxHash in blockData["transactions"]:
                # Add tnxHash.hex() of each transaction in allBlockTransactionHashes
                allBlockTransactionHashes.append(tnxHash.hex())
                
        # Create and empty list accountTransactions
        accountTransactions =[]

        # Run loop for each tnxHash in allBlockTransactionHashes
        for tnxHash in allBlockTransactionHashes:
            # Use web3.eth.get_transaction(tnxHash) to get the transaction data and store it in transaction variable
            transaction = web3.eth.get_transaction(tnxHash)
            # Check if transaction["from"] == address or transaction["to"] == address
            if(transaction["from"] == address or transaction["to"] == address):
                # Set tnxType variable to 'Received'
                tnxType = 'Received'
                # Check if transaction["from"] == address
                if(transaction["from"] == address):
                    # Set tnxType tp 'Sent'
                    tnxType = "Sent"
                # Append a dict containing "from", "to", "value", "tnxHash", 'tnxType' to accountTransactions
                accountTransactions.append({
                    "from": transaction["from"],
                    "to" : transaction["to"],
                    "value": web3.from_wei(transaction["value"], "ether"),
                    "tnxHash" : transaction["hash"].hex(),
                    'tnxType' : tnxType
                })
        # Return accountTransactions
        return accountTransactions 
    