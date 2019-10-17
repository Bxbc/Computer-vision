# Written by BI XI
# reference the knowledge about the SAT algorithm
# I am not sure whether the SAT is usefull for this case 
# However it seems ok with these situation given


import re
import math
from collections import defaultdict
from collections import deque
from copy import deepcopy


def angle(p):
    point = []
    for i in p:
        ni = i.split()
        point.append([float(ni[0]),float(ni[1])])
    a = math.sqrt((point[0][0]-point[1][0])**2 + (point[0][1]-point[1][1])**2)
    b = math.sqrt((point[1][0]-point[2][0])**2 + (point[1][1]-point[2][1])**2)
    c = math.sqrt((point[0][0]-point[2][0])**2 + (point[0][1]-point[2][1])**2)
    ang = (a**2 + b**2 - c**2)/(2*a*b)
    return ang,a

def available_coloured_pieces(file):
    f = file.read()
    file.close()
    rec = defaultdict(list)
    s = re.compile(r'<path.+>')
    ls = s.findall(f)
    # ls is a list contain all the paths in .xml
    sp = re.compile(r'\d+\s+\d+',re.I)
    sc = re.compile(r'"\w+"',re.I)
    for i in ls:
        pts = sp.findall(i)
        col = sc.search(i).group().strip('"')
        rec[col].extend(pts)
    return rec


def are_valid(coloured_pieces):
    for i in coloured_pieces:
        angs = []
        vx = len(coloured_pieces[i])
        dq = deque(maxlen = 3)
        dc = deque(maxlen = 2)
        dq2 = deque(maxlen = 3)
        if vx < 3 and vx != 0:
            return False
        elif vx == 0:
            return True
        else:
            allpieces = deepcopy(coloured_pieces[i])
            allpieces.append(coloured_pieces[i][0])
            allpieces.append(coloured_pieces[i][1])
            for j in allpieces:
                dq2.append(j)
                point = j.split()
                dq.append(point)
                if len(dq) < 3:
                    continue
                else:
                    cv = (int(dq[0][0]) - int(dq[2][0]))*(int(dq[1][1]) - int(dq[2][1])) - \
                        (int(dq[1][0]) - int(dq[2][0]))*(int(dq[0][1]) - int(dq[2][1]))
                    if cv == 0:
                        return False
                    else:
                        ans,_ = angle(dq2)
                        ans = math.acos(ans) * (180/math.pi)
                        angs.append(ans)
                        dc.append(cv)
                        if len(dc) == 2:
                            if dc[0]*dc[1] < 0:
                                return False
                            else:
                                continue
                        else:
                            continue
        final = sum(angs)
        final = round(final,10)
        if final == (vx - 2) * 180.0:
            continue
        else:
            return False
    return True
                
def are_identical_sets_of_coloured_pieces(col1, col2):
    if are_valid(col1) and are_valid(col2):
        k1 = list(col1.keys())
        k2 = list(col2.keys())
        k1 = sorted(k1)
        k2 = sorted(k2)
        if k1 != k2:
            return False
        else:
            for i in k1:
                if len(col1[i]) != len(col2[i]):
                    return False
                else:
                    ang1 = deque(maxlen = 3)
                    ang2 = deque(maxlen = 3)
                    ps1 = deepcopy(col1[i])
                    ps2 = deepcopy(col2[i])
                    ps1.append(col1[i][0])
                    ps1.append(col1[i][1])
                    ps2.append(col2[i][0])
                    ps2.append(col2[i][1])
                    angs1 = []
                    sides1 = []
                    angs2 = []
                    sides2 = []
                    for n in ps1:
                        ang1.append(n)
                        if len(ang1) < 3:
                            continue
                        else:
                            ang,a = angle(ang1)
                            angs1.append(ang)
                            sides1.append(a)
                    for m in ps2:
                        ang2.append(m)
                        if len(ang2) < 3:
                            continue
                        else:
                            ang,a = angle(ang2)
                            angs2.append(ang)
                            sides2.append(a)
                    angs1.sort()
                    sides1.sort()
                    angs2.sort()
                    sides2.sort()
                    if angs1 == angs2 and sides1 == sides2:
                        continue
                    else:
                        return False
            return True 
    else:
        return False              
    
         
def is_solution(tangram,shape):
    if not are_valid(tangram):
        return False
    keys = list(tangram.keys())
    num = len(keys)
    r = 0
    while(r < num -1):
        vp1 = tangram[keys[r]]
        t = r+1
        while(t < num):
            vp2 = tangram[keys[t]]
            bl = sat(vp1,vp2)
            if bl:
                t += 1
            else:
                return False
        r += 1
    count = 0
    newt = deepcopy(tangram)
    for i in shape:
        vs = shape[i]
        count  = 1
    if count == 0:
        return True
    inpt = defaultdict(list)
    for i in tangram:
        for j in tangram[i]:
            vn = deepcopy(vs)
            vn.append(vs[0])
            dp = deque(maxlen = 2)
            if j in vn:
                continue
            else:
                allang = []
                cvv = rcv(vn[0:3])
                for n in vn:
                    tr = []
                    dp.append(n)
                    if len(dp) < 2:
                        continue
                    else:
                        tr.append(dp[0])
                        tr.append(j)
                        tr.append(dp[1])
                        ang,_ = angle(tr)
                        if abs(ang) > 1:
                            ang = round(ang,8)
                        ang = math.acos(ang) * (180/math.pi)
                        nt = []
                        nt.append(tr[0])
                        nt.append(tr[2])
                        nt.append(tr[1])
                        cv = rcv(nt)
                        if cv > 0:
                            allang.append(ang)
                        elif cv < 0:
                            allang.append(-1*ang)
                        else:
                            if cvv > 0:
                                allang.append(ang)
                            else:
                                allang.append(-1*ang)
                if round(sum(allang),8) == 0:
                    return False
                else:
                    newt[i].remove(j)
                    inpt[i].append(j)
    allpts = []
    sinp = []
    for i in inpt:
        allpts.extend(inpt[i])
    for j in allpts:
        if j not in sinp:
            sinp.append(j)
    for i in sinp:
        for j in tangram:
            if i in tangram[j]:
                continue
            else:
                dq = deque(maxlen = 2)
                tr=[]
                sump = []
                tk = deepcopy(tangram[j])
                tk.append(tangram[j][0])
                cvv = rcv(tk[0:3])
                record = 0
                for n in tk:
                    dq.append(n)
                    if len(dq) < 2:
                        continue
                    else:
                        tr.append(dq[0])
                        tr.append(i)
                        tr.append(dq[1])
                        nt = []
                        nt.append(dq[0])
                        nt.append(dq[1])
                        nt.append(i)
                        ang,_ = angle(tr)
                        if abs(ang) > 1:
                            ang = round(ang,8)
                        ang = math.acos(ang) * (180/math.pi)
                        cv = rcv(nt)
                        if cv > 0:
                            sump.append(ang)
                        elif cv < 0:
                            sump.append(-1*ang)
                        else:
                            record  = 1
                if record == 1:
                    continue
                else:
                    sf = sum(sump)
                    if round(sf,8) != 360:
                        continue
                    else:
                        return False
              
    vet = []
    svet = []
    for i in newt:
        vet.extend(newt[i])
    for i in vet:
        if i not in svet:
            svet.append(i)
    newvs = deepcopy(vs)
    if len(svet) ==len(vs):
        for i in svet:
            if i in vs:
                continue
            else:
                return False
    else:
        return False
    sall = sarea(newvs)
    pall = []
    for i in tangram:
        s = sarea(tangram[i])
        pall.append(s)
    if sum(pall) != sall:
        return False
    else:
        mid = []
        dou = deque(maxlen = 2)
        fa = deepcopy(tangram)
        for i in fa:
            nfa = fa[i].append(fa[0])
            for j in nfa:
                dou.append(j)
                if len(dou) < 2:
                    continue
                else:
                    a1 = (int(dou[0].split()[0]) + int(dou[1].split()[0]))/2
                    a2 = (int(dou[0].split()[1]) + int(dou[1].split()[1]))/2
                    mid.append(str(a1)+' '+str(a2))

        vn = deepcopy(vs)
        vn.append(vs[0])
        for i in mid:
            allang = []
            dou.clear()
            for j in vn:
                tr = []
                dou.append(j)
                if len(dou) < 2:
                    continue
                else:
                    tr.append(dou[0])
                    tr.append(i)
                    tr.append(dou[1])
                    if (float(dou[0].split()[0]) == float(i.split()[0])) or (float(dou[1].split()[1]) == float(i.split()[1])):
                        break
                    else:
                        ang,_ = angle(tr)
                        if abs(ang) > 1:
                            ang = round(ang,8)
                        ang = math.acos(ang) * (180/math.pi)
                        nt = []
                        nt.append(tr[0])
                        nt.append(tr[2])
                        nt.append(tr[1])
                        cv = rcv(nt)
                        if cv > 0:
                            allang.append(ang)
                        elif cv < 0:
                            allang.append(-1*ang)
                        else:
                            if cvv > 0:
                                allang.append(ang)
                            else:
                                allang.append(-1*ang)
            if abs(sum(allang) - 360) < 1e-8:
                return False
        return True
                    


def sarea(pt):
    n = len(pt)
    np = []
    np.append(pt[-1])
    np.extend(pt)
    np.append(pt[0])
    s = 0
    for i in range(1,n+1):
        a = int(np[i].split()[1])*(int(np[i+1].split()[0]) - int(np[i-1].split()[0]))
        s += a
    return abs(s)

def rcv(tr):
    c1 = float(tr[1].split()[0])*float(tr[2].split()[1]) + float(tr[0].split()[0])*float(tr[1].split()[1]) + float(tr[0].split()[1])*float(tr[2].split()[0]) 
    c2 = float(tr[0].split()[1])*float(tr[1].split()[0]) + float(tr[1].split()[1])*float(tr[2].split()[0]) + float(tr[0].split()[0])*float(tr[2].split()[1])
    return c1-c2


def sat(a,b):
    p1 = deepcopy(a)
    p2 = deepcopy(b)
    p2.append(b[0])
    p1.append(a[0])
    l = deque(maxlen = 2)
    for i in p1:
        l.append(i)
        if len(l) < 2:
            continue
        else:
            max1 = float('-inf')
            min1 = float('inf')
            max2 = float('-inf')
            min2 = float('inf')
            x = int(l[1].split()[0]) - int(l[0].split()[0])
            y = int(l[1].split()[1]) - int(l[0].split()[1])
            pc = [-1*y,x]
            for n in a:
                dot = int(n.split()[0])*pc[0] + int(n.split()[1])*pc[1]
                if dot < min1:
                    min1 = dot
                if dot > max1:
                    max1 = dot
            for m in b:
                dot = int(m.split()[0])*pc[0] + int(m.split()[1])*pc[1]
                if dot < min2:
                    min2 = dot
                if dot > max2:
                    max2 = dot
            if (max1 <= min2) or (max2 <= min1):
                return True
            else:
                continue
    l.clear()
    for i in p2:
        l.append(i)
        if len(l) < 2:
            continue
        else:
            max1 = float('-inf')
            min1 = float('inf')
            max2 = float('-inf')
            min2 = float('inf')
            x = int(l[1].split()[0]) - int(l[0].split()[0])
            y = int(l[1].split()[1]) - int(l[0].split()[1])
            pc = [-1*y,x]
            for n in b:
                dot = int(n.split()[0])*pc[0] + int(n.split()[1])*pc[1]
                if dot < min1:
                    min1 = dot
                if dot > max1:
                    max1 = dot
            for m in a:
                dot = int(m.split()[0])*pc[0] + int(m.split()[1])*pc[1]
                if dot < min2:
                    min2 = dot
                if dot > max2:
                    max2 = dot
            if (max1 <= min2) or (max2 <= min1):
                return True
            else:
                continue
    return False
                    