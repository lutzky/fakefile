fakefile [![Build Status](https://travis-ci.org/lutzky/translationese.png?branch=master)](https://travis-ci.org/lutzky/translationese) 
========

Sometimes your code needs to write some files, and you want to test that it does this correctly. This library provides a relatively simple way to do it.

```python
import fakefile
import unittest
import mock

def my_function():
    with open("somefile", "w") as f:
        f.write("correct output")
    with open("existing_file", "w") as f:
        return f.read()
  

class TestMyCode(unittest.TestCase):
    def test_my_function(self):
        faker = fakefile.FakeFile()
    
        faker.set_contents("existing_file", "correct input")
    
        with mock.patch('__builtin__.open', faker.open):
            result = my_function()  # No file "somefile" will be created!
                                    # No file "existing_file" will be read!
        self.assertEquals(faker.files["somefile"].file_contents,
                          "correct output")
```

After writing, it turns out that Google has a much more advanced version of this, known as [pyfakefs](https://pypi.python.org/pypi/pyfakefs).
