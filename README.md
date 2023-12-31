# FSS0 Extractor

A simple python script to extract the contents out of Fusée Secondary binary file.

## Usage

```
fss0-extractor.py [-h] input output

positional arguments:
  input       Location of the fusee-secondary.bin file.
  output      Location to extract files

optional arguments:
  -h, --help  show this help message and exit
```

## FSS0 File Structure


| Offset | Size     | Description                           |
| ------ | -------- | ------------------------------------- |
| 0x0    | 0x4      | Instruction to branch to startup code |
| 0x4    | 0x4      | Offset of header                      |
| 0x8    |          | Startup code                          |

### Header

| Offset | Size  | Description                          |
| ------ | ----- | ------------------------------------ |
| 0x0    | 0x4   | Magicnum "FSS0"                      |
| 0x4    | 0x4   | Size of the entire file              |
| 0x8    | 0x4   | Offset of startup code               |
| 0xC    | 0x4   | Offset of content headers            |
| 0x10   | 0x4   | Number of content headers            |
| 0x14   | 0x4   | Maximum Horizon OS Supported         |
| 0x18   | 0x4   | Atmosphere Version                   |
| 0x1C   | 0x4   | First four bytes of the git revision | 

### Content Header

| Offset | Size  | Description       |
| ------ | ----- | ----------------- |
| 0x0    | 0x4   | Offset of content |
| 0x4    | 0x4   | Size of content   |
| 0x8    | 0x1   | Type              |
| 0x9    | 0x1   | First flag        |
| 0xA    | 0x1   | Second flag       |
| 0xB    | 0x1   | Third flag        |
| 0xC    | 0x4   | Reserved          |
| 0x10   | 0x10  | Name              |

### Content Header Types

| Value | Description    |
| ----- | -------------- |
| 0x0   | Fusee Primary  |
| 0x1   | Exosphere      |
| 0x2   | LP0 Firmware   |
| 0x3   | Reboot Stub    |
| 0x4   | Sept Primary   |
| 0x5   | Sept Secondary |
| 0x6   | KIP            |
| 0x7   | Bitmap         |
| 0x8   | EmuMMC         |
| 0x9   | Kernel Loader  |
| 0xA   | Kernel         |

### Content Header Flags

| Value | Description  |
| ----- | ------------ |
| 0x0   | None         |
| 0x1   | Experimental |