
import sys
import time
import random
import snappy
import hashlib
import re
import matplotlib.pyplot as plt
class Topic:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.message = ''
        self.ranges = []
        self.max_n_allowed = 40
        self.max_n = self.max_n_allowed
        self.n = 0
        self.force_diff = True
    def compose(self):
        prev = 0
        temp = ''
        for start, end in self.ranges:
            temp += self.message[prev:start]+ self.message[start:end]
            prev = end
        if prev < len(self.message):
            temp += self.message[prev:]
        return temp
    def increment_max_n(self):
        self.max_n += 1
        if self.max_n > self.max_n_allowed:
            self.max_n = self.max_n_allowed
    def print_static(self):
        
        prev = 0
        temp = ''
        for start, end in self.ranges:
            print(self.message[prev:start])
            prev = end
        if prev < len(self.message):
            print(self.message[prev:])
        return temp
    def get_diff(self, message):
        i = 0
        self.ranges = []
        
        def is_diff(c1, c2):
            
            if c1 != c2:
                
                return True
        size = min(len(self.message), len(message))
        while i < size:
            
            if is_diff(self.message[i], message[i]):
                start = i
                count = 0
                while i < size and count < 4:
                    if not is_diff(self.message[i], message[i]):
                        count += 1
                    else:
                        count = 0
                    i += 1
                
            
                
                #print(start, i, self.name)
                self.ranges.append((start, i))
        
            i += 1
      
    def detect_drift(self, message):
       
        
        prev = 0
        start, end = self.ranges[0]
        
        for i in range(prev, start):
            
            if self.message[i] != message[i]:
                #print(i, self.message[i], message[i])
                return True
        prev = end
        return False
    
    def process(self , message):
        if self.force_diff:
            self.get_diff(message)
            self.force_diff = False
        elif self.n > self.max_n:
            if len(self.ranges) > 0:
                if self.detect_drift(message):
                    #print('drift', self.max_n, self.index)
                    self.get_diff(message)
                    self.max_n = self.max_n_allowed
                else:
                    #print('no drift', self.max_n, self.index)
                    self.increment_max_n()
            else:
                self.get_diff(message)
                if len(self.ranges) == 0:
                    self.increment_max_n()
            self.message = message
            self.n = 0
        else:
            self.n += 1
def create_city_message(total):
    topic_name = '/atlanta/techsquare/device1'
    s1 = '{latitude:12345,longitude:12345,temperature:'
    d1 = '39.2'
    s2 = ',humidity:'
    d2 = '84.0'
    s3 = ',light:'
    d3 = '16222'
    s4 = ',dust:'
    d4 = '5455.21'
    s5 = ',airquality_raw:'
    d5 = '441}'
    messages = []

    counter = 0
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    sign = -1
    for i in range(total):
        d1 = '{:.2f}'.format(round(float(d1)+(random.randint(0,10)/100)*sign,2))
        d2 = '{:.2f}'.format(round(float(d2)+(random.randint(0,10)/100)*sign,2))
        d3 = '{:.2f}'.format(round(float(d3)+(random.randint(0,10)/100)*sign,2))
        d4 = '{:.2f}'.format(round(float(d4)+(random.randint(0,10)/100)*sign,2))
        if sign == -1:
            sign = 1
        else:
            sign = -1

        messages.append(topic_name+s1+d1+s2+d2+s3+d3+s4+d4+s5+d5)
        #print(i, messages[i])
        counter += 1
        if counter >= 10000:
            rand_letter = random.choice(alphabet)
            
            s1 = '{'+rand_letter+'atitude:12345,longitude:12345,temperature:'
            counter = 0
    return messages
def create_taxi_message(total):
    messages = []
    for i in range(total):
        messages.append('1358118240000,{"e":[{"u":"string","n":"taxi_identifier","sv":"D2B347756DA9B4B8A284E45499A3538B"},{"u":"string","n":"hack_license","sv":"DEE8A5B1695256673A7CCF26F1DFEBAB"},{"u":"time","n":"pickup_datetime","sv":"2013-01-14 04:28:00"},{"v":"360","u":"second","n":"trip_time_in_secs"},{"v":"2.27","u":"meter","n":"trip_distance"},{"u":"lon","n":"pickup_longitude","sv":"-73.973953"},{"u":"lat","n":"pickup_latitude","sv":"40.747063"},{"u":"lon","n":"dropoff_longitude","sv":"-74.000923"},{"u":"lat","n":"dropoff_latitude","sv":"40.739052"},{"u":"string","n":"payment_type","sv":"CSH"},{"v":"9.00","u":"dollar","n":"fare_amount"},{"v":"0.50","u":"percentage","n":"surcharge"},{"v":"0.50","u":"percentage","n":"mta_tax"},{"v":"0.00","u":"dollar","n":"tip_amount"},{"v":"0.00","u":"dollar","n":"tolls_amount"},{"v":"10.00","u":"dollar","n":"total_amount"}],"bt":1358118240000}')
    return messages


class TopicTableEntry:
    def __init__(self, name, hash):
        self.name = name
        self.hash = hash
        self.topic = None
    def get_topic(self):
        return self.topic
    def set_topic(self, topic):
        self.topic = topic

topic_table = []
total_topics = 10000
for i in range(total_topics):
    topic_table.append(TopicTableEntry('test', i))



with open('city_fixed.txt', 'r') as f:
    messages = f.readlines()
#with open('taxi.txt', 'r') as f:
#    messages = messages + f.readlines()

message_to_hash = [0 for i in range(len(messages))]
num_topics = 0
seen_topics = {}
for i in range(len(messages)):
    index = messages[i].find('"sv":"') 
    topic_name = messages[i][index+6:index+38]
    topic_hash = int(hashlib.md5(topic_name.encode()).hexdigest(),16)%total_topics
    
    if topic_table[topic_hash].get_topic() == None and topic_hash not in seen_topics:
        seen_topics[topic_hash] = 1
        topic_table[topic_hash].set_topic(Topic(topic_name, topic_hash))
        topic_table[topic_hash].get_topic().message = messages[i]
    message_to_hash[i] = topic_hash
    
#compressed_messages = []

def n_times(v,n):
    for i in range(n):
        yield v

#messages = [i for j in messages for i in n_times(j,1)]
#message_to_hash = [i for j in messages for i in n_times(j,1)]

    


j = 0
tot_messages = 200000
stats = []
count_down = 1
begin = 0
end = 0
while j < 20:
    
    begin_v = time.time()
    for i in range(j*tot_messages, j*tot_messages+tot_messages):
        
        #print(i, message_to_hash[i])
        topic_table[message_to_hash[i]].topic.process(messages[i])
        
        #print(messages[i])
        #topic.process(m3)
        #compressed_message = snappy.compress(messages[i])
       
    end_v = time.time()

    begin_s = time.time()
    for i in range(j*tot_messages, j*tot_messages+tot_messages):
        
        #print(i, message_to_hash[i])
        #topic_table[message_to_hash[i]].topic.process(messages[i])
        
        #print(messages[i])
        #topic.process(m3)
        compressed_message = snappy.compress(messages[i])
    
    
    end_s = time.time()
    

   
    stats.append([j*tot_messages, tot_messages/(end_v-begin_v), tot_messages/(end_s-begin_s)])
    j+=1


#plt.plot([i[0] for i in stats], [i[1] for i in stats], label='comprex')
#plt.plot([i[0] for i in stats], [i[2] for i in stats], label='snappy')
#plt.legend()
#plt.show()

def print_comma_separated(stats):
    for i in stats:
        print(str(i[0])+' '+str(i[1])+' '+str(i[2]))

#print_comma_separated(stats)

for i in stats:
        print(i[1])


"""
#message = '1358118240000,{"e":[{"u":"string","n":"taxi_identifier","sv":"D2B347756DA9B4B8A284E45499A3538B"},{"u":"string","n":"hack_license","sv":"DEE8A5B1695256673A7CCF26F1DFEBAB"},{"u":"time","n":"pickup_datetime","sv":"2013-01-14 04:28:00"},{"v":"360","u":"second","n":"trip_time_in_secs"},{"v":"2.27","u":"meter","n":"trip_distance"},{"u":"lon","n":"pickup_longitude","sv":"-73.973953"},{"u":"lat","n":"pickup_latitude","sv":"40.747063"},{"u":"lon","n":"dropoff_longitude","sv":"-74.000923"},{"u":"lat","n":"dropoff_latitude","sv":"40.739052"},{"u":"string","n":"payment_type","sv":"CSH"},{"v":"9.00","u":"dollar","n":"fare_amount"},{"v":"0.50","u":"percentage","n":"surcharge"},{"v":"0.50","u":"percentage","n":"mta_tax"},{"v":"0.00","u":"dollar","n":"tip_amount"},{"v":"0.00","u":"dollar","n":"tolls_amount"},{"v":"10.00","u":"dollar","n":"total_amount"}],"bt":1358118240000}'
#compressed_message = snappy.compress(message)

#print(len(message), len(compressed_message))
"""


total = 0
for start , end in topic_table[message_to_hash[0]].get_topic().ranges:
    total+= end-start

compressed_message = snappy.compress(messages[0])

#print(topic_table[523].get_topic().compose())
print(sys.getsizeof(topic_table[message_to_hash[2]].get_topic().max_n))



#print(total/len(messages[0]), len(messages[0])/len(compressed_message))