"""
Script to convert FabriCost_Logo.png to .ico format for Windows executable.
Run this once before building the installer.
"""
from PIL import Image

def create_icon():
    """Convert PNG logo to ICO format with multiple sizes."""
    try:
        # Open the logo
        img = Image.open("FabriCost_Logo.png")
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create icon with multiple sizes (Windows standard)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Save as ICO
        img.save(
            "FabriCost_Icon.ico",
            format='ICO',
            sizes=icon_sizes
        )
        
        print("[SUCCESS] Created FabriCost_Icon.ico")
        print("Icon sizes included: 16x16, 32x32, 48x48, 64x64, 128x128, 256x256")
        
    except Exception as e:
        print(f"[ERROR] Error creating icon: {e}")
        print("\nMake sure FabriCost_Logo.png exists in the current directory.")

if __name__ == "__main__":
    create_icon()

