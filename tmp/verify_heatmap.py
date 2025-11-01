"""
Quick script to verify if red squares are in the heatmap
"""

from PIL import Image
import numpy as np

# Load the heatmap
img_path = 'data/output/figures/optimal_heatmap_all_results.png'

try:
    img = Image.open(img_path)
    img_array = np.array(img)

    # Check for red pixels (RGB values where R is high, G and B are low)
    # Red is approximately (255, 0, 0) but borders might be anti-aliased

    # Look for pixels that are predominantly red
    red_channel = img_array[:, :, 0]
    green_channel = img_array[:, :, 1]
    blue_channel = img_array[:, :, 2]

    # Count pixels where red is dominant
    red_pixels = np.sum((red_channel > 200) & (green_channel < 100) & (blue_channel < 100))

    print(f"Heatmap analysis:")
    print(f"  Image size: {img.size}")
    print(f"  Image mode: {img.mode}")
    print(f"  Red-ish pixels found: {red_pixels:,}")

    if red_pixels > 1000:  # Reasonable threshold for border pixels
        print(f"\n[OK] Red squares detected in heatmap!")
        print(f"     The red borders are present.")
    else:
        print(f"\n[WARNING] Very few red pixels detected!")
        print(f"          Red squares might be missing or very thin.")

    print(f"\nHeatmap location: {img_path}")
    print(f"You can open it manually to verify visually.")

except Exception as e:
    print(f"Error: {e}")
    print(f"\nTry opening the heatmap manually:")
    print(f"  {img_path}")
