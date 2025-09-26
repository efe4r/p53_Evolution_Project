from PIL import Image, ImageDraw, ImageFont
import textwrap

# PNG dosyaları ve açıklamaları
png_files = [
    "p53_conservation.png",
    "p53_conservation_hotspots_domains.png",
    "p53_tree.png"
]
labels = ['A', 'B', 'C']
descriptions = [
    "Shows the evolutionary conservation of the p53 protein across multiple species. Highly conserved regions are indicative of critical functional importance, whereas variable regions may reflect species-specific adaptations.",
    "Highlights key mutational hotspots along the p53 protein sequence as well as the annotated functional domains. This visualization helps identify regions critical for DNA binding, tetramerization, and regulatory activity.",
    "Represents the phylogenetic relationships among p53 sequences from different organisms. Branch lengths reflect evolutionary distances, providing insights into p53 divergence and conservation across species."
]

# Logo veya kaynak (isteğe bağlı)
source_text = "Created by Efe Can Orhan | 2025 | GitHub/Zenodo"

# Görselleri aç
images = [Image.open(f) for f in png_files]

# Maksimum genişlik ve toplam yükseklik
max_width = max(img.width for img in images)
font_size = 26
line_height = 32
spacing = 240  # kutucuk ve gölge için ekstra boşluk

images_resized = [img.resize((max_width, int(img.height * max_width / img.width))) for img in images]
total_height = sum(img.height for img in images_resized) + spacing * len(images) + 50  # kaynak için ekstra alan

# Beyaz arka plan
combined = Image.new('RGB', (max_width, total_height), color=(255,255,255))
draw = ImageDraw.Draw(combined)

# Font
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

y_offset = 0
for img, label, desc in zip(images_resized, labels, descriptions):
    combined.paste(img, (0, y_offset))
    
    # Etiket
    draw.text((10, y_offset + 10), label, fill="black", font=font)
    
    # Açıklamayı satırlara böl
    lines = textwrap.wrap(desc, width=100)
    
    # Kutucuk boyutu
    bbox_height = line_height * len(lines) + 20
    bbox_y_start = y_offset + img.height + 5
    bbox_color = (230, 230, 230)  # açık gri
    shadow_color = (180, 180, 180)  # gölge
    shadow_offset = 5
    
    # Gölge
    draw.rectangle([shadow_offset, bbox_y_start+shadow_offset,
                    max_width+shadow_offset, bbox_y_start + bbox_height + shadow_offset],
                   fill=shadow_color)
    # Kutucuk
    draw.rectangle([0, bbox_y_start, max_width, bbox_y_start + bbox_height], fill=bbox_color, outline="black", width=1)
    
    # Metin
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (max_width - w) // 2
        draw.text((x, bbox_y_start + 10 + i*line_height), line, fill="black", font=font)
    
    y_offset += img.height + spacing

# Kaynak / logo ekle
source_font_size = 18
try:
    source_font = ImageFont.truetype("arial.ttf", source_font_size)
except:
    source_font = ImageFont.load_default()
bbox = draw.textbbox((0,0), source_text, font=source_font)
w = bbox[2] - bbox[0]
x = (max_width - w) // 2
draw.text((x, total_height - 40), source_text, fill="black", font=source_font)

# Kaydet
combined.save("p53_figures_final.png", dpi=(300,300))
print("✅ p53_figures_final.png oluşturuldu! Tamamen yayın-ready figür hazır.")
