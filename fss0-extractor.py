#!/usr/bin/env python3
#
# FSS0 Extractor
# Copyright (C) 2020 Nichole Mattera
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Location of the fusee-secondary.bin file.")
    parser.add_argument("output", help="Location to extract files")

    # Parse arguments
    return parser.parse_args()


def getExtension(type: int):
    if (type >= 0 and type <= 4) or (type >= 9 and type <= 10):
        return "bin"
    elif type == 5:
        return "enc"
    elif type == 6 or type == 8:
        return "kip"
    elif type == 7:
        return "bmp"


if __name__ == "__main__":
    args = parse_args()

    if not Path(args.input).exists():
        print("[ERROR] Fusee Secondary does not exists.")
        sys.exit()

    fusee_secondary = open(args.input, "rb")
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Skip branch instruction.
    fusee_secondary.seek(0x4)

    # Get the header offset
    header_offset = int.from_bytes(fusee_secondary.read(0x4), byteorder="little")
    fusee_secondary.seek(header_offset + 0xC)

    # Get content header information
    content_header_offset = int.from_bytes(
        fusee_secondary.read(0x4), byteorder="little"
    )
    number_of_content_headers = int.from_bytes(
        fusee_secondary.read(0x4), byteorder="little"
    )

    for i in range(0, number_of_content_headers):
        # Seek to the content header.
        fusee_secondary.seek(content_header_offset + (0x20 * i))

        # Get the offset, size and type.
        content_offset = int.from_bytes(fusee_secondary.read(0x4), byteorder="little")
        content_size = int.from_bytes(fusee_secondary.read(0x4), byteorder="little")
        content_type = int.from_bytes(fusee_secondary.read(0x1), byteorder="little")

        # Seek to the name
        fusee_secondary.seek(0x7, 1)
        name_bytes = fusee_secondary.read(0x10)
        name = ""

        # Trim the bytes for the name.
        if 0x0 in name_bytes:
            first_null = name_bytes.index(0x0)
            name = name_bytes[:first_null].decode("ascii")
        else:
            name = name_bytes.decode("ascii")

        # Extract the file
        fusee_secondary.seek(content_header["offset"])
        content = fusee_secondary.read(content_header["size"])
        name = f'{content_header["name"]}.{getExtension(content_header["type"])}'
        file = open(Path(args.output).joinpath(name), "wb")
        file.write(content)
        file.close()

    fusee_secondary.close()
