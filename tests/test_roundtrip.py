import tempfile
import os
from otoole.preprocess import create_datapackage, csv_to_datapackage, convert_datapackage_to_datafile, convert_file_to_package

def test_roundtrip():
    url = 'https://github.com/OSeMOSYS/simplicity'
    with tempfile.TemporaryDirectory() as temp_folder:
        path_to_datafile = os.path.join(temp_folder, 'simplicity.dat')
        convert_datapackage_to_datafile(url, path_to_datafile)
        path_to_package = os.path.join(temp_folder, 'simplicity')
        convert_file_to_package(path_to_datafile, path_to_package)
        path_to_package2 = os.path.join(temp_folder, 'simplicity2')
        csv_to_datapackage(path_to_package)
        path_to_csv = os.path.join(path_to_package, 'data')
        # This changes the string format of non-representable floats
        create_datapackage(path_to_csv, path_to_package2)
        # TODO: compare path_to_package and path_to_package2

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    test_roundtrip()


