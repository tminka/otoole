import tempfile
import os
from otoole.visualise import create_res

SIMPLICITY_VERSION = 'v0.1a0'


def test_create_res():

    url = 'https://github.com/OSeMOSYS/simplicity/archive/{}.zip'.format(SIMPLICITY_VERSION)
    with tempfile.TemporaryDirectory() as temp_folder:
        path_to_resfile = os.path.join(temp_folder, 'simplicity.pdf')
        create_res(url, path_to_resfile)
