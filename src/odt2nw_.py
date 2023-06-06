#!/usr/bin/python3
"""Convert ODT to novelWriter

Version @release
Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/odt2nw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
from pywriter.ui.ui import Ui
from pywriter.ui.ui_cmd import UiCmd
from odt2nwlib.odt_nw_converter import OdtNwConverter

SUFFIX = ''
APPNAME = 'odt2nw'
SETTINGS = dict(
    outline_status=('Outline', 'New', 'Notes'),
    draft_status=('Draft', 'Started', '1st Draft'),
    first_edit_status=('1st Edit', '2nd Draft'),
    second_edit_status=('2nd Edit', '3rd Draft'),
    done_status=('Done', 'Finished'),
    scene_status=('None', 'Outline', 'Draft', '1st Edit', '2nd Edit', 'Done'),
    major_character_status=('Major', 'Main'),
    character_notes_heading='## Notes',
    character_goals_heading='## Goals',
    character_bio_heading='## Bio',
    ywriter_aka_keyword='aka',
    ywriter_tag_keyword='tag',
)
OPTIONS = dict(
    double_linebreaks=True,
)


def main(sourcePath, silentMode=True):
    if silentMode:
        ui = Ui('')
    else:
        ui = UiCmd('Create a novelWriter project from an ODT document @release')

    kwargs = {'suffix': SUFFIX}
    kwargs.update(SETTINGS)
    kwargs.update(OPTIONS)
    converter = OdtNwConverter()
    converter.ui = ui
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a novelWriter project from an ODT document',
        epilog='')
    parser.add_argument('sourcePath',
                        metavar='Sourcefile',
                        help='The path of the .odt file.')
    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress error messages and the request to confirm overwriting')
    args = parser.parse_args()
    main(args.sourcePath, args.silent)
