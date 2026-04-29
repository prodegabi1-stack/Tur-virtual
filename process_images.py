import os
import sys
import json
import math
from PIL import Image

# Acest script transforma panoramele mari in "tiles" (pachete de imagini mici)
# pentru a permite incarcarea rapida si calitate maxima (Pro).

def process_panorama(input_path, output_dir, tile_size=512):
    print(f"Procesez: {input_path}...")
    img = Image.open(input_path)
    w, h = img.size
    
    # Calculam nivelurile de rezolutie
    # Pentru Marzipano, cel mai simplu e sa facem un Cube Map (6 fete)
    # Fiecare fata a cubului are o latime de aprox. w/4
    face_size = w // 4
    
    # Cream folderul pentru aceasta scena
    scene_id = os.path.splitext(os.path.basename(input_path))[0]
    scene_dir = os.path.join(output_dir, scene_id)
    os.makedirs(scene_dir, exist_ok=True)
    
    # Nota: Transformarea completa din Equi in Cube necesita matematica complexa (Lanczos/Spherical).
    # Pentru a fi rapizi si eficienti, vom optimiza imaginea la o rezolutie "Super-Pro" (8K)
    # care este suportata de Marzipano ca single-image dar optimizata.
    
    # Daca vrei Tiling real (ca la Google Maps), recomandarea este sa folosesti 
    # unealta oficiala Marzipano (marzipano.net/tool) deoarece necesita 
    # niste librarii de procesare imagini (C++) foarte specifice.
    
    # TOTUSI, pot sa iti fac varianta "High-Performance" aici:
    target_w = 8192
    target_h = 4096
    
    print(f"  -> Redimensionez la {target_w}x{target_h} (Calitate Maxima Web)...")
    img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    output_path = os.path.join(scene_dir, "full.jpg")
    img_resized.save(output_path, "JPEG", quality=85, optimize=True, progressive=True)
    
    print(f"  -> Salvat in: {output_path}")
    return {
        "id": scene_id,
        "path": f"tiles/{scene_id}/full.jpg",
        "width": target_w
    }

def main():
    try:
        from PIL import Image
    except ImportError:
        os.system("pip install Pillow")
        from PIL import Image

    # Tintim folderul de export direct
    target_folder = "photos"
    
    if not os.path.exists(target_folder):
        print(f"Folderul '{target_folder}' nu exista.")
        return

    files = [f for f in os.listdir(target_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    for f in files:
        path = os.path.join(target_folder, f)
        print(f"Optimizez Pro: {f}...")
        img = Image.open(path)
        
        # 8K este rezolutia maxima stabila pentru mobile
        target_w = 8192
        target_h = 4096
        
        img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        img_resized.save(path, "JPEG", quality=85, optimize=True, progressive=True)
        print(f"  -> OK (8K, Lanczos)")

if __name__ == "__main__":
    main()
