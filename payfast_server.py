################################################################################

# make accounts for randomly selected names

# load module
import random
# load datetime module to get current time
import datetime
# load uuid module to generate random password
import uuid
# to print data as table format 
from tabulate import tabulate

# get from user how man names to select
n_names=int(float(input('Enter number of random accounts to generate: ')))
# get initial amount in each account
init_amount=float(input('Enter initial amount in each account: '))
    
# read names text file
with open('names.txt',mode='r') as names_file:
    # read all lines in this file
    names=names_file.readlines()
    
# make random selection 
names=random.sample(names,n_names)
# clean name (remove '\n' from each name
names=[name.replace('\n','') for name in names]
# make random account numbers between 10**5 to 10**6
account_numbers=random.sample(range(10**5,10**6),n_names)
# convert each account number to string and make all lengths equal to nine
account_numbers=[str(account).zfill(9) for account in account_numbers]
# generate random password for each account
passwords=[str(uuid.uuid4()).replace('-','') for name in names]

# make ledger for each account number
ledger=list()

# add first transaction for each account
for name in names:
    # add first transaction
    ledger.append([[str(datetime.datetime.now()),'opening-balance',init_amount,
                    None,init_amount]])

# make file for each user with their names, account number and password
for name,password,account in zip(names,passwords,account_numbers):
    # create text file with name as account number
    with open(account+'.txt','w+') as account_info_file:
        # make print all information of account to this text file
        print('Account number:',account,file=account_info_file)
        print('Name:',name,file=account_info_file)
        print('Password:',password,file=account_info_file)

        
# function to check password and make transaction
def make_transaction(sender_account_number,recipient_account_number,
                     amount_2_send,sender_password):
    # convert amount to send to float
    amount_2_send=abs(float(amount_2_send))
    # check sender account number is valid or not
    if sender_account_number not in account_numbers:
        return 'error:sender_account_number_not_found'
    # check recipient account number is valid or not
    if recipient_account_number not in account_numbers:
        return 'error:recipient_account_number_not_found'
    # get sender account index
    sender_index=account_numbers.index(sender_account_number)
    # check password is valid or not
    if sender_password!=passwords[sender_index]:
        return 'error:invalid_password'
    # get balance in account and checl it should be greater than amount to send
    sender_balance=ledger[sender_index][-1][-1]
    # check
    if sender_balance>=amount_2_send:
        # make transaction and update ledger - sender 
        ledger[sender_index].append([str(datetime.datetime.now()),f'trx_to_{recipient_account_number}',
                                     None,amount_2_send,sender_balance-amount_2_send])
        # get recipient index
        recipient_index=account_numbers.index(recipient_account_number)
        # get recipient balance
        recipient_balance=ledger[recipient_index][-1][-1]
        # make transaction and update ledger - recipient
        ledger[recipient_index].append([str(datetime.datetime.now()),f'trx_from_{sender_account_number}',
                                        amount_2_send,None,recipient_balance+amount_2_send])
        # return that transaction had done
        return True
    # else if balance is less than ammount to send
    else:
        return 'error:insufficient_balance'


# make function to print account ledger
def print_ledger(account_number,password):
    # check sender account number is valid or not
    if account_number not in account_numbers:
        return 'error:account_number_not_found'
    # get sender account index
    account_index=account_numbers.index(account_number)
    # check password is valid or not
    if password!=passwords[account_index]:
        return 'error:invalid_password'
    # make text file with name of account holder
    with open(f'{account_number}_ledger.txt','w+') as ledger_file:
        # make print ledger
        print(tabulate(ledger[account_index],headers=['date','info','debits (dr)','credits (cr)','balance'],
                       tablefmt="rst"),file=ledger_file)
    # make return done
    return True

# make a function to check balance in account
def check_balance(account_number,password):
    # check sender account number is valid or not
    if account_number not in account_numbers:
        return 'error:account_number_not_found'
    # get sender account index
    account_index=account_numbers.index(account_number)
    # check password is valid or not
    if password!=passwords[account_index]:
        return 'error:invalid_password'
    # make retrun the balance
    return ledger[account_index][-1][-1]
    
    
###########################################################################################################

# load socket module
import socket
# load Thread class
from threading import Thread

# get host and ports from user
host_name=input('Enter host name: ')
# get list of ports 
ports=input('Enter ports name (seprated by ","): ')
# seprate and convert port to integer number
ports=[int(float(port)) for port in ports.split(',')]
# make list of server sockets
server_sockets=list()

# make socket and bind for connection
for port in ports:
    # make socket
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # binding port and host with socket
    server_socket.bind((host_name,port))
    # start socket listen
    server_socket.listen(5)
    # add socket to socket list
    server_sockets.append(server_socket)

# add info that connected 
print(f'Connect to host "{host_name}" at ports "{ports}".')
print('Press "ctrl+break" or "ctrl + F6" (if this not work then "ctrl + Fn + F6" to stop server.')

# make client thread class to read data from client
class client_thread(Thread):

    # make constructor
    def __init__(self,client_socket,client_address):
        # make call Thread class (parent)
        Thread.__init__(self)
        # make add socket of client
        self.scoket=client_socket
        # add client address
        self.address=client_address      
        # start thread
        self.start()


    # define run / thread function
    def run(self):
        # run function till data is recived
        while True:
            # get data from client
            message=self.scoket.recv(1024).decode()
            # check if there is a message (non-empty string)
            if message:
                # make info
                print(f'Recived request from {self.address}')
                # make split message
                message=message.split('|')
                # check and get function name
                # if make_transaction function is called
                if message[0]=='make_transaction':
                    message_to_return=make_transaction(*message[1:])
                    # if return is true (transcation is done)
                    if message_to_return==True:
                        message_to_return=f'transaction_done_from_{message[1]}_to_{message[2]}_of_{message[3]}'
                # if print_ledger function is called
                elif message[0]=='print_ledger':
                    message_to_return=print_ledger(*message[1:])
                    # if return is true (ledger has printed is done)
                    if message_to_return==True:
                        message_to_return='ledger_has_printed'
                # if print_ledger function is called
                elif message[0]=='check_balance':
                    message_to_return=check_balance(*message[1:])
                # else
                else :
                    message_to_return='error:invalid_request'
                # make send message to client
                self.scoket.send(str(message_to_return).encode())
                # make message print at server  
                print(message_to_return)
            # if it is  message
            else :
                # make loop end 
                break


# condition for loop
condition=True
# make infinit loop
while condition:
    try:
        # make data accept from sender / client
        for server_scoket in server_sockets:
            # make accept all
            client_socket,client_address=server_scoket.accept()
            # make forword to client thread
            client_thread(client_socket,client_address)
    # if their is keyborad Interrupt - make loop stop 
    except KeyboardInterrupt:
        # make infinit loop end
        condition=False
        
# make all socket close
[server_socket.close() for server_socket in server_sockets]
