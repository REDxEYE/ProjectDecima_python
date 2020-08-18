from pathlib import Path

from ProjectDecima.archive.archive_array import ArchiveSet
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core_file import CoreFile
from ProjectDecima.archive.archive import Archive


def test_core_files():
    # folder = r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\models\characters\sam_sam\core\sam_body_naked\model\parts"
    folder = r'F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\models\characters\sam_sam\core\sam_textures\textures'
    for file in Path(folder).rglob('*.core'):
        c = CoreFile(file)
        c.parse()
        EntryReference.resolve(c, None)
        print(c)


def test_archives():
    archive_path = r"F:\SteamLibrary\steamapps\common\Death Stranding\data\7017f9bb9d52fc1c4433599203cc51b1.bin"
    archive = Archive(archive_path)
    archive.parse()
    a = archive.queue_file("ds/models/characters/sam_sam/core/sam_body_naked/model/parts/mesh_bodynaked_lx.core")
    if a:
        a.parse()
    print(a)
    pass


def test_archive_set():
    work_dir = r"F:\SteamLibrary\steamapps\common\Death Stranding\data"
    arch_set = ArchiveSet(work_dir)
    arch_set.parse_all()
    a = arch_set.queue_file("ds/models/characters/sam_sam/core/sam_textures/textures/sam_body_naked_v01_set.core")
    if a:
        EntryReference.resolve(a, arch_set)
        print(a)


if __name__ == '__main__':
    test_core_files()
    # test_archives()
    # test_archive_set()
