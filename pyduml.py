#!/usr/bin/python
# HDnes pythonDUML
# Thanks the_lord for the sniffing
import os

from dji_crc import *
import struct

# Enter upgrade mode (delete old file if exists)
packet_1 = bytearray.fromhex(u'55 16 04 FC 2A 28 65 57 40 00 07 00 00 00 00 00 00 00 00 00 27 D3')
# Enable Reporting
packet_2 = bytearray.fromhex(u'55 0E 04 66 2A 28 68 57 40 00 0C 00 88 20')

# 551A04B12A286B5740000800YYYYYYYY0000000000000204XXXX
#YYYYYYYY - file size in little endian
#XXXX - CRC as produced by dji_crc.py

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/fireworks.tar"
# Pack file size into 4 byte Long little endian
file_size = struct.pack('<L',int(os.path.getsize(dir_path)))

packet_3 = bytearray.fromhex(u'55 1A 04 B1 2A 28 6B 57 40 00 08 00')
packet_3 += file_size #append file size
packet_3 += bytearray.fromhex(u'00 00 00 00 00 00 02 04')
#print ' '.join(format(x, '02X') for x in packet_3)

packet_length = len(packet_3)
crc = calc_checksum(packet_3,packet_length)
#print "%02X %02X" % (crc & 0xFF, crc >> 8)
crc = struct.pack('<H',crc)
packet_3 += crc
print ' '.join(format(x, '02X') for x in packet_3)