# CSC 249 – Project 2 – ATM client with multi-client back-end banking server status report
By Feiran Chang and Liangnuo Zhang  

## (a) which of the P2 design requirements you believe you have satisfied

- server  
Our bank server could work well now. It can connect to multiple clients and manipulate messages from clients: It allows sending and receiving multiple messages; validate account number and pin.

- client
The client also works well. It could manipulate atm work including sending message to server, log into account and manage transaction through keyboard interaction. 

- and also Message Specification Document in ABNF finished

(b) the top 3 most significant knowledge or understanding gaps that are standing in your way 
we haven't revise our code to accept real IP addresses instead of the loopback address


(c) any thoughts you have about what you might do to overcome those gaps 
learn about real IP and change it
