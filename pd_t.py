from pathlib import Path

from ProjectDecima.core_file import CoreFile
from ProjectDecima.archive.archive import Archive


def test_core_files():
    for file in Path(
            r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\models\characters\sam_sam\core\sam_body_naked\model\parts").rglob(
        '*.core'):
        c = CoreFile(file)
        c.parse()
        print(c)


def test_archives():
    archive_path = r"F:\SteamLibrary\steamapps\common\Death Stranding\data\0404fe2210c6609046c1c08bf2ea7c8a.bin"
    arhive = Archive(archive_path)
    arhive.parse()
    print(arhive)
    pass


if __name__ == '__main__':
    # test_core_files()
    test_archives()
