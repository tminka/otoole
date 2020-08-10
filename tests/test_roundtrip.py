import tempfile
import os
from otoole.preprocess import create_datapackage, csv_to_datapackage, convert_datapackage_to_datafile, convert_file_to_package, write_default_values

def test_roundtrip():
    url = 'https://github.com/OSeMOSYS/simplicity'
    #url = '../simplicity'
    #temp_folder = '../output'
    #if True:
    with tempfile.TemporaryDirectory() as temp_folder:
        path_to_datafile = os.path.join(temp_folder, 'simplicity.dat')
        convert_datapackage_to_datafile(url, path_to_datafile)
        path_to_package = os.path.join(temp_folder, 'simplicity')
        convert_file_to_package(path_to_datafile, path_to_package)
        path_to_package2 = os.path.join(temp_folder, 'simplicity2')
        path_to_csv = os.path.join(path_to_package, 'data')
        # This changes the string format of non-representable floats
        # default_values.csv is missing
        # datapackage.json is ordered differently
        create_datapackage(path_to_csv, path_to_package2)
        csv_to_datapackage(path_to_package2)
        # TODO: compare path_to_package and path_to_package2

def fix_simplicity():
    write_default_values('../simplicity',None)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    test_roundtrip()


