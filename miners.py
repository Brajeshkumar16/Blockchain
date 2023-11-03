# load hashlib module
import hashlib
# load datetime
import datetime

# make miner class
class miner(object):

    # make class constructor
    def __init__(self,node='localhost:5050'):

        # set miner node
        self.node=node


    # make a function to mine a block
    def mine_block(self,block,difficulty):

        # make infinite loop 
        while True:
            # get hash of block
            hash_of_block=hashlib.sha256(str(block).encode()).hexdigest()
            # check hash is valid or not
            if hash_of_block[:difficulty]=='0'*difficulty:
                # valid hash found - add hash to block
                block['hash']=hash_of_block
                # break the infinit loop
                break
            # else - increase the value of nonce and find hash again 
            else: block['nonce']+=1
        # make return the block
        return block 
                
            
    # define a function to mine transaction
    def mine_transaction(self,transaction):

        # generate hash of transaction
        hash_of_transaction=hashlib.sha256(str(transaction).encode()).hexdigest()
        # add hash to transaction dictionary
        transaction['hash']=hash_of_transaction
        # make return transaction
        return transaction
        
