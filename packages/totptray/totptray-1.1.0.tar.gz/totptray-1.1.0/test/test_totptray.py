#!/usr/bin/python3
from totptray import totptray
import unittest
import pyperclip

class Test(unittest.TestCase):
    def test_icon_creation(self):
        icon = totptray._create_icon()
        try:
            icon.verify()
        except:
            self.fail("Icon does not pass verification!")

        self.assertTrue(icon.width > 1)
        self.assertTrue(icon.height > 1)
    
    def test_copy_code(self):
        #Clear the clipboard.
        pyperclip.copy("")
        try:
            totptray._copy_code("test")
        except:
            self.fail("Got an exception while calling _copy_code!")

        code = pyperclip.paste()
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_create_menu_empty(self):
        menu = totptray._create_menu("")
        self.assertEqual(len(menu), 0)

    def test_create_menu_one(self):
        menu = totptray._create_menu((("label","key"),))
        self.assertEqual(len(menu), 1)
        self.assertEqual(menu[0].text, "label")

    def test_create_menu_multiple(self):
        menu = totptray._create_menu((("label0","key0"),("label1","key1"),("label2","key2")))
        self.assertEqual(len(menu), 3)
        for idx, item in enumerate(menu):
            self.assertEqual(item.text, "label" + str(idx))

    def test_create_menu_incorrect(self):
        self.assertRaises(AssertionError, totptray._create_menu, (("label=key",),))

if __name__ == '__main__':
    unittest.main()
