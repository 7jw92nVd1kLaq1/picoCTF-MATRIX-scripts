import json
import sys


class ANSI():
	def background(code):
		return "\33[{code}m".format(code=code)

	def style_text(code):
		return "\33[{code}m".format(code=code)

	def color_text(code):
		return "\33[{code}m".format(code=code)


base_command = int("0x1020f0", 16)

commands_json = None
with open("./matrix_commands.json", "r") as f:
    commands_json = json.load(f)

commands = {}
for key, value in commands_json.items():
    # Convert key and value from hex (as string) to an integer
    int_key = int(key, 16)
    commands[int_key] = value

rbx0x10 = [
    int('01', 16),
    int('01', 16),
    int('00', 16),
]
rbx0x10.extend([int('72', 16)]) # 75, 64, 6c, 72
rbx0x10.extend([0 for each in range(999)])
rbx0x10_location = 4

rbx0x18 = [
    int('00', 16),
    int('00', 16),
    int('00', 16),
]
rbx0x18.extend([0 for each in range(1000)])
rbx0x18_location = 0

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
    print("Jumping to the command: ", current_command)
    rbx0x10_location -= 1

def command0x31():
    global rbx0x10
    global rbx0x10_location
    global current_command

    if rbx0x10[rbx0x10_location - 2] == 0:
        current_command = rbx0x10[rbx0x10_location - 1]
        print("Jumping to the command: ", current_command)
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

    input_flag = 1

    rbx0x10[3] = ord(user_input[user_input_index])

    while rbx0x10_location < 10020 and rbx0x18_location < 10020:
        if rbx0x10_location == 500:
            break

        if current_command == 251:
            print("\n\n")
            print("*"*50)
            print("Failed... You have entered the wrong password")
            print(user_input)
            print("*"*50)
            print("\n\n")
            sys.exit()
        elif current_command == 123:
            user_input_index += 1
            rbx0x10_location = 4
            rbx0x10[3] = ord(user_input[user_input_index])
            print("\n\n")
            print("*"*50)
            print("CONGRATULATIONS! You have entered the right password")
            print("Moving to the next character: ", user_input[user_input_index])
            print("*"*50)

            print(f"Current rbx0x10_location at {rbx0x10_location}: ", rbx0x10[rbx0x10_location])
            print(f"Current rbx0x18_location at {rbx0x18_location}: ", rbx0x18[rbx0x18_location])

            print("Before rbx0x10 Stack: ", rbx0x10[:100])
            print("Before rbx0x18 Stack: ", rbx0x18[:100])

            print("\n\n")
            current_command += 1

        command = commands[base_command + current_command]
        command_rn = current_command

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
            print("Unknown command")
            break
    
        ## For debug
        if input_flag == 1:
            print(ANSI.background(32) + "Current command at ", hex(base_command + current_command), ":", command, "\033[0m")
            print("\n Processing the command ", command, "...\n")
            print(f"After rbx0x10_location at {rbx0x10_location}: ", rbx0x10[rbx0x10_location])
            print(f"After rbx0x18_location at {rbx0x18_location}: ", rbx0x18[rbx0x18_location])
            print("\n" + ANSI.background(35) + "After rbx0x10 Stack")
            for each in range(16, -1, -1):
                if rbx0x10_location == each:
                    print(ANSI.color_text(35) + str(rbx0x10[each]))
                else:
                    print(ANSI.color_text(36) + str(rbx0x10[each]))
            print("\n")
            print(ANSI.background(35) + "After rbx0x18 Stack")
            for each in range(16, -1, -1):
                if rbx0x18_location == each:
                    print(ANSI.color_text(35) + str(rbx0x18[each]))
                else:
                    print(ANSI.color_text(36) + str(rbx0x18[each]))

            print("\033[0m----------------------------------------------------------")
            input()

    for each in range(len(rbx0x10)-1, -1, -1):
        print(chr(rbx0x10[each]), end=" ")
