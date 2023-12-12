import socket
import threading

# Global flag to control the threads
Continue = True

def scan_tcp_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect((ip, port))
        if Continue:
            print(f"TCP Port {port} is open")
    except:
        pass
    finally:
        sock.close()

def scan_udp_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(b"", (ip, port))
        sock.recvfrom(1024)
    except socket.timeout:
        if Continue:
            print(f"UDP Port {port} is open")
    except socket.error as e:
        if e.errno != 10054:
            if Continue:
                print(f"UDP Port {port} is open!")
    finally:
        sock.close()

def port_scanner(ip, start_port, end_port):
    for port in range(start_port, end_port+1):
        if Continue:
            tcp_thread = threading.Thread(target=scan_tcp_port, args=(ip, port))
            udp_thread = threading.Thread(target=scan_udp_port, args=(ip, port))
            tcp_thread.start()
            udp_thread.start()
        else:
            break

# Start the port scanner
port_scanner('141.37.168.26', 1, 50)