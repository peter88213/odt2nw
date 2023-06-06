""" Build python script for the FreeMind to novelWriter converter.
        
In order to distribute single scripts without dependencies, 
this script "inlines" all modules imported from the pywriter package.

For further information see https://github.com/peter88213/odt2nw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import inliner

VERSION = '0.1.0'

SRC = '../src/'
BUILD = '../'
SOURCE_FILE = f'{SRC}odt2nw_.py'
TARGET_FILE = f'{BUILD}odt2nw.py'


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'odt2nwlib', '../src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'yw2nwlib', '../src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'pywriter', '../src/')
    # inliner.run(TARGET_FILE, TARGET_FILE, 'pywriter', '../../PyWriter/src/', copyPyWriter=True)
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        script = f.read()
    with open(TARGET_FILE, 'w', encoding='utf-8', newline='\n') as f:
        f.write(script.replace('@release', VERSION))
    print('Done.')


if __name__ == '__main__':
    main()
