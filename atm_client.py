#!/usr/bin/env python3
#
# Automated Teller Machine (ATM) client application.

## 1 -> reject
## 0 -> accept

import socket
import selectors

HOST = "127.0.0.1"      # The bank server's IP address
PORT = 65432            # The port used by the bank server

##########################################################
#                                                        #
# ATM Client Network Operations                          #
#                                                        #
# NEEDS REVIEW. Changes may be needed in this section.   #
#                                                        #
##########################################################
def configure_selectors(sock):
    sock.setblocking(False)
    sel = selectors.DefaultSelector()
    events = selectors.EVENT_WRITE | selectors.EVENT_READ
    data = {}
    sel.register(sock, events, data=data)
    return sel

def send_to_server(sel, msg):
    """ Given an open socket connection (sock) and a string msg, send the string to the server. """
    for key, mask in sel.select():
        sock = key.fileobj
        if mask & selectors.EVENT_WRITE:
            print("Sending " + msg + " to the server...")
            return sock.sendall(msg.encode('utf-8'))
        
        else:
            print("It is not ready to send massage")
            return False

def get_from_server(sel):
    """ Attempt to receive a message from the active connection. Block until message is received. """
    while True:
        for key, mask in sel.select():
            sock = key.fileobj
            if mask & selectors.EVENT_READ:
                msg = sock.recv(1024)
                if msg:
                    return msg.decode("utf-8")


def login_to_server(sel, acct_num, pin):
    """ Attempt to login to the bank server. Pass acct_num and pin, get response, parse and check whether login was successful. """
    validated = 1
    send_to_server(sel, acct_num)
    msg = get_from_server(sel)
    if msg == "0":
        send_to_server(sel,pin)
        msg = get_from_server(sel)
        if msg == "0":
            validated = 0
    if msg == "-2":
        validated = -2
    return validated

def get_login_info():
    """ Get info from customer. Validate inputs, ask again if given invalid input. """
    acct_num = input("Please enter your account number: ")
    if isinstance(acct_num, str) and \
    len(acct_num) == 8 and \
    acct_num[2] == '-' and \
    acct_num[:2].isalpha() and \
    acct_num[3:8].isdigit():
        pin = input("Please enter your four digit PIN: ")
        if (isinstance(pin, str) and \
        len(pin) == 4 and \
        pin.isdigit()):   
            return acct_num, pin
        else:
            print("The PIN format is invalid")
    else:
        print("The account number is in invalid format")
    return "", ""

def process_deposit(sel, acct_num):
    """ Write this code. """
    amt = input()
    # communicate with the server to request the deposit, check response for success or failure.
    send_to_server(sel, "d" + amt)
    valid = get_from_server(sel)
    if valid == "0":
        print("Deposit transaction completed.")
        bal = get_acct_balance(sel, acct_num)
        print("Your new balance is "+ bal)
    else:
        print("Invalid amount")
    return

def get_acct_balance(sel, acct_num):
    """ Ask the server for current account balance. """
    send_to_server(sel, "b")
    bal = get_from_server(sel)
    # code needed here, to get balance from server then return it
    return bal

def process_withdrawal(sel, bal, acct_num):
    """ Write this code. """
    amt = input()
    #  communicate with the server to request the withdrawal, check response for success or failure.
    if amt>bal:
        print("The amount to withdraw is more than your balance")
        return 
    send_to_server(sel, "w" + amt)
    valid = get_from_server(sel)
    if valid == "0":
        print("Withdrawal transaction completed.")
        bal = get_acct_balance(sel, acct_num)
        print("Your new balance is " + bal)
    elif valid == "111":
        print("Invalid amount")
    else:
        print("Account overdraft")
    return

def process_customer_transactions(sel, acct_num):
    """ Ask customer for a transaction, communicate with server. Revise as needed. """
    while True:
        bal = get_acct_balance(sel, acct_num)
        print("Select a transaction. Enter 'd' to deposit, 'w' to withdraw, or 'x' to exit.")
        req = input("Your choice? ").lower()
        if req not in ('d', 'w', 'x'):
            print("Unrecognized choice, please try again.")
            continue
        if req == 'x':
            # if customer wants to exit, break out of the loop
            break
        elif req == 'd':
            print(f"How much would you like to deposit? (You have ${bal} available)")
            process_deposit(sel, acct_num)
        else:
            print(f"How much would you like to withdraw? (You have ${bal} available)")
            process_withdrawal(sel, bal, acct_num)

def run_atm_core_loop(sock):
    sel = configure_selectors(sock)
    """ Given an active network connection to the bank server, run the core business loop. """
    login_check = False
    acct_num, pin = get_login_info()
    if acct_num != "" and pin != "":
        login_check = True
    if login_check:
        validated = login_to_server(sel, acct_num, pin)
        if validated == 0:
            print("Thank you, your credentials have been validated.")
        elif validated == -2:
            sock.close()
            print("The account is in use! Terminating ATM session")
            return False
        else:
            sock.close()
            print("Account number and PIN do not match. Terminating ATM session.")
            return False
        process_customer_transactions(sel, acct_num)
        sock.close()
        print("ATM session terminating.")
        return True
    else:
        sock.close()
        print("ATM session terminating.")

##########################################################
#                                                        #
# ATM Client Startup Operations                          #
#                                                        #
# No changes needed in this section.                     #
#                                                        #
##########################################################

def run_network_client():
    """ This function connects the client to the server and runs the main loop. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            run_atm_core_loop(s)
    except Exception as e:
        print(f"Unable to connect to the banking server - exiting...")

if __name__ == "__main__":
    print("Welcome to the ACME ATM Client, where customer satisfaction is our goal!")
    run_network_client()
    print("Thanks for banking with us! Come again soon!!")