from io import BytesIO

import types


class FakeFile(object):
    def __init__(self):
        self.files = {}

    def open(self, filename, *args, **kwargs):
        f = BytesIO()
        orig_close = f.close

        def save_contents_and_close(self, *args, **kwargs):
            self.seek(0)
            self.file_contents = self.read()
            orig_close()

        f.close = types.MethodType(save_contents_and_close, f)

        self.files[filename] = f

        return f
