import sys, random, math
sys.path.insert(0, sys.argv[1])
sys.dont_write_bytecode = True
import sim_s3s4 as S
rng = random.Random(1)
cnt = 0
for t in range(4000):
    tr = S.Truth(rng, 'prosegue')
    fr = 0
    while True:
        tr.step(); fr += 1
        if not S.detectable(tr.x, tr.z): break
    x_entry = tr.x
    det = None
    for k in range(1, 60):
        tr.step()
        if S.detectable(tr.x, tr.z) and rng.random() < 0.9:
            det = k; break
        if k == 45 and S.cls(tr.x, tr.z, 0.0) == S.NON:
            cnt += 1
            if cnt < 6: print("NON a 3 s:", round(tr.x,2), round(tr.z,2), round(math.hypot(tr.x,tr.z),2), "sp", round(tr.sp,2), "entry", round(x_entry,2), "vz", round(tr.vz,3))
print(cnt)
