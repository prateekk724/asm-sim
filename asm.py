from tables import *

with open("input.txt", "r") as f:
    instruct = f.read()
    instruct = instruct.split("\n")
    instructions = list()
    for lines in instruct:
        instructions.append(lines.split())

initial_state=0
for lines in instructions:
    if(lines[0] != "var" and initial_state==0):
        idx = instructions.index(lines)
        initial_state = 1
    
print(idx)
