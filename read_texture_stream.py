from PIL import Image

pixel_type = 0x42

t = {0x42: 1,
     0x43: 2,
     0x44: 3,
     0x45: 4,
     0x47: 5,
     0x4B: 7, }[pixel_type]
width = 512
height = 512
with open(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\textures\library\rock\dslchn_sngl_clr_8275bfa9_001.core.stream",
        'rb') as f:
    im = Image.frombytes('RGBA', (width, height), f.read(-1), 'bcn', t, 0)
    im.convert('RGB').save(f'test.png')
