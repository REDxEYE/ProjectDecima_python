from pathlib import Path

from ProjectDecima.core_file import CoreFile

if __name__ == '__main__':
    for file in Path(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\models\characters\sam_sam\core\sam_body_naked\model\parts").rglob('*.core'):
        c = CoreFile(file)
        c.parse()
        print(c)
