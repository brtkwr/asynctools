import unittest
import asynctools
import asynctools.tests as tests

class Test(unittest.TestCase):
    def setUp(self):
        self.label = 'urls'
        self.input_format = 'jpeg'
        self.output_format = 'jpeg'
        self.min_size = 300
        self.max_ratio = 2

    def test_downloader(self):
        downloader = asynctools.AsyncDownloader(self.label)
        downloader.download()

    def test_resizer(self):
        resizer = asynctools.AsyncResizer(self.label, self.input_format, self.output_format, self.min_size, self.max_ratio)
        resizer.resize()

if __name__ == '__main__':
    unittest.main()
