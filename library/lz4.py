from __future__ import print_function
import os
from lz4framed import *
from sys import argv, stderr
def __error(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def do_compress(in_stream, out_stream):
    read = in_stream.read
    read_size = get_block_size()
    try:
        with Compressor(out_stream, level=6) as compressor:
            try:
                while True:
                    compressor.update(read(read_size))
            # empty read result supplied to update()
            except Lz4FramedNoDataError:
                pass
            # input stream exception
            except EOFError:
                pass
    except Lz4FramedError as ex:
        __error('Compression error: %s' % ex)
        return 8
    return 0

def do_decompress(in_stream, out_stream):
    write = out_stream.write
    try:
        for chunk in Decompressor(in_stream):
            write(chunk)
    except Lz4FramedError as ex:
        __error('Compression error: %s' % ex)
        return 8
    return 0

def docomp(filename):
    filename_out = filename.replace('.ms2', '.mz4')
    in_file = open(filename, 'rb')
    out_file = open(filename_out, 'ab')
    do_compress(in_file, out_file)
    in_file.close()
    out_file.close()
    os.remove(filename)

def dodecomp(filename):
    filename_out = filename.replace('npy.lz4', 'npy')
    in_file = open(filename, 'rb')
    out_file = open(filename_out, 'ab')
    do_decompress(in_file, out_file)
    in_file.close()
    out_file.close()
    os.remove(filename)