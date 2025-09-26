from Bio import SeqIO
from Bio.Align import MultipleSeqAlignment

# FASTA dosyamızı oku
records = list(SeqIO.parse("p53_sequences.fasta", "fasta"))

# Basit bir multiple sequence alignment (demo)
alignment = MultipleSeqAlignment(records)

# Alignment’i ekrana yazdır
for record in alignment:
    print(f">{record.id}")
    print(record.seq)
