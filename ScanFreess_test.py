import unittest
import ScanFreess


class Test(unittest.TestCase):
    def test_decode(self):
        res = ScanFreess.deCode()
        self.assertEqual(res["status"], 1)

    def test_fetchSSInfo(self):
        l = ScanFreess.fetchSSInfo()
        self.assertEquals(l[3], 'aes-256-cfb')