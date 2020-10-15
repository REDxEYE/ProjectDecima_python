import os
from pathlib import Path

from ProjectDecima.archive.archive_manager import ArchiveManager
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.core.entry_reference import EntryReference
from ProjectDecima.core.stream_reference import StreamingDataSource
from ProjectDecima.core.core_file import CoreFile
from ProjectDecima.archive.archive import Archive
from ProjectDecima.utils.dsjson_serializer import DSJsonSerializer

def test_archive_set():
    work_dir = r"F:\SteamLibrary\steamapps\common\Death Stranding\data"
    arch_set = ArchiveManager(work_dir)
    arch_set.parse_all()

    file = Path(
        r"F:\SteamLibrary\steamapps\common\Death Stranding\dump\levels\worlds\_l000_area00\leveldata.core"
        # r"F:\SteamLibrary\steamapps\common\Death
        # Stranding\dump\localized\sentences\ds_lines_sam\lines_sam\sentences.core"
        # r"F:\SteamLibrary\steamapps\common\Death
        # Stranding\dump\ds\models\characters\sam_sam\core\sam_body_naked\model\parts\mesh_bodynaked_lx.core"
        # r"ds/artparts/characters/hgs_higgs/part_hgs_body_def.core" r"F:\SteamLibrary\steamapps\common\Death
        # Stranding\dump\ds\artparts\characters\sam_sam\part_sam_body_suiti.core"
        # r"F:\SteamLibrary\steamapps\common\Death
        # Stranding\dump\ds\models\characters\sam_sam\core\sam_body_naked\model\parts\mesh_upperbody_lx.core"
        # r"F:\SteamLibrary\steamapps\common\Death
        # Stranding\dump\ds\models\characters\sam_sam\core\sam_body_naked\model\skeletons
        # \skeleton_jnt_c_b_000_root_helpers.core" r"F:\SteamLibrary\steamapps\common\Death
        # Stranding\dump\ds\sounds\wwise_bnk_collections\sd_wwise_bnk_collection_game_resident.core"
        # "ds/sounds/systems/sd_ds_facts"
        # "ds/models/characters/sam_sam/core/sam_body_naked/model/parts/mesh_upperbody_lx.core"
        # "ds/sounds/systems/sd_system_submix_settings"
        # "ds/models/characters/sam_sam/core/sam_textures/textures/sam_body_naked_v01_set"
        # "ds/models/characters/sam_sam/core/sam_textures/textures/sam_body_subpouch_v00_set.core"
        # "localized/sentences/ds_lines_sam/lines_sam/sentences.core" "ds/archives/music_player_resource.core"
    )
    if file.is_dir():
        for file in Path(file).rglob('*.core'):
            core_file = CoreFile(file)
            core_file.parse()
            pass
    elif file.is_file():
        core_file = CoreFile(file)
        core_file.parse()

        pass
    else:
        core_file = arch_set.queue_file(file.as_posix(), True)
        print(core_file)

        pass


if __name__ == '__main__':
    EntryTypeManager.load_handlers('./ProjectDecima/core/entry_types/')
    test_archive_set()
