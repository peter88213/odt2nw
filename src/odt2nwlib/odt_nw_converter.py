"""Provide an converter class for ODT import. 

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/mm2yw7
Published under the MIT License (https://opensourceFile.org/licenses/mit-license.php)
"""
import os
from pywriter.pywriter_globals import *
from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.odt_r.odt_r_import import OdtRImport
from pywriter.model.novel import Novel
from pywriter.yw.yw7_purge import remove_language_tags
from yw2nwlib.nwx_file import NwxFile


class OdtNwConverter(YwCnvUi):
    """A converter class for ODT import.

    Public methods:
        run(sourcePath, **kwargs) -- Create source and target objects and run conversion.
    """

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath -- str: the source file path.
        
        Required keyword arguments: 
            (none)
        """
        self.newFile = None

        if not os.path.isfile(sourcePath):
            self.ui.set_info_how(f'!File "{norm_path(sourcePath)}" not found.')
            return

        fileName, fileExtension = os.path.splitext(sourcePath.replace('\\', '/'))
        srcDir = os.path.dirname(sourcePath).replace('\\', '/')
        if not srcDir:
            srcDir = '.'
        srcDir = f'{srcDir}/'
        if fileExtension == OdtRImport.EXTENSION:
            sourceFile = OdtRImport(sourcePath, **kwargs)
            title = fileName.replace(srcDir, '')
            prjDir = f'{srcDir}{title}.nw'
            if os.path.isfile('{prjDir}/nwProject.lock'):
                self.ui.set_info_how(f'!Please exit novelWriter.')
                return

            try:
                os.makedirs(f'{prjDir}{NwxFile.CONTENT_DIR}')
            except FileExistsError:
                extension = '.bak'
                i = 0
                while os.path.isdir(f'{prjDir}{extension}'):
                    extension = f'.bk{i:03}'
                    i += 1
                    if i > 999:
                        self.ui.set_info_how(f'!Unable to back up the project.')
                        return

                os.replace(prjDir, f'{prjDir}{extension}')
                self.ui.set_info_what(f'Backup folder "{norm_path(prjDir)}{extension}" saved.')
                os.makedirs(f'{prjDir}{NwxFile.CONTENT_DIR}')
            targetFile = NwxFile(f'{prjDir}/nwProject.nwx', **kwargs)
            self.ui.set_info_what(
                _('Create a novelWriter project file from {0}\nNew project: "{1}"').format(sourceFile.DESCRIPTION, norm_path(targetFile.filePath)))
            try:
                self.check(sourceFile, targetFile)
                sourceFile.novel = Novel()
                sourceFile.read()
                remove_language_tags(sourceFile.novel)
                targetFile.novel = sourceFile.novel
                targetFile.write()
            except Exception as ex:
                message = f'!{str(ex)}'
                self.newFile = None
            else:
                message = f'{_("File written")}: "{norm_path(targetFile.filePath)}".'
                self.newFile = targetFile.filePath
            finally:
                self.ui.set_info_how(message)
        else:
            self.ui.set_info_how(f'!File type of "{norm_path(sourcePath)}" not supported.')
