import socket
import struct

def pack_message(id, operation, numbers):
    operation_encoded = operation.encode('utf-8')
    numbers_format = '!' + 'i' * len(numbers)
    return struct.pack('!I', id) + struct.pack('!B', len(operation_encoded)) + operation_encoded + struct.pack(numbers_format, *numbers)

Server_IP = '127.0.0.1'
Server_PORT = 50000

# Beispielnachricht
id = 1
operation = "Produkt"  # Kann "Summe", "Produkt", "Minimum" oder "Maximum" sein
numbers = [1, 2, 3, 4, 5]  # Liste der Zahlen

# Nachricht packen
message = pack_message(id, operation, numbers)

# Verbindung herstellen
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((Server_IP, Server_PORT))

# Nachricht senden
sock.send(message)
print(f'Nachricht gesendet: ID={id}, Operation={operation}, Zahlen={numbers}')

# Antwort empfangen
data = sock.recv(1024)
received_id, result = struct.unpack('!Ii', data)
print(f'Antwort erhalten: ID={received_id}, Ergebnis={result}')

sock.close()
