import socket
import struct
import time

def calculate(operation, numbers):
    if operation == "Summe":
        return sum(numbers)
    elif operation == "Produkt":
        result = 1
        for num in numbers:
            result *= num
        return result
    elif operation == "Minimum":
        return min(numbers)
    elif operation == "Maximum":
        return max(numbers)
    else:
        raise ValueError("Unbekannte Operation")

My_IP = '127.0.0.1'
My_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
sock.listen(1)
print(f'Listening on Port {My_PORT} for incoming TCP connections')

while True:
    try:
        conn, addr = sock.accept()
        print(f'Incoming connection accepted: {addr}')

        while True:
            data = conn.recv(1024)
            if not data:
                print('Connection closed from other side')
                conn.close()
                break

            # Unpack and calculate
            id, = struct.unpack('!I', data[:4])
            operation_len = data[4]
            operation = data[5:5 + operation_len].decode('utf-8')
            numbers = struct.unpack('!' + 'i' * ((len(data) - 5 - operation_len) // 4), data[5 + operation_len:])

            result = calculate(operation, numbers)
            response = struct.pack('!Ii', id, result)
            conn.send(response)

    except socket.timeout:
        print(f'Socket timed out at {time.asctime()}')

sock.close()
