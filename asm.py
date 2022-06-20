from tables import *

with open("input.txt", "r") as f:
    instruct = f.read()
    instruct = instruct.split("\n")
    instructions = list()
    for lines in instruct:
        instructions.append(lines.split())      #

main = list()
definitions = list()

for lines in instructions:    
    if(lines[0] == "var"):
        definitions.append(lines)
    else:
        main.append(lines)
print(main)