import json
import sys


base_command = int("0x1020f0", 16)

commands_json = None
with open("./matrix_commands.json", "r") as f:
    commands_json = json.load(f)


keys = []
for each in commands_json.keys():
    keys.append(each)

## find the index of "00102264" in the keys
index = keys.index("00102264")


matrix_map = {}

count = 0

lst = [[] for each in range(16)]
modulus = 0
real = 0

while keys[index] != "00102664":
    command = commands_json[keys[index]]
    if command == "81":
        if commands_json[keys[index + 1]] == "fb":
            matrix_map[keys[index]] = "XX DEATH XX"
            lst[real].append("-")
        else:
            matrix_map[keys[index]] = "HOPE"
            lst[real].append("O")
    else:
        matrix_map[keys[index]] = "HOPE"
        lst[real].append("O")

    count += 1
    modulus = count % 16
    real = count // 16

    index += 4

json.dump(matrix_map, open("matrix_map.json", "w"), indent=4)

for each in lst:
    print(each)
