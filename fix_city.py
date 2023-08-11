
import re
import random

def find(s, sub):
    return [m.start() for m in re.finditer(sub, s)]

def fix_string(message, substr, offset, lenght, type):
    subs = find(message, substr)
    
    i = 0
    while i < len(subs):
        
        
        
        j = 0
        if type == 'numeric':
            while (message[subs[i]+offset+j].isnumeric() or message[subs[i]+offset+j] == '.' or message[subs[i]+offset+j] == '-'):
                
                j += 1
        else:
            while (message[subs[i]+offset+j] != '"'):
                
                j += 1
        if j < lenght:
            
            temp = message[subs[i]+offset:subs[i]+offset+j]
            
            temp = temp.zfill(lenght)
            
            message = message[:subs[i]+offset]+temp+message[subs[i]+offset+j:]
            subs = find(message, substr)
        i+=1
    return message


def randomizer(message):
    subs = find(message, '"v":')
    i = 0
    
    while i < len(subs):
        
        rand_n = random.randint(1000000000, 1100000000)
        rep = message[subs[i]+5:subs[i]+5+10]
       
        message = message.replace(rep, str(rand_n))
        
        i+=1
    return message
        


def fix_file(source, dest):
    messages = []
    message_blocks = []
    with open(source, 'r') as f:
        messages = f.readlines()
        
        for i in range(len(messages)):
            messages[i] = fix_string(messages[i], '"sv":"', 6, 32, 'string')
            messages[i] = fix_string(messages[i], '"v":', 5, 11, 'numeric')
    
    j = 0
    while j < 5000:
        
        
        for i in range(len(messages)):
            if len(messages[i]) == 427:
                message_blocks.append(randomizer(messages[i]))
            
        j+=1            

    with open(dest, 'w') as f:
        
        for message in message_blocks:
            f.write(message)

fix_file('city.txt', 'city_fixed.txt')