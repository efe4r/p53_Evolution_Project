import matplotlib
matplotlib.use('Agg')  # PNG için ekran açmadan çalıştır
from Bio import AlignIO
import math
import matplotlib.pyplot as plt

# ------------------------------
# 1) Alignment oku
# ------------------------------
aln_file = r'C:\Users\PC\Desktop\p53_evolution\p53_aligned.fasta'
aln = AlignIO.read(aln_file,'fasta')
L = aln.get_alignment_length()

# ------------------------------
# 2) Shannon entropy hesaplama
# ------------------------------
def shannon_entropy(col):
    freqs = {}
    for aa in col:
        if aa != '-':
            freqs[aa] = freqs.get(aa,0)+1
    total = sum(freqs.values())
    if total == 0:
        return 0
    entropy = -sum((f/total)*math.log2(f/total) for f in freqs.values())
    return entropy

entropy_scores = [shannon_entropy([rec.seq[i] for rec in aln]) for i in range(L)]
conservation_scores = [1 - e/max(entropy_scores) if max(entropy_scores) != 0 else 1 for e in entropy_scores]

# ------------------------------
# 3) Human hotspot pozisyonları
# ------------------------------
hotspot_positions = [175,245,248,249,273,282]
human = [rec for rec in aln if rec.id.startswith("H_sapiens")][0]

def aligned_index_for_residue(seq, pos):
    count = 0
    for i,aa in enumerate(seq):
        if aa != '-':
            count += 1
        if count == pos:
            return i
    return None

hot_cols = [aligned_index_for_residue(human.seq, h) for h in hotspot_positions]

# ------------------------------
# 4) Domain bölgeleri (UniProt)
# ------------------------------
domains = {
    'Transactivation': (1, 93),
    'DNA-binding': (94, 292),
    'Tetramerization': (325, 356)
}
domain_cols = {}
for name, (start, end) in domains.items():
    start_idx = aligned_index_for_residue(human.seq, start)
    end_idx = aligned_index_for_residue(human.seq, end)
    domain_cols[name] = (start_idx, end_idx)

# ------------------------------
# 5) Grafik çizimi
# ------------------------------
plt.figure(figsize=(14,5))

# Korunma
plt.plot(conservation_scores, label='Conservation (1-Entropy)', linewidth=1.5)

# Domainleri gölge ile göster
colors = {'Transactivation':'yellow','DNA-binding':'grey','Tetramerization':'lightblue'}
for name, (start,end) in domain_cols.items():
    if start is not None and end is not None:
        plt.axvspan(start, end, color=colors[name], alpha=0.2, label=name)

# Hotspotları göster
for hc in hot_cols:
    if hc is not None:
        plt.axvline(hc, color='red', linestyle=':', alpha=0.7)

plt.xlabel('Alignment column')
plt.ylabel('Conservation')
plt.title('p53 Conservation with Domains and Human Hotspots')
plt.legend(loc='upper right', fontsize=8)
plt.tight_layout()

# PNG kaydet
output_file = r'C:\Users\PC\Desktop\p53_evolution\p53_conservation_hotspots_domains.png'
plt.savefig(output_file, dpi=200)
print(f"Grafik kaydedildi: {output_file}")
