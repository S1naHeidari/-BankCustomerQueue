import socket, pickle           # Import socket module

def main():
    #input("Push the button to get your ticket")
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 9192                 # Reserve a port for your service.
    s.connect((host, port))

    while True:
        input('Push the button to get your ticket (Any key) ...')
        # Send a message to server to get a ticket for this customer
        data_variable = pickle.dumps('bankClient')
        s.send(data_variable)
        # Recieve ticket id and time
        assign_recv = s.recv(1024)
        ticket_recv = pickle.loads(assign_recv)
        print(ticket_recv)


    s.close()



if __name__ == '__main__':
    main()

