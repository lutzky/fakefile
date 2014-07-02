from io import BytesIO

import types


class FakeFile(object):
    def __init__(self):
        self.files = {}

    def open(self, filename, *args, **kwargs):
        if filename not in self.files:
            self.set_contents(filename, "")

        if self.files[filename].closed:
            self.reopen(filename)

        return self.files[filename]

    def reopen(self, filename):
        self.set_contents(filename, self.files[filename].file_contents)

    def set_contents(self, filename, content):
        f = BytesIO()
        orig_close = f.close

        def save_contents_and_close(self, *args, **kwargs):
            self.seek(0)
            self.file_contents = self.read()
            orig_close()

        f.close = types.MethodType(save_contents_and_close, f)

        if content:
            f.write(content)
            f.seek(0)

        self.files[filename] = f

        return f
