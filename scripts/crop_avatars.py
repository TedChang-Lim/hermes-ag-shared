import os
from PIL import Image, ImageDraw, ImageOps

def crop_to_circle(image_path, output_path, size=200):
    if not os.path.exists(image_path):
        print(f"Error: {image_path} does not exist.")
        return False
        
    img = Image.open(image_path)
    # Ensure it's in RGBA mode for transparency
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
        
    width, height = img.size
    min_dim = min(width, height)
    
    # We crop a square from the center of the image
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    
    img_square = img.crop((left, top, right, bottom))
    
    # Create a circular mask
    mask = Image.new('L', img_square.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img_square.size, fill=255)
    
    # Put mask as alpha layer
    img_square.putalpha(mask)
    
    # Resize to the final size
    img_resized = img_square.resize((size, size), Image.Resampling.LANCZOS)
    
    # Save as transparent PNG
    img_resized.save(output_path, 'PNG')
    print(f"Successfully created circular avatar: {output_path}")
    return True

if __name__ == '__main__':
    templates_dir = '/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/templates'
    
    # Image 1 (media__1781361825281.jpg) -> Haena (Woman)
    haena_src = os.path.join(templates_dir, 'media__1781361825281.jpg')
    haena_dst = os.path.join(templates_dir, 'haena_avatar.png')
    crop_to_circle(haena_src, haena_dst)
    
    # Image 2 (media__1781361825298.png) -> AG (Man)
    ag_src = os.path.join(templates_dir, 'media__1781361825298.png')
    ag_dst = os.path.join(templates_dir, 'ag_avatar.png')
    crop_to_circle(ag_src, ag_dst)
