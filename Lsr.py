# Written by XI BI for COMP9331 ass1
# The python version is 2.7.16



import sys
import time
import threading
import socket
from collections import defaultdict



def getmss(port, conf):
    global Node_alive 
    global Node_infor
    global Hb_time
    nodesock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ('localhost', port)
    nodesock.bind(address)
    while True:
        try:
            content, portname = nodesock.recvfrom(1024)
            index = Node_alive.keys()
            # print Node_alive
            # print Node_infor
            P_lock.acquire()
            if content in index:
                #Node_alive[content] = 'alive'
                Hb_time[content] = time.time()
            else:
                info = content.split('\r')
                # The first time disassemble to get soure\nname cost port state
                while '' in info:
                    info.remove('')
                for i in info:
                    source = i.split('\n')[0]
                    if source in Node_infor:
                        if Node_infor[source] == i:
                            continue
                        else:
                            Node_infor[source] = i
                    else:
                        Node_infor[source] = i
            # print Node_alive
            # print Node_infor
            P_lock.release()

        except Exception as e:
            print e
            break
    nodesock.close()



def sendmss(source, conf):
    global Node_alive 
    global Node_infor
    global P_lock
    # source is the name of the node
    # conf is the information of its neighbors
    nodesock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        time.sleep(1) # Set the update_interval as 1 second
        try:
            P_lock.acquire()
            # The content should be in this format-> source\nNeighbor cost port state
            # And each one with the same source is seperated by '\n'
            # each one with the different source is seperated by '\r'
            data  = []
            for m in Node_alive:
                if m in Node_infor:
                    if Node_alive[m] == 'die':
                        Node_infor.pop(m)
                        # remove the dead nodes
            for i in Node_infor:
                assemble_1 = []
                disassemble_1 = Node_infor[i].split('\n') # disassemble_1 -> list[source,'name,cost,port,state'*n]
                name = disassemble_1.pop(0)
                for n in disassemble_1:
                    disassemble_2 = n.split()
                    if disassemble_2[0] in Node_alive:
                        disassemble_2[3] = Node_alive[disassemble_2[0]] # disassemble_2 -> list[name,cost,port,state]
                    assemble_2 = ' '.join(disassemble_2) # assemble -> str'name cost port state'
                    assemble_1.append(assemble_2)
                assemble_1.insert(0,name)
                content = '\n'.join(assemble_1)
                Node_infor[name] = content

            massage = []
            for j in Node_infor:
                massage.append(Node_infor[j])
            finalmss = '\r'.join(massage)
        
            # below is the part to send information to its neighbors
            
            for j in conf:
                # massage = []
                # known = []
                neigbors = j.split()
                destination = neigbors[0]
                if Node_alive[destination] == 'alive':
                    # if destination in Node_infor:
                    #     neigh_known = Node_infor[destination]
                    #     check_known = neigh_known.split('\n')
                    #     check_known = check_known[1:]
                    #     print check_known
                    #     for i in check_known:
                    #         temp = i.split()
                    #         known = temp[0]
                    #     for n in Node_infor:
                    #         if n not in known:
                    #             massage.append(Node_infor[n])
                    # else:
                    #     for n in Node_infor:
                    #         massage.append[Node_infor[n]]
                    # finalmss = '\r'.join(massage)
                    address = ('localhost', int(neigbors[2]))
                    nodesock.sendto(finalmss, address)
            P_lock.release()
        except Exception as e:
            print e
            break
    nodesock.close()


def heartbeat(Node_name, conf):
    global Node_infor
    heartsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        time.sleep(0.3) # let the heartbeat packet be sent 3 times per second
        try:
            for i in conf:
                neigbors = i.split()
                address = ('localhost', int(neigbors[2]))
                data = Node_name
                heartsock.sendto(data, address)
        except Exception as e:
            print e
            break
    heartsock.close()

def detection_1():
    global P_lock
    global Node_alive
    while True:
        time.sleep(20)
        P_lock.acquire()
        for i in Node_alive:
            Node_alive[i] = 'die'
        P_lock.release()

def detection_2():
    global P_lock
    global Node_alive
    global Hb_time
    while True:
        time.sleep(2)
        P_lock.acquire()
        for i in Hb_time:
            current_time = time.time()
            if (current_time - Hb_time[i]) > 2:
                Node_alive[i] = 'die'
            else:
                Node_alive[i] = 'alive'
        P_lock.release()
    

def findshortest(names,shortpath,unvisited):
    mincost = float('inf')
    minnode = None
    if names == []:
        names = unvisited[:]
    for i in names:
        if shortpath[i] < mincost:
            minnode = i
            mincost = shortpath[i]
    return minnode



def Dijkstra(hostname):
    global Node_infor
    global P_lock
    while True:
        time.sleep(29)
        P_lock.acquire()
        # print Node_alive
        # print Node_infor
        shortpath = defaultdict(float)
        pre_node = defaultdict(str)
        unvisited = Node_infor.keys()
        unvisited.sort()
        visited = []
        current_node = hostname
        for i in unvisited:
            if i == hostname:
                shortpath[i] = 0
            else:
                shortpath[i] = float('inf')
        while unvisited:
            visited.append(current_node)
            if current_node in unvisited:
                unvisited.remove(current_node)
            else:
                print "Update error: Router will recaculate the path"
                break
            neigbs = Node_infor[current_node].split('\n')
            neigbs.pop(0)
            allname = []
            for i in neigbs:
                nodes = i.split()
                name = nodes[0]
                cost = float(nodes[1])
                state = nodes[3]
                if state == 'alive':
                    cost = round(cost + shortpath[current_node], 1)
                    if cost < shortpath[name]:
                        shortpath[name] = cost
                        pre_node[name] = current_node
                    if name in unvisited:
                        allname.append(name)
                else:
                    if name in unvisited:
                        unvisited.remove(name)
                        shortpath.pop(name)
            current_node = findshortest(allname,shortpath,unvisited)
        print 'I am Router %s'%(hostname)
        # print Node_infor
        numbers = 0
        for i in shortpath:
            numbers += 1
            path = []
            current = i
            while current != hostname:
                path.append(current)
                current = pre_node[current]
            path.append(current)
            path.reverse()
            pathstr = ''.join(path)
            if len(path) == 1:
                continue
            else:
                print 'Least cost path to router %s: %s and the cost is %.1f'%(path[-1],pathstr,shortpath[path[-1]])
        if numbers == 1:
            print "There is only one Router in the network\n"
        else:
            print
        P_lock.release()
        

global Node_alive  # record the nodes that are alive in network
global Node_infor  # record the information recieved in current time
global P_lock      # get a programing lock
global Hb_time     # record the time when node recieves a new heartbeat packet

Node_alive = defaultdict(str)
Node_infor = defaultdict(str)
P_lock = threading.Lock()
Hb_time = defaultdict(float)

# read the configuration file
try:
    with open(sys.argv[1],'r') as f:
        conf = f.read().split('\n')
        if '' in conf:
            conf.remove('')
except Exception as e:
    print e
    sys.exit()


host = conf.pop(0).split()
hostname = str(host[0])
portnumb = int(host[1])
neigbor_num = int(conf.pop(0)) 
# Now the conf only contains information of neighbors

Node_infor[hostname] = hostname
# format-> source\nNeighbor cost port state
for n in conf:
    neighbors = n.split()
    Node_alive[neighbors[0]] = 'die'
    Hb_time[neighbors[0]] = time.time()
    Node_infor[hostname] = Node_infor[hostname] + '\n' + n + ' ' + Node_alive[neighbors[0]]

thread_send = threading.Thread(target = sendmss, args = (hostname, conf))
thread_get = threading.Thread(target = getmss, args = (portnumb, conf))
thread_heart = threading.Thread(target = heartbeat, args = (hostname, conf))
thread_dijks = threading.Thread(target = Dijkstra, args = (hostname, ))
thread_detection = threading.Thread(target = detection_2)

thread_send.setDaemon(True)
thread_get.setDaemon(True)
thread_heart.setDaemon(True)
thread_dijks.setDaemon(True)
thread_detection.setDaemon(True)

thread_send.start()
thread_get.start()
thread_heart.start()
thread_dijks.start()
thread_detection.start()

thread_send.join(float('inf'))
thread_get.join(float('inf'))
thread_heart.join(float('inf'))
thread_dijks.join(float('inf'))
thread_detection.join(float('inf'))
