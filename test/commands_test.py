import unittest

from src import acad_utils
from src.commands import CreateCatalog
from src.invokers import _create_catalog_style


class MyTestCase(unittest.TestCase):
    def test_create_catalog(self):
        app = acad_utils.get_application(version=24)
        lib_path = r'C:\Users\shun\Desktop\test\lib'
        template = r'catalog_style_01_A1.dwg'
        config = r'C:\Users\shun\Desktop\test\config.xlsx'
        target = r'C:\Users\shun\Desktop\test\catalog.dwg'
        CreateCatalog(application=app,
                      lib_path=lib_path,
                      catalog_style=CATALOG_STYLE['catalog_style_01_A1'],
                      excel_config=config,
                      target_dwg_file=target,
                      update=False).execute()

    # def test_create_catalog_style(self):
    #     _create_catalog_style()
if __name__ == '__main__':
    unittest.main()
