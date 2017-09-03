import os
import shutil
import pickle
from pprint import pprint

from lib.bdt_file import BDTFile
from lib.bhd5_file import BHD5File
from lib.bnd3_file import BND3File
from lib.tpf_file import TPFFile
from lib.dcx_file import DCXFile


extract_base_dir = os.path.abspath("./test")
output_base_dir = os.path.abspath("./test_output")


def dir_prep(base_dir):
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.mkdir(base_dir)


def do_read_test(filename, cls):
    dir_prep(extract_base_dir)
    manifest = cls(open(filename, "rb"), filename).extract_file(extract_base_dir)
    #pprint(manifest)
    return manifest


def do_write_test(filename, manifest, cls):
    dir_prep(output_base_dir)
    cls(open(filename, "wb"), filename).create_file(manifest)


def do_read_write_test(filename, cls):
    manifest = do_read_test(os.path.join("..", filename), cls)
    do_write_test(os.path.join(output_base_dir, filename), manifest, cls)
    do_read_test(os.path.join(output_base_dir, filename), cls)

    manifest_filename = os.path.join(output_base_dir, "manifest")
    pickle.dump(manifest, open(manifest_filename, "wb"))

tpf_file = "o1470"
#tpf_file = "c3320"
bnd3_file = "o1470.objbnd"
#bnd3_file = "item.objbnd"
dcx_file = bnd3_file
#dcx_file = "m18_00_00_00.emeld"
bdt_file = "dvdbnd1"

test = "bdt"

if test == "tpf":
    do_read_write_test(tpf_file + ".tpf", TPFFile)
elif test == "bnd3":
    do_read_write_test(bnd3_file + ".bnd3", BND3File)
elif test == "bhd5":
    do_read_write_test(bdt_file + ".bhd5", BHD5File)
elif test == "bdt":
    do_read_write_test(bdt_file + ".bdt", BDTFile)
elif test == "dcx":
    do_read_write_test(dcx_file + ".dcx", DCXFile)

#print(get_hash_from_string("/param/GeneratorParam_m10_02_00_00.param"))
