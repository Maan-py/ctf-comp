import randcrack
import random
import os
from libnum import s2n
import signal

# ====================
# Our Logic

from sage.all import GF, vector, Matrix

R = randcrack.RandCrack()
R.submit(0) # gacha msb 0
idx = 0

def temper(x) :
    return R._to_int(R._harden(R._to_bitarray(x)))

# This is matrix S, where S(v) = xor sum of the next 624 32 bytes output for a randcrack instance fed [0] * 623 + [v]
def tf_mat() :
    return Matrix(GF(2), list(map(lambda x : int_to_vec(x), get_bit_contributions()[::-1]))).T

# Construct columns of S by finding S(e) for each elementary vector ei
def get_bit_contributions() :
    results = []
    for i in range(32) :
        tempR = randcrack.RandCrack()
        for _ in range(623) :
            tempR.submit(0)
        tempR.submit(1 << i)
        outputs = [tempR.predict_getrandbits(32) for _ in range(624)]
        acc = 0
        for o in outputs :
            acc ^= o
        results.append(acc)
    return results

def int_to_vec(x) :
    return list(map(int, bin(x)[2:].zfill(32)))

mat = tf_mat()
outputs = []
def input(x) :
    global idx, outputs
    idx += 1
    if idx != 624 :
        return str(temper(0))
    else :
        extra = R.predict_getrandbits(32)
        outputs = [R.predict_getrandbits(32) for _ in range(624)]
        acc = 0
        for out in outputs :
            acc ^= out
        result = mat.solve_right(vector(int_to_vec(acc)))
        result = "".join(map(str, list(result)))
        result = int(result, 2)
        return str(result)
    
# ====================

seed = os.urandom(12)
wack = randcrack.RandCrack()
random.seed(seed)

print("Find the rabbit!")
for _ in range(624):
    signal.alarm(2) # Dont waste time
    num = int(input(">> "))
    signal.alarm(0)

    wack.submit(num)
    R.submit(random.getrandbits(32)) if _ != 623 else random.getrandbits(32)

rabbit = 0
for _ in range(624):
    rabbit ^= random.getrandbits(32) ^ wack.predict_getrandbits(32)
    
if abs(rabbit) < s2n(b'ribbit') % 1337:
    print("You found the rabbit!")
    gift = open('flag.txt').read()
    print(gift)
else:
    print("You didn't find the rabbit, try again!")
    print("Rabbit was:", rabbit)
    exit(1)