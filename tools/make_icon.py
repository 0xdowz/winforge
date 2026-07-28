import os
from pathlib import Path
from PIL import Image

def generate_multi_res_icon():
    project_root = Path(__file__).resolve().parent.parent
    assets_dir = project_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    ico_path = assets_dir / "icon.ico"
    if not ico_path.exists():
        print(f"[ERROR] Icon not found at {ico_path}")
        return False
        
    base_img = Image.open(ico_path).convert("RGBA")
    
    # Standard Windows ICO resolutions
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    base_img.save(ico_path, format="ICO", sizes=sizes)
    
    print(f"[SUCCESS] Multi-resolution Windows ICO saved at: {ico_path}")
    print(f" -> File Size: {ico_path.stat().st_size} bytes")
    return True

if __name__ == "__main__":
    generate_multi_res_icon()
