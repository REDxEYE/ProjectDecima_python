import os
from pathlib import Path

from ProjectDecima.archive.archive_array import ArchiveSet
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.stream_reference import StreamReference
from ProjectDecima.core.core_file import CoreFile
from ProjectDecima.archive.archive import Archive


def test_core_file():
    file = r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\sounds\wwise_cinematics_sound_resource\cs00\sq_cs00_s00100\sq_cs00_s00100_sound.core"
    c = CoreFile(file)
    c.parse()
    EntryReference.resolve(c, None)
    print(c)


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
    # a = arch_set.queue_file("ds/sounds/wwise_bnk_collections/sd_wwise_bnk_collection_game_resident.core")
    # EntryReference.resolve(a, arch_set)
    # StreamReference.resolve(arch_set)
    # pass
    folder = r'F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\sounds\wwise_bnk_collections'
    for file in Path(folder).rglob('*.core'):
        c = CoreFile(file)
        c.parse()
        EntryReference.resolve(c, arch_set)
        StreamReference.resolve(arch_set)
        for ent in c.entries:
            if ent.header.magic == 0xA664164D69FD2B38:
                ent.export(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump")
            elif ent.header.magic == 0x150c273beb8f2d0c:
                os.makedirs(
                    Path(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump") / c.filepath.with_suffix('') / str(
                        ent.header.guid.__str__()), exist_ok=True)
                ent.export(
                    Path(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump") / c.filepath.with_suffix('') / str(
                        ent.header.guid.__str__()))
        pass


if __name__ == '__main__':
    test_core_file()
    # test_core_files()
    # test_archives()
    # test_archive_set()
