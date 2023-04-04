import torch
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)

num_cols = 3
num_rows = 4
prompt = [
             "The girl had just come out of the bath, and she was wearing only a pair of socks, showing her beautiful white figure"
         ] * num_cols
all_images = []
for i in range(num_rows):
    images = pipe(prompt).images
    all_images.extend(images)

grid = image_grid(all_images, rows=num_rows, cols=num_cols)
grid.show()
