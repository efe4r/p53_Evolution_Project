# --- 1) PDB dosyasını yükle ---
load C:/Users/PC/Desktop/p53_evolution/1TUP.pdb, p53

# --- 2) Görselleştirme ayarları ---
hide everything
show cartoon
bg_color white
set ray_opaque_background, off
set cartoon_transparency, 0.2

# --- 3) DNA-binding domain (residues 94-292) ---
select dna_binding, resi 94-292
color blue, dna_binding
set cartoon_transparency, 0.3, dna_binding

# --- 4) Human hotspotlar ---
select hotspots, resi 175+245+248+249+273+282
color red, hotspots
show sticks, hotspots

# --- 5) Görüntüyü optimize et ---
orient
zoom

# --- 6) PNG kaydet ---
png C:/Users/PC/Desktop/p53_evolution/p53_hotspots.png, dpi=300
