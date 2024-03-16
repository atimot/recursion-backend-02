import os
import json

config = json.load(open('config.json'))
filepath = config['filepath']

dirpath = os.path.dirname(filepath)
if not os.path.exists(dirpath):
    os.makedirs(dirpath)

if os.path.exists(filepath):
    os.remove(filepath)

os.mkfifo(filepath, 0o600)

print("FIFO named '% s' is created successfully." % filepath)
print("Type in waht you would like to send to clients.")

flag = True

while flag:
    inputstr = input()

    if(inputstr == 'exit'):
        flag = False
    else:
        with open(filepath, 'w') as f:
            f.write(inputstr)

os.remove(filepath)
