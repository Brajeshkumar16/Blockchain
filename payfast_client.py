# load socket module
import socket
# load Thread class
from threading import Thread
# load getpass to get password from user
import getpass

# get host and ports from user
host_name=input('Enter host name: ')
# get list of ports 
port=int(float(input('Enter port name: ')))


# make socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# connect port and host with socket
client_socket.connect((host_name,port))

# make info
print(f'Connect to host "{host_name}" at port "{port}".')
print('Wellcome to payfast client!')
print('Press "ctrl+break" or "ctrl + F6" (if this not work then "ctrl + Fn + F6" to end client.')

# make user interface - infinite loop
while True:
    # make user choice
    print('1. Make transaction.')
    print('2. Print ledger.')
    print('3. Check balance.')
    # get user choice
    choice=input('Enter your choice [1, 2 or 3]: ')
    # if user want to make transaction
    if choice=='1':
        # get account number from user - sender 
        sender_account=input('Enter sender account number: ')
        # get recipient account number
        recipient_account=input('Enter recipient account number: ')
        # get amount to send
        try:
            amount=float(input('Enter amount to transfer: '))
        # except error
        except ValueError:
            print('Invalid amount!')
            # re-run loop 
            continue
        # get user password
        password=getpass.getpass(prompt='Enter sender password: ')
        # send request to server
        message=f'make_transaction|{sender_account}|{recipient_account}|{amount}|{password}'
    # if user want to print ledger
    elif choice=='2':
        # get account number from user
        account=input('Enter account number which passbook to generate: ')
        # get user password
        password=getpass.getpass(prompt='Enter account password: ')
        # make message to send request to server
        message=f'print_ledger|{account}|{password}'
    # if user want to get blalance in its account
    elif choice=='3':
        # get account number from user
        account=input('Enter account number which balance to check: ')
        # get user password
        password=getpass.getpass(prompt='Enter account password: ')
        # make message to send request to server
        message=f'check_balance|{account}|{password}'
    # else if request is invalid
    else:
        print('Invalid request! Enter on of 1, 2 or 3')
        # make loop re-run
        continue 
    # make info - sending request to server
    print('Sending request to server and waiting for reply ......')
    # send request to server
    client_socket.send(message.encode())
    # waiting for reply
    message=client_socket.recv(1024).decode()
    # make print message
    print(f'Server reply - "{message}"')
