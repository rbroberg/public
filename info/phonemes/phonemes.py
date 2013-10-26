# -*- coding: utf-8 -*-
# test dropbox integration from codeanywhere
# test dropbox integration from nitrous.io
import codecs
import csv
from math import log

def entropy(p,d):
    acc=0
    for i in range(len(p)):
        if not p[i] == 0 :
            acc=-log(p[i],d)
        else:
            acc=acc # log(0,d) = 0
    return acc

cmu={}
f1=open('data/cmudict.0.7a.csv', 'r')
for line in f1:
    if not line.startswith(';;;'):
        row=line.split(',')
        cmu[row[0].lower()]=len(row[1].split(' '))

f1.close()

words=[]
f2=open('data/wordlist.csv', 'r')
for line in f2:
    if not line.startswith("'"):
        row=line.split(',')
        try:
            words.append((row[2],cmu[row[1].lower()]))
        except:
            words.append((row[2],-99999))

f2.close()

# OBE: I've used this info to 'fix' wordlist
# how many not cross-mapped? 4 ... not bad!
# sum([1 for i in words if i[1]==-99999])
#[('1247', -99999), ('474', -99999), ('419', -99999), ('371', -99999)]
# honour, favour, to-morrow, colour

# now remove them
freqs=[i for i in words if not i[1]==-99999]

# find sum of freqs
acc=sum([int(i[0]) for i in freqs])

# freqs to probs
probs=[int(i[0])/acc for i in freqs]

# spoken word entropy
# 84 symbols in cmudict.0.7a.symbols
entropy(probs,84) #2.076852173647841

# ave word length SUM p(i)*l(i) = 2.89754459466716
avewordlen=sum([probs[i]*freqs[i][1] for i in range(len(probs))])

# how many words are compound symbols?
# 1000 by spelling
wlist=[]
wdict={}
f2=open('data/wordlist.csv', 'r')
for line in f2:
    if not line.startswith("'"):
        row=line.split(',')
        wlist.append(row[1].lower())
        wdict[row[1].lower()]=row[0]

f2.close()

prefixbad=[]
for i in range(len(wlist)):
    for j in range(len(wlist)):
        if not i==j:
            try:
                x=wdict[''.join([wlist[i],wlist[j]])]
                prefixbad.append((wlist[i],wlist[j]))
            except:
                # oh well
                x=1

prefixbad
#[('to', 'o'), ('of', 'ten'), ('a', 'go'), ('a', 'way'), ('a', 'long'), ('a', 'round'), ('in', 'to'), ('he', 'art'), ('with', 'in
#'), ('with', 'out'), ('for', 'get'), ('be', 'come'), ('be', 'came'), ('be', 'side'), ('be', 'low'), ('be', 'cause'), ('me', 'an'
#), ('so', 'on'), ('so', 'me'), ('no', 'thing'), ('no', 'body'), ('when', 'ever'), ('what', 'ever'), ('an', 'other'), ('out', 'si
#de'), ('do', 'or'), ('up', 'on'), ('some', 'what'), ('some', 'thing'), ('some', 'times'), ('some', 'body'), ('any', 'thing'), ('
#any', 'body'), ('how', 'ever'), ('can', 'not'), ('every', 'thing'), ('every', 'body'), ('hand', 'some'), ('under', 'stood'), ('u
#nder', 'stand'), ('gentle', 'man'), ('gentle', 'men'), ('break', 'fast')]
# len(prefixbad) # 43

# ================================
# German

cmu={}
f1=codecs.open('data/voxDE20090209.arpabet', 'r', 'utf-8')
for line in f1:
    row=line.split('\t')
    cmu[row[0].lower()]=len(row[1].split(' '))

f1.close()

words=[]
f2=codecs.open('data/wordfreqlist.de', 'r', 'utf-8')
cnt=0
for line in f2:
    cnt = cnt+1
    if not line.startswith("'") and cnt <= 2000:
        row=line.split(',')
        try:
            words.append((row[2],cmu[row[1].lower()]))
        except:
            words.append((row[2],-99999))

f2.close()

# OBE: I've used this info to 'fix' wordlist
# how many not cross-mapped? 323 in first 1000, 846 in first 2000
# sum([1 for i in words if i[1]==-99999])


# now remove them
freqs=[i for i in words if not i[1]==-99999]
freqs=freqs[0:1000]

# find sum of freqs
acc=sum([int(i[0]) for i in freqs])

# freqs to probs
probs=[int(i[0])/acc for i in freqs]

# spoken word entropy
# how many symbols in german arpabit?
entropy(probs,84) #2.095257550274826

# ave word length SUM p(i)*l(i) = 4.331310634501739
avewordlen=sum([probs[i]*freqs[i][1] for i in range(len(probs))])

# how many words are compound symbols?
# 1000 by spelling
wlist=[]
wdict={}
cnt=0
f2=codecs.open('data/wordfreqlist.de', 'r','utf-8')
for line in f2:
    cnt=cnt+1
    if not line.startswith("'") and cnt <=2000:
        row=line.split(',')
        wlist.append(row[1].lower())
        wdict[row[1].lower()]=row[0]

f2.close()

prefixbad=[]
for i in range(len(wlist)):
    for j in range(len(wlist)):
        if not i==j:
            try:
                x=wdict[''.join([wlist[i],wlist[j]])]
                prefixbad.append((wlist[i],wlist[j]))
            except:
                # oh well
                x=1

prefixbad # 223