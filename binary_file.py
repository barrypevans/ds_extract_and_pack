import os


class BinaryFile:
    def __init__(self, file, path):
        self.file = file
        self.path = path
        self.endian = "little"

    def normalize_filepath(self, filepath):
        if self.path is None:
            raise RuntimeError("File path not given")
        if filepath.lower().startswith("n:\\"):
            filepath = filepath[3:]
        filepath = os.path.join(os.path.dirname(self.path), filepath.replace("\\", os.sep))
        return os.path.normpath(filepath)

    def write(self, *args):
        for arg in args:
            self.file.write(arg)

    def write_header(self, manifest):
        self.write(*manifest['header'].values())

    def read(self, num_bytes):
        return self.file.read(num_bytes)

    def consume(self, expected_bytes, num_to_read=None):
        if num_to_read:
            expected_bytes = expected_bytes.to_bytes(num_to_read, self.endian)
        else:
            num_to_read = len(expected_bytes)
        actual_bytes = self.read(num_to_read)
        if actual_bytes != expected_bytes:
            raise ValueError("Expected {}, got {}".format(expected_bytes, bytes))
        return actual_bytes

    def read_null_terminated_string(self):
        buffer = b""
        while True:
            byte = self.read(1)
            if byte == b'' or byte == b'\x00':
                break
            buffer += byte
        return buffer.decode("shift_jis")

    def write_data(self, filepath, data):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        open(filepath, 'wb').write(data)

    def int32_bytes(self, i):
        return i.to_bytes(4, byteorder=self.endian)

    def to_int32(self, b):
        return int.from_bytes(b, byteorder=self.endian, signed=False)
