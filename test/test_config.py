from unittest import TestCase

from src.config import set_default_sys_config, save_sys_config, sys_config, get_project_config


class Test(TestCase):
    def test__set_default_sys_config(self):
        set_default_sys_config()

    def test_save_sys_config(self):
        save_sys_config()

    def test_get_sys_config(self):
        print(sys_config)

    def test_get_project_config(self):
        print(get_project_config('test_project'))
