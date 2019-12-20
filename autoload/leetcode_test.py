import unittest
import os
import sys

plugin_dir = os.getcwd()
thirdparty_dir = os.path.join(plugin_dir, 'thirdparty')
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)
if thirdparty_dir not in sys.path:
    sys.path.append(thirdparty_dir)

os.environ['LEETCODE_BASE_URL'] = 'https://leetcode.com'
import leetcode
try:
    import keyring
    has_keyring = False
except ImportError:
    has_keyring = False

class TestLeetcode(unittest.TestCase):

    def setUp(self):
        leetcode.enable_logging()
        is_login = leetcode.signin("fake", "fake")
        self.assertEqual(is_login, True)

    def testGetProbles(self):
        leetcode.get_problems(["all"])


    def test_eqal(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
