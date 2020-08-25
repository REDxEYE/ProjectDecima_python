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
    print(c)


def test_core_files():
    # folder = r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\models\characters\sam_sam\core\sam_body_naked\model\parts"
    folder = r'F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\models\characters\sam_sam\core\sam_textures\textures'
    for file in Path(folder).rglob('*.core'):
        c = CoreFile(file)
        c.parse()

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

    file = Path(
        # r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\entities\player\variant\ds_player_variant_sam_body_suit.core")
        r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\ds\models\characters\sam_sa~~m\core\sam_body_naked\model\parts\mesh_bodynaked_lx.core")

    if file.is_dir():
        for file in Path(file).rglob('*.core'):
            core_file = CoreFile(file)
            core_file.parse()
            EntryReference.resolve(arch_set)
            StreamReference.resolve(arch_set)
            for ent in core_file.entries:
                if ent.header.magic == 0xA664164D69FD2B38:
                    ent.export(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump")
                elif ent.header.magic == 0x150c273beb8f2d0c:
                    os.makedirs(
                        Path(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump") / core_file.filepath.with_suffix(
                            '') / str(
                            ent.header.guid.__str__()), exist_ok=True)
                    ent.export(
                        Path(r"F:\SteamLibrary\steamapps\common\Death Stranding\dump") / core_file.filepath.with_suffix(
                            '') / str(
                            ent.header.guid.__str__()))
            pass
    else:
        core_file = CoreFile(file)
        core_file.parse()
        EntryReference.resolve(arch_set)
        while EntryReference.dirty:
            EntryReference.resolve(arch_set)
        StreamReference.resolve(arch_set)
        pass


if __name__ == '__main__':
    # test_core_file()
    # test_core_files()
    # test_archives()
    test_archive_set()
