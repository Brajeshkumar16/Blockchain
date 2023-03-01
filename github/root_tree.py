#load hashlib module
import hashlib

#hefine a function to generate hash tree (merkle tree)
def generate_tree(transactions:list):

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
    return tree
        
