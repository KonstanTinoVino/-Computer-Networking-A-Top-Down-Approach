from socket import *
import ssl
import base64
import time

client_address = ('localhost', 1071)

email = input("Email:")
print("")
password = input("Password:")
print("")
rec = input("Rec Email:")


msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.mail.com", 465)
server_address = "smtp.mail.com"

# Create socket called clientSocket and establish a TCP connection with mailserver
sock = socket(AF_INET, SOCK_STREAM)
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
clientSocket = context.wrap_socket(sock, server_hostname=server_address)

clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)

print(recv)
print(recv[:3])

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELLO command and print server response.
helloCommand = 'EHLO Tino\r\n'

clientSocket.send(helloCommand.encode())

recv1 = clientSocket.recv(1024)

print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Authentication required for the mail.com server I'm using
command = 'AUTH LOGIN\r\n'
print('C: ' + command)
clientSocket.send(command.encode())
resp = clientSocket.recv(1024)
print(resp)

# Send username as Base64 encoded string
command = base64.b64encode(email.encode()) + '\r\n'.encode()
print(command)
clientSocket.send(command)
resp = clientSocket.recv(1024)
print(resp)

# Send password as Base64 encoded string
command = base64.b64encode(password.encode()) + '\r\n'.encode()
print(command)
clientSocket.send(command)
resp = clientSocket.recv(1024)
print(resp)

# Send MAIL FROM command and print server response.
# Fill in start
mail_command = "MAIL FROM: <" + email + ">\r\n"
print(mail_command)
clientSocket.send(mail_command.encode())
recv2 = clientSocket.recv(1024)

print(recv2)
# Fill in end
# Send RCPT TO command and print server response.
# Fill in start
RCPT_command = "RCPT TO: <" + rec + ">\r\n"
print(RCPT_command)
clientSocket.send(RCPT_command.encode())
recv3 = clientSocket.recv(1024)

print(recv3)
# Fill in end
# Send DATA command and print server response.
# Fill in start
DATA_command = "DATA\r\n"
clientSocket.send(DATA_command.encode())
recv4 = clientSocket.recv(1024)
print(recv4)
# Send message headers
# Gmail does not accept mail without headers to prevent spam
command = 'From: ' + "Tino" + ' <' + email + '>' + '\r\n'
print(command)
clientSocket.send(command.encode())
command = 'To: ' + rec + '\r\n'
print(command)
clientSocket.send(command.encode())
command = 'Date: ' + time.asctime(time.localtime(time.time())) + '\r\n'
print(command)
clientSocket.send(command.encode())
command = 'Subject: ' + "Test Mail" + '\r\n'
print(command)
clientSocket.send(command.encode())

# Fill in end
# Send message data.
# Fill in start
msg = "What's Up"
clientSocket.send(msg.encode())
# Fill in end
# Message ends with a single period.
# Fill in start
endmsg = "\r\n.\r\n"
print('C: ' + endmsg)
clientSocket.send(endmsg.encode())
# Fill in end
# Send QUIT command and get server response.
# Fill in start
quitCommand = 'QUIT\r\n'
print('C: ' + quitCommand)
clientSocket.send(quitCommand.encode())
resp = clientSocket.recv(1024)
print(resp)
# Fill in end
