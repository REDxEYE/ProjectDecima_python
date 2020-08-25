from PIL import Image

pixel_type = 0x42

t = {0x42: 1,
     0x43: 2,
     0x44: 3,
     0x45: 4,
     0x47: 5,
     0x4B: 7, }[pixel_type]
width = 4096
height = 4096
with open(
        r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\levels\worlds\_l000_area00\lods\cmbnd_flttnd_hght_68e1761f_001.core.stream",
        'rb') as f:
    im = Image.frombytes('RGBA', (width, height), f.read(-1), 'bcn', 5)
    im.convert('RGB').save(f'test.png')
