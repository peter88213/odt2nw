"""Regression test for the odt2nw project.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/odt2nw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
from shutil import copyfile, rmtree, copytree
import re
import odt2nw_

# Test environment

TEST_PATH = f'{os.getcwd()}/../test'
TEST_DATA_PATH = f'{TEST_PATH}/data/'
TEST_EXEC_PATH = TEST_PATH

# To be placed in TEST_DATA_PATH:

NW_NORMAL = 'normal.nw'
PROJECT = 'Sample Project'
NORMAL_ODT = 'normal.odt'


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # File may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


def adjust_timestamp(text):
    return re.sub('timeStamp=".*?"', 'timeStamp="2023-06-07 10:53:35"', text)


def remove_all_testfiles():
    try:
        os.remove(f'{TEST_EXEC_PATH}{PROJECT}.odt')
    except:
        pass
    try:
        rmtree(f'{TEST_EXEC_PATH}{PROJECT}.nw')
    except:
        pass


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):
        try:
            os.mkdir(TEST_EXEC_PATH)
        except:
            pass
        remove_all_testfiles()

    def test_odt_to_nw(self):
        copyfile(f'{TEST_DATA_PATH}{NORMAL_ODT}', f'{TEST_EXEC_PATH}{PROJECT}.odt')
        os.chdir(TEST_EXEC_PATH)
        odt2nw_.main(f'{TEST_EXEC_PATH}{PROJECT}.odt')
        self.assertEqual(adjust_timestamp(read_file(f'{TEST_EXEC_PATH}{PROJECT}.nw/nwProject.nwx')),
                                            read_file(f'{TEST_DATA_PATH}{NW_NORMAL}/nwProject.nwx'))
        contentFiles = os.listdir(f'{TEST_EXEC_PATH}{PROJECT}.nw/content')
        for contentFile in contentFiles:
            self.assertEqual(read_file(f'{TEST_EXEC_PATH}{PROJECT}.nw/content/{contentFile}'), read_file(
                                        f'{TEST_DATA_PATH}{NW_NORMAL}/content/{contentFile}'))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
