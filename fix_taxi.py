
import re

def find(s, sub):
    return [m.start() for m in re.finditer(sub, s)]

def fix_string(message):
    subs = find(message, '"v":')
    
    i = 0
    while i < len(subs):
        
        
        print(message[i+5:i+5+10])
        j = 0
        while message[subs[i]+5+j].isnumeric() or message[subs[i]+5+j] == '.':
            j += 1
        if j < 5:
            
            temp = message[subs[i]+5:subs[i]+5+j]
            
            temp = temp.zfill(5)
            print(temp)
            message = message[:subs[i]+5]+temp+message[subs[i]+5+j:]
            subs = find(message, '"v":')
        i+=1
    return message





def fix_file(source, dest):
    messages = []
    with open(source, 'r') as f:
        messages = f.readlines()
        print(len(messages))
        for i in range(len(messages)):
            messages[i] = fix_string(messages[i])
            print(messages[i])

    with open(dest, 'w') as f:
        
        for message in messages:
            f.write(message)

fix_file('taxi_temp.txt', 'taxi.txt')