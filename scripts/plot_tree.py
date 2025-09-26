from Bio import Phylo
import matplotlib.pyplot as plt

# Newick dosyasını oku
tree = Phylo.read('p53_tree.nwk', 'newick')

# Görselleştir
plt.figure(figsize=(6,6))
Phylo.draw(tree, do_show=False)  # Ekrana gösterme, sadece kaydet
plt.title('p53 phylogenetic tree')
plt.tight_layout()
plt.savefig('p53_tree.png', dpi=200)
print("p53_tree.png kaydedildi.")
