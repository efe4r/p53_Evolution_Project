from Bio import AlignIO
import matplotlib.pyplot as plt

# Alignment oku
aln = AlignIO.read('p53_aligned.fasta','fasta')
L = aln.get_alignment_length()

# Column-wise korunma skoru
cons = []
for i in range(L):
    col = [record.seq[i] for record in aln]
    most = max(set(col), key=col.count)
    cons.append(col.count(most)/len(col))

# İnsan p53 hotspot pozisyonları
hotspots = [175,245,248,249,273,282]

# Helper: Alignment index
human = [rec for rec in aln if rec.id.startswith("H_sapiens")][0]
def aligned_index_for_residue(seq, pos):
    count = 0
    for i,aa in enumerate(seq):
        if aa != '-':
            count += 1
        if count == pos:
            return i
    return None
hot_cols = [aligned_index_for_residue(human.seq, h) for h in hotspots]

# Plot
plt.figure(figsize=(12,3))
plt.plot(cons, linewidth=1)
for hc in hot_cols:
    if hc: plt.axvline(hc, linestyle='--', alpha=0.7)
plt.title('p53 conservation across species (column-wise)')
plt.xlabel('Alignment column')
plt.ylabel('Conservation fraction')
plt.tight_layout()
plt.savefig('p53_conservation.png', dpi=200)
