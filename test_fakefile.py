import mock
import unittest

from fakefile import FakeFile


class TestFakeFile(unittest.TestCase):
    def setUp(self):
        self.fakefile = FakeFile()

    def test_write(self):
        with mock.patch('__builtin__.open', self.fakefile.open):
            f = open("/impossible/location", "w")
            f.write("content")
            f.close()

        test_reference_to_f = self.fakefile.files["/impossible/location"]
        self.assertEquals("content", test_reference_to_f.file_contents)

    def test_write_context(self):
        with mock.patch('__builtin__.open', self.fakefile.open):
            with open("/impossible/location", "w") as f:
                f.write("content2")

        test_reference_to_f = self.fakefile.files["/impossible/location"]
        self.assertEquals("content2", test_reference_to_f.file_contents)

    def test_write_multiline(self):
        with mock.patch('__builtin__.open', self.fakefile.open):
            with open("/impossible/location", "w") as f:
                print >>f, "line 1"
                print >>f, "line 2"

        test_reference_to_f = self.fakefile.files["/impossible/location"]
        actual_lines = test_reference_to_f.file_contents.splitlines()
        self.assertEquals(["line 1", "line 2"], actual_lines)

    def test_read(self):
        self.fakefile.set_contents("/dev/null", "look ma, content!")

        with mock.patch('__builtin__.open', self.fakefile.open):
            with open("/dev/null", "r") as f:
                self.assertEqual(f.read(), "look ma, content!")

            # Should still be re-openable and re-readable
            with open("/dev/null", "r") as f:
                self.assertEqual(f.read(), "look ma, content!")
