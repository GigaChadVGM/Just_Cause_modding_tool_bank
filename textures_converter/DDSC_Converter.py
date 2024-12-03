import struct
import sys

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

try:
    from folder_analyzer import FolderAnalyzer
except ImportError as e:
    print(RED + f"\nError importing FolderAnalyser: {e}" + RESET)
    input(RED + "Process Failed, press enter to exit." + RESET)
    sys.exit(1)


def dds_to_ddsc(dds_path: str, mode: str = "srgb"):
    """Converts any dds as ddsc, based on Brooen's script, user account: https://github.com/brooen/"""
    with open(dds_path, 'rb') as f:
        file_bytes = f.read()

    height = struct.unpack_from('<H', file_bytes, 0x0c)[0]
    width = struct.unpack_from('<H', file_bytes, 0x10)[0]
    mip_levels = file_bytes[0x1c]
    four_byte_string = file_bytes[0x54:0x58].decode('ascii')

    print(f"Height: {height}")
    print(f"Width: {width}")
    print(f"Mip Levels: {mip_levels}")
    print(f"4-byte String: {four_byte_string}")

    if four_byte_string == "ATI2":
        int8_value = 83
    elif four_byte_string == "ATI1":
        int8_value = 80
    elif four_byte_string == "DXT1":
        int8_value = 71
    elif four_byte_string == "DXT3":
        int8_value = 74
    elif four_byte_string == "DXT5":
        int8_value = 77
    else:
        raise f"Unknown 4-byte string: {four_byte_string}"

    new_header = bytearray(128)

    template = bytearray([0x41, 0x56, 0x54, 0x58, 0x01, 0x00, 0x08, 0x02, 0x00, 0x00, 0x00, 0x00,
                          0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00,
                          0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
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

    file_length = len(file_bytes)
    offset_value = file_length - 128
    offset_bytes = struct.pack('<I', offset_value)

    new_header[0x24:0x28] = offset_bytes

    new_file_path = dds_path.rsplit('.', 1)[0] + ".ddsc"
    with open(new_file_path, 'wb') as f:
        f.write(new_header + file_bytes[128:])

    print(f"New file created: {new_file_path}")

def ddsc_to_dds(ddsc_path: str):
    """Coverts any ddsc back to a dds"""
    with open(ddsc_path, 'rb') as f:
        file_bytes = f.read()

    is_dds = file_bytes[0x00:0x03].decode('ascii')

    if is_dds == "DDS":
        new_file_path = ddsc_path.rsplit('.', 1)[0] + ".dds"
        print("the current file is a DDS but with a ddsc extension")
        print(f"the new file has been created at {new_file_path}")
        with open(new_file_path, 'wb') as f:
            f.write(file_bytes)
    else:
        texture_compression = struct.unpack_from('<H', file_bytes, 0x08)[0]
        height = struct.unpack_from('<H', file_bytes, 0x0e)[0]
        width = struct.unpack_from('<H', file_bytes, 0x0c)[0]
        mip_levels = file_bytes[0x14]

        if texture_compression == 71:
            texture_compression = "DXT1"
        elif texture_compression == 74:
            texture_compression = "DXT3"
        elif texture_compression == 77:
            texture_compression = "DXT5"
        elif texture_compression == 80:
            texture_compression = "ATI1"
        elif texture_compression == 83:
            texture_compression = "ATI2"
        else:
            raise f"Unknown texture compression: {texture_compression}"

        print(f"Texture compression: {texture_compression}")
        print(f"Height: {height}")
        print(f"Width: {width}")
        print(f"Mip Levels: {mip_levels}")
    
    
        new_header = bytearray(128)

        template = bytearray([0x44, 0x44, 0x53, 0x20, 0x7C, 0x00, 0x00, 0x00, 0x07, 0x10, 0x0A, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        new_header[:len(template)] = template

        text_bytes = texture_compression.encode("ascii")
        total_size = width + height
        if mip_levels > 1:
            new_header[0x6c] = 0x08
            new_header[0x6e] = 0x40
        new_header[0x6d] = 0x10
        new_header[0x54:0x58] = text_bytes
        new_header[0x10:0x12] = struct.pack('<H', width)
        new_header[0x15:0x17] = struct.pack('<H', total_size)
        new_header[0x0c:0x0e] = struct.pack('<H', height)
        new_header[0x1c] = mip_levels

        new_file_path = ddsc_path.rsplit('.', 1)[0] + ".dds"
        with open(new_file_path, 'wb') as f:
            f.write(new_header + file_bytes[128:])

        print(f"New file created: {new_file_path}")

if __name__ == "__main__":
    paths = sys.argv[1:]
    textures = FolderAnalyzer(paths)
    if textures.exists:
        try:
            for texture in textures.file_list:
                if texture.endswith('.dds'):
                    dds_to_ddsc(texture)
                elif texture.endswith('.ddsc'):
                    ddsc_to_dds(texture)
                else:
                    raise Exception(RED + "the tool cannot convert this type of file, only .ddsc or .dds." + RESET)
            input(GREEN + "\nProcess Successful, press enter to exit." + RESET)

        except Exception as e:
            print(RED + f"\nError : {e}" + RESET)
            input(RED + "Process Failed, press enter to exit." + RESET)
