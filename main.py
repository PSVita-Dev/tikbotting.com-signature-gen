import time
import string
import execjs
import base64

digs = string.digits + string.ascii_letters

def int2base(x, base): #thanks to https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(digs[x % base])
        x = x // base
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)

def e(inputs):
    res = []
    i=0
    while i < len(inputs):
        res.append(base64.b64encode(inputs[i:57].encode()).decode())
        i+=57
    return ''.join(res)
        
def hex_592(inputs):
    return inputs[::-1]


    
def parseInt(string):
    return int(''.join(i for i in string if i.isdigit()))

def x(inputs,key=5):
    res = []
    inputs = str(inputs)[:-3]
    inputs = str(inputs)+"000"

    xor = execjs.compile(open("sm3.js").read())
    has = xor.call('xor',int(inputs),key) # js xor is 32bit
    res.append(int2base(int(has),16)[2:])
    return ''.join(res).replace(',', '')
    

def gen_gorgon(vid,ts):
    ts = int2base(int(ts),16)
    sm3 = execjs.compile(open("sm3.js").read())
    has = sm3.call('sm3_hash',str(vid),ts)
    gorg = "0411"+has.replace(",","")
    return gorg

def gen_klython(ts):
    ts = int2base(int(ts),16)
    return ts

def gen_argus(vid,ts):
    return e(hex_592(e(x(vid, ts)))).replace('=','')

def gen_ladon(ts):
    pre = hex_592(e(str(ts))).replace('=','')
    return e("="+pre)

if __name__ == "__main__":
    videoid = 7150937196365663494 #edit with the id from your video link
    ts = int(round(time.time()))
    print("tekkys x-gorgon:"+gen_gorgon(videoid,ts)) # generate gorgon with the video id (awemeid) parameter and current time
    print("tekkys x-khronos:"+str(ts))
    print("tekkys x-argus:"+gen_argus(int(videoid),ts)) # generate argus with the video id (awemeid) parameter and current time
    print("tekkys x-ladon:"+gen_ladon(ts)) # generate ladon with the current time
    print("tekkys x-klython:"+gen_klython(ts)) # generate klython with the current time
