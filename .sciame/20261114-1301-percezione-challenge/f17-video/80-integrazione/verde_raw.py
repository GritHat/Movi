# stesso criterio di verde.py (G > R+40, G > B+40, G > 90, > 20 px), su un fotogramma ogni 2 s letto da ffmpeg in rgb24
import sys, subprocess, numpy as np
p = sys.argv[1]; W, H = 1920, 1080
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", "fps=0.5", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True, timeout=600).stdout
n = len(raw) // (W * H * 3); k = 0
for i in range(n):
    a = np.frombuffer(raw[i*W*H*3:(i+1)*W*H*3], np.uint8).reshape(H, W, 3).astype(int); R, G, B = a[..., 0], a[..., 1], a[..., 2]
    m = int(((G > R + 40) & (G > B + 40) & (G > 90)).sum())
    if m > 20: k += 1; print("VERDE", p, "fotogramma", i + 1, "t =", 2 * i, "s", m, "px")
print(p, "fotogrammi:", n, "con verde:", k)
