import socket
import base64
import time

# SMTP Server Details
Server_IP = 'asmtp.htwg-konstanz.de'
Server_PORT = 587
username = "rnetin"
password = "PasswortderRNVorlesunganderHTWG"

# Encode credentials
encoded_username = base64.b64encode(username.encode()).decode()
encoded_password = base64.b64encode(password.encode()).decode()

# Email details
from_address = "de391bol@htwg-konstanz.de"
to_address = "robin.stockinger@gmx.de"
subject = "Subject: Test Email from Python\n"
message = "This is a test email sent from a Python script."

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
print('Connecting to SMTP server', Server_IP, 'on Port', Server_PORT)

# Connect to the server
sock.connect((Server_IP, Server_PORT))
response = sock.recv(1024)  # Server response

# Send EHLO command
sock.send(b'EHLO localhost\n')
response = sock.recv(1024)

# Authenticate
sock.send(b'AUTH LOGIN\n')
response = sock.recv(1024)
print(response.decode())
sock.send((encoded_username + "\n").encode())
response = sock.recv(1024)
print(response.decode())
sock.send((encoded_password + "\n").encode())
response = sock.recv(1024)
print(response.decode())

# Send MAIL FROM command
sock.send(("MAIL FROM: " + from_address + "\n").encode())
response = sock.recv(1024)
print(response.decode())

# Send RCPT TO command
sock.send(("RCPT TO: " + to_address + "\n").encode())
response = sock.recv(1024)
print(response.decode())

# Send DATA command
sock.send(b'DATA\n')
response = sock.recv(1024)
print(response.decode())

# Send email content
sock.send((subject + message + "\r\n.\r\n").encode())
response = sock.recv(1024)
print(response.decode())

# Quit
sock.send(b'QUIT\n')
response = sock.recv(1024)
print(response.decode())

sock.close()
