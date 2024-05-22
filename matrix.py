import json
import sys


## Convert the base command to an integer for calculation
base_command = int("0x1020f0", 16)


## Load the commands from the matrix_commands.json file
commands_json = None
with open("./matrix_commands.json", "r") as f:
    commands_json = json.load(f)

## Convert the addresses in hexadecimals from the json file to integers
commands = {}
for key, value in commands_json.items():
    # Convert key and value from hex (as string) to an integer
    int_key = int(key, 16)
    commands[int_key] = value


## The stack at `param_1[2]`
rbx0x10 = [
    int('01', 16),
    int('01', 16),
    int('00', 16),
]
rbx0x10.extend([int('72', 16)]) # 75, 64, 6c, 72
rbx0x10.extend([0 for each in range(999)])
rbx0x10_location = 4

## The stack at `param_1[3]`
rbx0x18 = [
    int('00', 16),
    int('00', 16),
    int('00', 16),
]
rbx0x18.extend([0 for each in range(1000)])
rbx0x18_location = 0


## The current command
current_command = 124


def command0x10():
    global rbx0x10
    global rbx0x10_location
    global current_command
    rbx0x10[rbx0x10_location] = rbx0x10[rbx0x10_location-1]
    rbx0x10_location += 1
    current_command += 1

def command0x11():
    global rbx0x10_location
    global current_command
    rbx0x10_location -= 1
    current_command += 1

def command0x12():
    global rbx0x10
    global rbx0x10_location
    global current_command
    minus4 = rbx0x10[rbx0x10_location - 2]
    minus2 = rbx0x10[rbx0x10_location - 1]
    rbx0x10[rbx0x10_location - 2] = minus4 + minus2

    rbx0x10_location -= 1
    current_command += 1

def command0x13():
    global rbx0x10 
    global rbx0x10_location
    global current_command
    minus4 = rbx0x10[rbx0x10_location - 2]
    minus2 = rbx0x10[rbx0x10_location - 1]
    rbx0x10[rbx0x10_location - 2] = minus4 - minus2

    rbx0x10_location -= 1
    current_command += 1

def command0x14():
    global rbx0x10
    global rbx0x10_location
    global current_command
    temp = rbx0x10[rbx0x10_location - 2]
    rbx0x10[rbx0x10_location - 2] = rbx0x10[rbx0x10_location - 1]
    rbx0x10[rbx0x10_location - 1] = temp

    current_command += 1

def command0x20():
    global rbx0x10
    global rbx0x18
    global rbx0x10_location
    global rbx0x18_location
    global current_command
    rbx0x18[rbx0x18_location] = rbx0x10[rbx0x10_location - 1]
    rbx0x10_location -= 1
    rbx0x18_location += 1
    current_command += 1

def command0x21():
    global rbx0x10_location
    global rbx0x18_location
    global current_command
    rbx0x10[rbx0x10_location] = rbx0x18[rbx0x18_location - 1]
    rbx0x10_location += 1
    rbx0x18_location -= 1
    current_command += 1

def command0x30():
    global rbx0x10
    global rbx0x10_location
    global current_command
    current_command = rbx0x10[rbx0x10_location - 1]
    #print("Jumping to the command: ", current_command)
    rbx0x10_location -= 1

def command0x31():
    global rbx0x10
    global rbx0x10_location
    global current_command

    if rbx0x10[rbx0x10_location - 2] == 0:
        current_command = rbx0x10[rbx0x10_location - 1]
    #    print("Jumping to the command: ", current_command)
    else:
        current_command += 1
    rbx0x10_location -= 2

def command0x32():
    global rbx0x10
    global rbx0x10_location
    global current_command
    
    if rbx0x10[rbx0x10_location - 2] != 0:
        current_command = rbx0x10[rbx0x10_location - 1]
    else:
        current_command += 1
    rbx0x10_location -= 2

def command0x33():
    global rbx0x10
    global rbx0x10_location
    global current_command
    
    if rbx0x10[rbx0x10_location - 2] < 0:
        current_command = rbx0x10[rbx0x10_location - 1]
    else:
        current_command += 1
    rbx0x10_location -= 2

def command0x34():
    global rbx0x10
    global rbx0x10_location
    global current_command
    
    if rbx0x10[rbx0x10_location - 2] < 1:
        current_command = rbx0x10[rbx0x10_location - 1]
    else:
        current_command += 1
    rbx0x10_location -= 2

def command0x80():
    global rbx0x10
    global rbx0x10_location
    global current_command
    rbx0x10[rbx0x10_location] = int(commands[base_command+current_command+1], 16)
    rbx0x10_location += 1
    current_command += 2

def command0x81():
    global rbx0x10
    global rbx0x10_location
    global current_command
    next_command = commands[base_command+current_command+2] + commands[base_command+current_command+1]
    rbx0x10[rbx0x10_location] = int(next_command, 16)
    rbx0x10_location += 1
    current_command += 3


if __name__ == "__main__":
    user_input = input("Enter the password: ")
    base_command = int("0x1020f0", 16)
    user_input_index = 0

    rbx0x10[3] = ord(user_input[user_input_index])
    break_point = None

    while rbx0x10_location < 10020 and rbx0x18_location < 10020:
        if rbx0x10_location == 500:
            break
        
        if current_command == 123:
            user_input_index += 1
            rbx0x10_location = 4
            try:
                rbx0x10[3] = ord(user_input[user_input_index])
            except IndexError:
                break
            current_command += 1
        ## 251 is 'FB' in hex. End of the program
        elif current_command == 251:
            print("\n\n")
            print("*"*50)
            print("Failed... You have entered the wrong password")
            print(f'Your input: {user_input}')
            print("*"*50)
            print("\n\n")
            sys.exit()

        command = commands[base_command + current_command]
        if command == "00":
            current_command += 1
        elif command == "01":
            break
        elif command == "10":
            command0x10()
        elif command == "11":
            command0x11()
        elif command == "12":
            command0x12()
        elif command == "13":
            command0x13()
        elif command == "14":
            command0x14()
        elif command == "20":
            command0x20()
        elif command == "21":
            command0x21()
        elif command == "30":
            command0x30()
        elif command == "31":
            command0x31()
        elif command == "80":
            command0x80()
        elif command == "81":
            command0x81()
        else:
            break

    output_msg = []
    for each in range(len(rbx0x10)-1, -1, -1):
        output_msg.append(chr(rbx0x10[each]))
    
    output_msg = "".join(output_msg)
    if "Congratulations" in output_msg:
        print("\n\n")
        print("*"*50)
        print("Congratulations... You have entered the correct password")
        print(f'Your input: {user_input}')
        print("*"*50)
        print("\n\n")
    else:
        print("\n\n")
        print("*"*50)
        print("Failed... You have entered the wrong password")
        print(f'Your input: {user_input}')
        print("*"*50)
        print("\n\n")
