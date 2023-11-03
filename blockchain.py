# load hashlib module
import hashlib
# load datetime
import datetime
#load time(to get current time_)
import time
#load thread to make block generation auto
from threading import Thread

# make blockchain class
class blockchain(object):


    # make class constructor
    def __init__(self,difficulty:int=5,node:str='loaclhost:5000',gas_price:float=1E-9,
                 gas_limit:int=1E9,coin_alpha:int=1E-6,mining_reward:float=2.0,
                 genrate_block_after:int=60,blockchain_name='arc_coins'):

        # define difficulty
        self.difficulty=difficulty
        # add node
        self.node=node
        # gas price
        self.gas_price=gas_price
        # gas limit - maximum amount of gas given to a transaction
        self.gas_limit=gas_limit
        # minimum amount of crypto can transfer
        self.coin_alpha=coin_alpha
        #add mining rewards
        self.mining_reward=mining_reward
        #add block genration time(after this interval new blockis generate in sec
        self.genrate_block_after=genrate_block_after
        #add blockchain name
        self.blockchain_name=blockchain_name

        # make chain
        self.chain=list()
        #last mined block index
        self.LMB=0
        # define mined transaction
        self.mined_transactions=list()
        # define unmined transaction
        self.unmined_transactions=list()
        # add first block / Gensis Block
        self.__add_block()
        #make run thread to auto generate a block
        self.__block_generatin_thread=Thread(target=self.__add_block_auto)
        # make block generation thread daemon
        self.__block_generatin_thread.setDaemon(True)
        #make this thread function run
        self.__block_generatin_thread.start()
        

    # add __str__function to print chain when object called
    def __str__(self):
        #make return chain as string
        return str(self.chain)
    
    # define a function to add a block
    def __add_block(self):

        # get block number
        block_number=len(self.chain)+1
        # set nonce value
        nonce=0
        # get all mined transaction
        data=self.mined_transactions.copy()
        # make mined transaction clear
        self.mined_transactions.clear()
        # make up a block (dictionary)
        block={'block_number':block_number,
               'nonce':nonce,
               'timestamp':None,
               'merkle_root':None,
               'data':data,
               'previous_hash':None}
        # make block add to chain
        self.chain.append(block)
         
    #add automatically the block
    def __add_block_auto(self):

        #make functionto run infinitly as thread
        while True:
            #make function sleep for blockgeneration time(time after which new block is generated)
            time.sleep(self.genrate_block_after)
            #make new block to block 
            self.__add_block()
        
    # function to send coins / to do transaction
    def make_transaction(self,reciver:str,amount:float,gas:float=2E4):


        # make transaction dictionary
        trx={'sender':self.node,
             'reciver':reciver,
             'coins':amount,
             'gas':gas}
        # add transaction to unmined transaction
        self.unmined_transactions.append(trx)
        # make return that transaction had done
        return f'done:transaction_{amount}_to_{reciver}.'


    # function to mine a transaction
    def mine_transaction(self,miner,minimum_gas:int=1E4):

        # check if that there is unmined transaction or not
        if self.unmined_transactions:
            # check / find transaction having gas more or equal to minimum gas give
            for unmined_transaction in self.unmined_transactions:
                # check if gas is more that given gas or not
                if unmined_transaction['gas']<minimum_gas:
                    pass
                # else if gas is more or equal to gas limit
                else:
                    unmined_transaction=self.unmined_transactions.pop(self.unmined_transactions.index(unmined_transaction))
                    # break loop
                    break
                # else - if not fouund any transaction having gas more than gas limit (run only if
                # above for loop run fully - (break noyt applied)
                #else: return f'warning:found_no_transaction_under_given_gas_limit_{minimum_gas}'
            # make transaction mined
            mined_transaction=miner.mine_transaction(unmined_transaction)
            # add this mined transaction to mined transactions list
            self.mined_transactions.append(mined_transaction)
            # make reward transfer to miner
            reward=miner.mine_transaction({'sender':f'mining-transaction-reward-{mined_transaction["sender"]}',
                                           'reciver':miner.node,
                                           'coins':unmined_transaction['gas']*self.gas_price,
                                           'gas':None})
            # make add reward to  mined transactions list
            self.mined_transactions.append(reward)
            # make return info of transaction mined
            return f'done:mined_tx_{mined_transaction["hash"]}'
        # if unmined transaction list is empty
        return 'warning:empty_unmined_transaction_list'


    # add function to mine a block
    def mine_block(self,miner):

        #check last mined block number should not be more than chain length
        if self.LMB>len(self.chain):
            #make again zero
            self.LMB=0
        #search for unmined block
        for block in self.chain[self.LMB:]:
            #Chech block is mined or not
            if 'hash' in block:
                #continue to next block mined block number
                self.LMB+=1
                #continue to next block as block is mined
                #continue
            #else we got the last mined block
            else:
                #make copy of block
                block=block.copy()
                #make loop end
                break
        #if there is no block to mined - else(this will run only if for loop not break, i.e. break is not called)
        else: return 'warning:no_block_to_mine'
        #check previous block is mined ot not or if it is a first block
        if block['block_number']==1:
            #update block parameters - get previous block hash
            block['previous_hash']='0'*len(hashlib.sha256('0'.encode()).hexdigest())
        # if previous block is not mined then we can call mining function restart to seach for unmined block
        elif 'hash' not in self.chain[block['block_number']-2]: #as block index start form 1 but list index are strat form 0 then we take 2 minus
            #make again last mined block to zero
            self.LMB=0
            #call agin this function
            self.mine_block(miner)
        else:

            #update block parameters - get previous block hash
            block['previous_hash']=self.chain[block['block_number']-2]['hash']


            
        #so block is mined ---
        #add miner reward to block
        block['data'].append(miner.mine_transaction({'sender':f'mining-reward-{self.blockchain_name}',
                                           'reciver':miner.node,
                                           'coins':self.mining_reward,
                                           'gas':None}))
        
            
        #get merkle root
        block['merkle_root']=self.__get_root_hash(block['data'],full_tree=False)
        #update time stamp
        block['timestamp']=datetime.datetime.now()
        # make block mine and over write orginal block (one step ahead as block
        #start form one and list index form zero
        self.chain[block['block_number']-1]=miner.mine_block(block,self.difficulty)
        #make info
        return f'done:block_mined_{block["block_number"]}_hash_{block["hash"]}'

    #to calculate root hash
    def __get_root_hash(self,transactions:list,full_tree:bool=True):

        #create tree (list of dictionary)
        tree=list()
        #make dictionary for getting hash of each transaction
        next_level_hash=dict()
        #tree (dictionary) - add all treansaction to tree
        for index,transaction in enumerate(transactions):
            #add hash of each transaction to tree (key as transaction index)
            next_level_hash[str(index)]=hashlib.sha256(str(transaction).encode()).hexdigest()
        #add all hashes to tree
        tree.append(next_level_hash.copy())
        #make next_level_hash clean
        next_level_hash.clear()
        #run infinite loop (until nubmer of hash genrated is one, i.e root hash)
        while True:
            #make empty dictionary for next level hash(combined hash of child nodes)
            #next_level_hash=dict()
            #if there is only one transaction or last add hash is only one(root hash)
            if len(tree[-1])==1:
                   #make loop brake
                   break
            #maek run loop
            #dict_index=0
            for index in range(0,len(tree[-1]),2):
                #calculate combine hash of two child node
                hashx=hashlib.sha256((''.join(list(tree[-1].values())[index:index+2])).encode()).hexdigest()
                #get index for this hash
                dict_index=''.join(list(tree[-1].keys())[index:index+2])

                #add to next level dictionay
                next_level_hash[str(dict_index)]=hashx
                #dict_index+=1

            #add all hashes to tree
            tree.append(next_level_hash.copy())
            #make next_level_hash clear
            next_level_hash.clear()


    
        # finally return the tree
        if full_tree:return tree
        # if want only last hash
        else: return list(tree[-1].values())[0]
 
        
