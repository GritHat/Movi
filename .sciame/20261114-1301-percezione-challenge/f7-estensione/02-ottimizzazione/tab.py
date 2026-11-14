import re,sys
for fn in sys.argv[1:]:
  for l in open(fn):
    if l.startswith('#'): print(l.strip()); continue
    m=re.match(r'(\S+)\s+ris=\s*(\d+)cm scena=(\S+)\s+raggi=\s*(\d+) fot=(\d+) ombra=(\d) arena=(\d).*?agg_ms media=(\S+) p95=(\S+) max=(\S+) primo=(\S+).*?interr_ms media=(\S+) p95=(\S+) max=(\S+) \| passi/fot media=(\S+) max=(\S+) \| mem usata=(\d+) riservata=(\d+).*?allocati=(\d+) toccati_ultimo=(\d+).*?blocchi=(\d+) nodi=(\d+) mattoni=(\d+) scartati=(\d+).*?liberi=(\d+) ignoti=(\d+) occupati=(\d+) \| scorr_ms media=(\S+) max=(\S+) \| rss_max=(\d+).*somma=(\S+) ',l)
    if not m: print('??',l[:80]); continue
    g=m.groups()
    print(f"{g[0]:8s} {g[1]:>2s} {g[2]:5s} {g[3]:>6s} o{g[5]}a{g[6]} agg {g[7]:>8s} {g[8]:>8s} {g[9]:>8s} primo {g[10]:>8s} | int {g[11]:>7s} {g[12]:>7s} {g[13]:>7s} | passi {g[14]:>8s} | mem {g[16]:>8s} | all {g[18]:>6s} tocc {g[19]:>6s} blk {g[20]:>4s} scart {g[23]} | L/I/O {g[24]}/{g[25]}/{g[26]} | scorr {g[27]} {g[28]} | rss {g[29]} | {g[30][-6:]}")
