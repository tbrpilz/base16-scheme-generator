from colorific import extract_colors
from colour import Color
from PIL import Image

import os, random

def showPreview(preview):
  preview.show()

def genPreview(scheme, img=None):
  color_boxes = [Image.new("RGB", (64,64), tuple(round(v*255) for v in color.rgb)) 
                  for color in scheme]
  width = 64*len(scheme)
  scheme_preview=Image.new('RGB', (width, 64))

  # Create wallpaper thumbnail and pad preview
  if img is not None:
    img.thumbnail((width, img.size[1]))
    width, height = img.size
    scheme_preview = scheme_preview.crop((0,0,width,height+64))
    scheme_preview.paste(im=img, box=(0,64))

  for index, color_box in enumerate(color_boxes):
    scheme_preview.paste(im=color_box, box=(index*64, 0))

  return scheme_preview

# Color palette with all dominant colors and their prominence
def genPalette(img):
  (rest, background) = extract_colors(
      img,
      min_saturation=0,
      n_quantized=55
  )
  return rest.append(background) if background is not None else rest

# Base 16 Scheme
def genScheme(palette):
  # gen color object
  colors = [Color(rgb=tuple(v/255 for v in color.value)) for color in palette]

  # Sort by luminance
  luminance_gradient = sorted(colors, key=lambda c: c.luminance)

  return luminance_gradient

if(__name__ == '__main__'):
  folder_path = '/home/lvncelot/Pictures/wal/'

  img_names = os.listdir(folder_path)

  img_name = img_names[0]
#img_name = random.choice(img_names)

  img = Image.open(folder_path+img_name)

  palette = genPalette(img)
  scheme = genScheme(palette)

  preview = genPreview(scheme, img=img)

  preview.show()
