from azunyan.conn import process, remote
from azunyan.mersenne import untemper, temper, twist, calc
from tqdm import trange

#r = process(['python3', 'chall.py'])
#r = remote('localhost', 8054)
# r = remote('20.6.89.33', 8054)
r = remote('18.143.31.243', 9054)

def sum(lst):
    s = 0
    for i in lst:
        s ^= i
    return s
def int32(x): return x & 0xffffffff

nums = []
num = 0
for _ in trange(623):
    r.sendlineafter('>> ', str(num).encode())
    num = int(r.recvline().strip())
    nums.append(untemper(num))
    
# predict the last number
wack_last = calc(0, nums[0], nums[396])
nums.append(wack_last)

# calculate lhs sum
tw = [i for i in nums]
twist(tw)

idx1 = 622 - 397
idx2 = 622 - 1
idx3 = 622
idx4 = (idx1 - 397) % 624

# crafting solution
lhs = sum(tw[i] for i in [idx1, idx2, idx3, idx4, 623])
mini = 2 ** 33
minimum = 2**32
ans = None

for a in range(2):
    for b in range(2):
        mini = 0
        minimum = lhs
        i = a | (b << 1) | mini
        calc1 = calc(nums[idx1], nums[idx1+1], i)
        calc2 = calc(nums[idx2], i, tw[(idx2 + 397) % 624])
        calc3 = calc(i, nums[idx3+1], tw[(idx3 + 397) % 624])
        calc4 = calc(nums[idx4], nums[idx4+1], calc1)
        rhs = sum(k for k in [nums[-1], calc1, calc2, calc3, calc4])
        minimum = lhs ^ rhs

        for idx in range(2, 32):
            i = a | (b << 1) | (1 << idx) | mini
            
            calc1 = calc(nums[idx1], nums[idx1+1], i)
            calc2 = calc(nums[idx2], i, tw[(idx2 + 397) % 624])
            calc3 = calc(i, nums[idx3+1], tw[(idx3 + 397) % 624])
            calc4 = calc(nums[idx4], nums[idx4+1], calc1)
            rhs = sum(k for k in [nums[-1], calc1, calc2, calc3, calc4])
            pred_rabbit = lhs ^ rhs
            
            if pred_rabbit < minimum:
                mini = i
                minimum = pred_rabbit
            if pred_rabbit == 0: 
                ans = i
                print("Found the answer:", ans)
                break
        if ans: break
    if ans: break
if ans is None: 
    print("Fail")
    ans = mini
    #exit(1)
print("Sending the last number:", ans)
r.sendlineafter('>> ', str(temper(ans)).encode())
print("Predicted rabbit:", minimum)

r.interactive()
