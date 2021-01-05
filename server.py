from datetime import datetime
from datetime import timedelta
from threading import Thread
import socket, pickle

# List of employers. in this exercise, We only have one employer. For multiple employers we need multiple employer threads,
# which is easy with our paradigm
employer_list = []

# List of customers.
customer_list = []

# employer_list.append({'id': len(employer_list) + 1})
# employer_list.append({'id': len(employer_list) + 1})
# print(employer_list)

# customer_list.append({'id': len(employer_list) + 1, 'time' : (datetime.now() + timedelta(minutes=3)).strftime('%H:%M') })
# customer_list.append({'id': len(employer_list) + 1, 'time' : (datetime.now() + timedelta(minutes=3)).strftime('%H:%M') })
# print(customer_list)

def customer_thread():
    try:
        # establish a socket for tcp protocol, under ipv4
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Customer socket successfully created")
    except socket.error as err:
        print("Socket creation failed with error %s" %(err))

    # Customer port
    port = 9192
    # Get the host ip
    host = socket.gethostname()
    # Bind the socket to host and port
    s.bind((host, port))
    print ("Customer socket binded to %s" %(port))

    s.listen(5)
    print ("Customer socket is listening")

    # Waiting to accept a connection
    c, addr = s.accept()
    print ('Got connection from', addr, ' for customer thread' )

    while True:

        # data received from client
        data = c.recv(1024)
        data_variable = pickle.loads(data)
        print('Message to', data_variable, 'from customer requesting ticket')
        # assign a customer
        if not data:
            print('Bye')
            break

        # If the request header data is 'bankClient'm then add a ticket for the customer
        if data_variable == 'bankClient':
            dic_to_add = {'id': 1000 + len(customer_list), 'time': (datetime.now() + timedelta(minutes=3*len(customer_list))).strftime('%H:%M')}
            # Append the ticket to customer_list
            customer_list.append(dic_to_add)
            # Send the ticket to customer machine
            ticket_msg = f'this is your ticket: {dic_to_add}'
            assign_var = pickle.dumps(ticket_msg)
            c.send(assign_var)

    # connection closed
    c.close()


def employer_thread():
    try:
        # establish a socket for TCP protocol under ipv4
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Employer socket successfully created")
    except socket.error as err:
        print("Socket creation failed with error %s" %(err))

    # Port for employer 1
    port = 9191
    # Get host ip
    host = socket.gethostname()
    # Bind the socket to host and port
    s.bind((host, port))
    print ("Employer socket binded to %s" %(port))

    # Listen for connections
    s.listen(5)
    print ("Employer socket is listening")

    # Wait to accept a connection from employer 1
    c, addr = s.accept()
    print ('Got connection from', addr, ' for employer thread' )

    while True:

        # data received from client
        data = c.recv(1024)
        data_variable = pickle.loads(data)
        print('Message from' , data_variable, ' calling a customer')
        if not data:
            print('Bye')
            break

        if data_variable == 'bankEmployer':
            # If ticket are more than 0, in customer_list, then dequeue the ticket
            if len(customer_list) > 0:
                chosen_customer = customer_list.pop(0)
                # Send the customer information to employer
                assign_msg = f'Customer {chosen_customer} is yours'
                assign_var = pickle.dumps(assign_msg)
                c.send(assign_var)
            # If no ticket is recieved by any customer, send 'No customers yet!' to employer
            else:
                assign_msg = 'No customers yet!'
                assign_var = pickle.dumps(assign_msg)
                c.send(assign_var)

    # connection closed
    c.close()

def main():
    # Start customer thread
    cThread = Thread(target = customer_thread)
    cThread.start()

    # Start employer thread
    eThread = Thread(target = employer_thread)
    eThread.start()

if __name__ == '__main__':
    main()


