import socket, pickle           # Import socket module

def main():
    # If any key is pressed, employer will connect to employer thread in server
    input("Are you ready (Press any key)? ")
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 9191                 # Reserve a port for your service.
    s.connect((host, port))

    while True:
        choice = input('Enter 0 to call next customer: ')
        if choice == '0':
            # If the employer asks for a customer, then a message is sent to server for dequeueing customer_list
            data_variable = pickle.dumps('bankEmployer')
            s.send(data_variable)
            # Recieve customer ticket information
            assign_recv = s.recv(1024)
            pickle_recv = pickle.loads(assign_recv)

            print(pickle_recv)

        else:
            print('Invalid input. try again!')
            continue

    s.close()



if __name__ == '__main__':
    main()

