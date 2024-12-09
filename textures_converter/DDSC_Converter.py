import struct
import sys
from folder_analyzer import FolderAnalyzer
from DDSC_compressions import compressions
from colors import *

def ddsc_converter(texture_path: str, mode: str = "srgb"):
    """Converts between .dds and .ddsc files."""
    with open(texture_path, 'rb') as f:
        file_bytes = f.read()

    if texture_path.endswith('.dds'):
        height = struct.unpack_from('<H', file_bytes, 0x0c)[0]
        width = struct.unpack_from('<H', file_bytes, 0x10)[0]
        mip_levels = file_bytes[0x1c]
        four_byte_string = file_bytes[0x54:0x58].decode('ascii')

        print(f"Height: {height}")
        print(f"Width: {width}")
        print(f"Mip Levels: {mip_levels}")
        print(f"4-byte String: {four_byte_string}")

        int8_value = compressions.get(four_byte_string)
        if int8_value is None:
            raise ValueError(f"Unsupported compression format: {four_byte_string}")

        new_header = bytearray(128)
        template = bytearray([0x41, 0x56, 0x54, 0x58, 0x01, 0x00, 0x08, 0x02, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        new_header[:len(template)] = template
        new_header[0x08] = int8_value
        new_header[0x0c:0x0e] = struct.pack('<H', width)
        new_header[0x0e:0x10] = struct.pack('<H', height)
        new_header[0x14] = mip_levels
        new_header[0x15] = mip_levels

        if mode == 'srgb':
            new_header[0x12] = 0x09

        offset_value = len(file_bytes) - 128
        new_header[0x24:0x28] = struct.pack('<I', offset_value)

        new_file_path = texture_path.rsplit('.', 1)[0] + ".ddsc"
        with open(new_file_path, 'wb') as f:
            f.write(new_header + file_bytes[128:])
        print(f"New file created: {new_file_path}\n")

    elif texture_path.endswith('.ddsc'):
        is_dds = file_bytes[0x00:0x03].decode('ascii')
        if is_dds == "DDS":
            new_file_path = texture_path.rsplit('.', 1)[0] + ".dds"
            print("The current file is a DDS but with a ddsc extension")
            with open(new_file_path, 'wb') as f:
                f.write(file_bytes)
        else:
            texture_compression = struct.unpack_from('<H', file_bytes, 0x08)[0]
            height = struct.unpack_from('<H', file_bytes, 0x0e)[0]
            width = struct.unpack_from('<H', file_bytes, 0x0c)[0]
            mip_levels = file_bytes[0x14]

            compression_name = next((name for name, value in compressions.items() if value == texture_compression), None)
            if compression_name is None:
                raise ValueError(f"Unsupported texture compression: {texture_compression}")

            print(f"Texture compression: {compression_name}")
            print(f"Height: {height}")
            print(f"Width: {width}")
            print(f"Mip Levels: {mip_levels}")

            new_header = bytearray(128)
            template = bytearray([0x44, 0x44, 0x53, 0x20, 0x7C, 0x00, 0x00, 0x00, 0x07, 0x10, 0x0A, 0x00,
                                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                  0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            new_header[:len(template)] = template
            new_header[0x54:0x58] = compression_name.encode("ascii")
            new_header[0x10:0x12] = struct.pack('<H', width)
            new_header[0x0c:0x0e] = struct.pack('<H', height)
            new_header[0x1c] = mip_levels

            new_file_path = texture_path.rsplit('.', 1)[0] + ".dds"
            with open(new_file_path, 'wb') as f:
                f.write(new_header + file_bytes[128:])
            print(f"New file created: {new_file_path}\n")

    else:
        raise ValueError(f"Unsupported file type for conversion: {texture_path}\n")


if __name__ == "__main__":
    paths = sys.argv[1:]
    textures = FolderAnalyzer(paths)
    if textures.exists:
        try:
            for texture in textures.file_list:
                ddsc_converter(texture)
            input(GREEN + "Process Successful, press enter to exit." + RESET)
        except Exception as e:
            print(RED + f"Error : {e}" + RESET)
            input(RED + "Process Failed, press enter to exit." + RESET)
