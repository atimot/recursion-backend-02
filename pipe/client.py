import os
import json

config = json.load(open('config.json'))

f = open(config['filepath'], 'r')

flag = True

while flag:
    if not os.path.exists(config['filepath']):
        flag = False

    data = f.read()

    if len(data) != 0:
        print("Data received from pipe: '{}'".format(data))

f.close()