def calculate_first_containing_chunk(file_offset, chunk_size):
    return file_offset - (file_offset % chunk_size)


def calculate_last_containing_chunk(file_offset, file_size, chunk_size):
    return calculate_first_containing_chunk(file_offset + file_size, chunk_size)

