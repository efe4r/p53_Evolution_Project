import requests

accessions = {
    "H_sapiens":"P04637",
    "M_musculus":"P02340",
    "R_norvegicus":"P10361",
    "G_gallus":"P10360",
    "X_laevis":"P07193",
    "D_rerio":"P79734"
}

with open('p53_sequences.fasta','w') as out:
    for name,acc in accessions.items():
        url = f'https://rest.uniprot.org/uniprotkb/{acc}.fasta'
        r = requests.get(url)
        r.raise_for_status()
        fasta = r.text
        header, seq = fasta.split('\n',1)
        out.write(f">{name}|{acc}\n{seq}\n")
print("Wrote p53_sequences.fasta")
