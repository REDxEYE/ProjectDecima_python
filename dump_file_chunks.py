from struct import pack

from ProjectDecima import ArchiveManager, Archive
from ProjectDecima.utils.decryption import hash_string, decrypt_chunk_data
from ProjectDecima.archive.archive import ArchiveEntry, ArchiveChunk
from ProjectDecima.utils.oodle_wrapper import Oodle

ar_set = ArchiveManager(r'F:\SteamLibrary\steamapps\common\Death Stranding\data')
ar_set.parse_all()
file_to_dump = 'interface/textures/ds/image_display/ut_ui_m00650_title.core'
file_hash = hash_string(file_to_dump)
archive: Archive = ar_set.hash_to_archive.get(file_hash, None)
if not archive:
    print("Failed to find file")
    exit()

entry: ArchiveEntry = archive.hash_to_entry.get(file_hash, None)
if not entry:
    print("Failed to find file")
    exit()

print(f"File found in {archive.filepath.stem} archive")
chunk_ranges = archive.get_chunk_boundaries(file_hash)
first_chunk: ArchiveChunk = archive.chunks[chunk_ranges[0]]
last_chunk: ArchiveChunk = archive.chunks[chunk_ranges[1]]
print(f"First chunk: {chunk_ranges[0]} offset: 0x{first_chunk.compressed_offset:X}\n"
      f"Last chunk {chunk_ranges[1]} offset: 0x{last_chunk.compressed_offset:X}")
# for i in range(chunk_ranges[0], chunk_ranges[1] + 1):
#     chunk = archive.chunks[i]
#     archive.reader.seek(chunk.compressed_offset)
#     chunk_data = archive.reader.read_bytes(chunk.compressed_size)
#     if archive.is_encrypted:
#         key = pack('Q2I', chunk.uncompressed_offset, chunk.uncompressed_size, chunk.key_0)
#         chunk_data = decrypt_chunk_data(chunk_data, key)
#         decompressed_data = Oodle.decompress(chunk_data, chunk.uncompressed_size)
