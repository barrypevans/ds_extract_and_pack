import os
import hashlib

from . import bdt_file, tpf_file, dcx_file, bnd3_file


def class_for_data(data):
    classes_to_check = [bnd3_file.BND3File, tpf_file.TPFFile, dcx_file.DCXFile, bdt_file.BDTFile]

    for file_cls in classes_to_check:
        if data.startswith(file_cls.MAGIC_HEADER):
            return file_cls
    return None


def write_data(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.isfile(filepath):
        self_digest = hashlib.md5(data).hexdigest()
        other_digest = hashlib.md5(open(filepath, "rb").read()).hexdigest()
        if self_digest == other_digest:
            print("WARN: File already exists and has same hash: {}".format(filepath))
            return
        # This seems to only happen with *.sibcam and *.hkx files
        print("ERROR: File already exists and has different hash: {}".format(filepath))

    file = open(filepath, 'w+b')
    file.write(data)
    file.seek(0)
    return file
