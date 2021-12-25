import os
from pathlib import Path

from ProjectDecima import ArchiveManager
from ProjectDecima.core.core_entry_handler_manager import EntryTypeManager
from ProjectDecima.utils.dsjson_serializer import DSJsonSerializer


def main():
    EntryTypeManager.load_handlers('./ProjectDecima/core/entry_types/')
    archive_dir = Path(input('Folder with archives: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\data')
    print(f'Loading archives from "{archive_dir}"')
    dump_dir = Path(input('Output path: ') or r'F:\SteamLibrary\steamapps\common\Death Stranding\dump')
    print(f'Dumping files to "{archive_dir}"')
    ar_set = ArchiveManager(archive_dir)
    ar_set.parse_all()
    while 1:
        core_file_path = input(
            'Core file path: ') or "localized/sentences/ds_lines_common/lines_1p5_dsp_global/sentences.core"
        if not core_file_path:
            break
        core_file_path = core_file_path.replace('\\', '/')
        file = ar_set.queue_file(core_file_path, True)
        os.makedirs((dump_dir / Path(core_file_path).with_suffix('')), exist_ok=True)
        file_dump_path = dump_dir / Path(core_file_path).with_suffix('')
        for entry in file.entries:
            if not entry.exportable:
                continue
            DSJsonSerializer.begin(dump_dir, file_dump_path.with_suffix('.ds_json'))
            DSJsonSerializer.add_object(entry)
            with file_dump_path.with_suffix('.ds_json').open('w', encoding='utf-8') as f:
                import json
                json.dump(DSJsonSerializer.finalize(), f, indent=1, ensure_ascii=False)

            # entry_dump_path = file_dump_path
            # os.makedirs(entry_dump_path, exist_ok=True)
            # entry.export(entry_dump_path)


if __name__ == '__main__':
    main()
