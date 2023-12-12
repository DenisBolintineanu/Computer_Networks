import socket
import struct

def pack_message(id, operation, numbers):
    operation_encoded = operation.encode('utf-8')
    numbers_format = '!' + 'i' * len(numbers)
    return struct.pack('!I', id) + struct.pack('!B', len(operation_encoded)) + operation_encoded + struct.pack(numbers_format, *numbers)

#Server_IP = '127.0.0.1'
#Server_PORT = 50000

Server_IP = '141.37.206.23'
Server_PORT = 50000


# Example message
id = 1
operation = "Product"  # Can be "Sum", "Product", "Minimum" or "Maximum"
numbers = [1, 2, 3, 4, 5]  # List of numbers

# Pack message
message = pack_message(id, operation, numbers)

# Establish connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind((Server_IP, 40000))
sock.connect((Server_IP, Server_PORT))
local_ip, local_port = sock.getsockname()
print(f'Local IP: {local_ip}, Local Port: {local_port}')


# Send message
sock.send(message) # Send message
print(f'Message sent: ID={id}, Operation={operation}, Numbers={numbers}')

# Receive response
data = sock.recv(1024) # Blocking call
received_id, result = struct.unpack('!Ii', data)
print(f'Response received: ID={received_id}, Result={result}')

sock.close()