#!/usr/bin/env python3
import sys
import os
import time

client_ip = '192.168.5.9'
port = '502'

keywords = ('back', 'clear', 'exit', 'help')

address_table = [(1, "0x01", "0x006B"),
                 (2, "0x02", "0x006C"),
                 (3, "0x03", "0x006D"),
                 (4, "0x04", "0x006E"),
                 (5, "0x05", "0x006F"),
                 (6, "0x06", "0x0070"),
                 (7, "0x07", "0x0071"),
                 (8, "0x08", "0x0072"),
                 (9, "0x09", "0x0073"),
                 (10,"0x0A", "0x0074")
]

func_codes_register = [
    (0x04, "Read", "Analog-Input-Registers"),
    (0x03, "Read", "Analog-Output-Holding-Registers"),
    (0x06, "Write-Single", "Analog-Output-Holding-Registers"),
    (0x10, "Write-Multiple", "Analog-Output-Holding-Registers")
]

func_codes_coil = [
    (0x02, "Read", "Discrete-Input-Contacts"),
    (0x01, "Read", "Discrete-Output-Coils"),
    (0x05, "Write-Single", "Discrete-Output-Coil"),
    (0x0F, "Write-Multiple", "Discrete-Output-Coils")
]

def parse_keywords(word):
    if word == 'back':
        main_menu()
    elif word == 'clear':
        clear_screen()
    elif word == 'exit':
        sys.exit()
    elif word == 'help':
        help_menu()
    else:
        print("Unknown Error")
        sys.exit()

def clear_screen():
    if os.name.startswith('posix'):
        os.system('clear')
    elif os.name.startswith('nt'):
        os.system('cls')

def keyboard_interrupt():
    print("\n\nExiting the program")
    sys.exit()

def initial_connection():
    clear_screen()
    print("Establishing Connection...")
    time.sleep(3)
    print("Connected\n")
    time.sleep(1)

def help_menu():
    clear_screen()
    print(("*" * 30) + "HELP MENU" + ("*" * 30) + "\n")
    print(" \tCommands:\tDescription:\n")
    print(" \tback\t\treturn to main menu")
    print(" \tclear\t\tclear screen")
    print(" \texit\t\tclose the program")
    print(" \thelp\t\tprint this help menu")
    print(" \trequest\t\tinitiate data request")
    print(" \twrite\t\tconnect to write interface")
    print("\n\n" + ("*" * 70) + "\n\n")

def server_manifest():
    clear_screen()
    while True:
        try:
            print("*" * 30, "ACTIVE UNITS", "*" * 30)
            print("\n", "ID\t", "FC\t", "LOCATION\n")
            
            for x,y,z in address_table:
                print(x,"\t", y, "\t", z, "\n")
            
            _choice = input("> ")
            
            if _choice in keywords:
                word = _choice
                parse_keywords(word)
            else:
                server_manifest()
        except KeyboardInterrupt:
            keyboard_interrupt()

def data_request():
    clear_screen()
    while True:
        try:
            print("*" * 30, "DATA REQUEST", "*" * 30)
            print("\nType 'request' to initiate request")
           
            _choice = input("\n> ")

            if _choice in keywords:
                word = _choice
                parse_keywords(word)
            elif _choice == "request":
                print("\nConnecting...")
                time.sleep(3)
                print("\nConnected: Unit Gateway\n")
                while True:
                    try:
                        print("*" * 10,"UNIT GATEWAY", "*" * 10)
                        print("\nPress 'ctl+c' to end request ")
                        print("\nUnitID - FunctionCode - DataRequest")
                        _id = input("\n(request:)> ")
                        for entry in address_table:
                            if int(_id) in entry:
                                print("\nSending Request...")
                                time.sleep(1)
                                print("\nWaiting for Response...")
                                time.sleep(2)
                                print("\nRead From Unit:",_id,"\n")
                                print(entry,"\n")
                    except KeyboardInterrupt:
                        data_request()
                    except ValueError:
                        print("Invalid Unit ID")
            else:
                data_request()
        except KeyboardInterrupt:   
            keyboard_interrupt()

def write_data():
    clear_screen()
    while True:
        try:
            print("*" * 30, "WRITE DATA", "*" * 30)
            print("\nType 'write' to connect to write interface")
            _choice = input("\n> ")
            if _choice in keywords:
                word = _choice
                parse_keywords(word)
            elif _choice == "write":
                print("Connecting to Interface...\n")
                time.sleep(3)
                while True:
                    try: 
                        print(("*" * 15) +  " WRITE INTERFACE " + ("*" * 15))
                        print("\nUsage: ID - FC - RegLoc")
                        print("\n'ctl-c' to close interface")
                        _id = int(input("\n(write)> "))
                        print("\nWriting to Unit...")
                        time.sleep(3)
                        for entry in address_table:
                            if _id in entry:
                                print("\nUnit Data:\n")
                                print(str(entry) + "\n")
                        
                    except KeyboardInterrupt:
                        write_data()
                    except ValueError:
                        print("Invalid Input")
            else:
                write_data()
        except KeyboardInterrupt:
            keyboard_interrupt()


def main_menu():
    clear_screen()
    print("Client: " + client_ip + "\nPort: " + port)
    while True:
        try:
            print("*" * 15 ,"MODBUS-TCP CLIENT", "*" * 15)
            print("1.Active Units\n")
            print("2.Data Request\n")
            print("3.Write Data\n")
            print("4.Help Menu\n")
            print("*" * 50)

            _choice = input("> ")
            
            if _choice in keywords:
                word = _choice
                parse_keywords(word)
            elif _choice == '1':
                server_manifest()
            elif _choice == '2':
                data_request()
            elif _choice == '3':
                write_data()
            elif _choice == '4':
                help_menu()
            else:
                main_menu() 
        except KeyboardInterrupt:
            keyboard_interrupt()


def main():
    initial_connection()
    main_menu()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        keyboard_interrupt()
