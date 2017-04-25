import unittest
import os

import pep8


class Pep8TestCase(unittest.TestCase):
    """
    Keep styles in check with PEP8
    """
    def test_pep8(self):
        files = os.listdir('.')
        python_files = [f for f in files if f.endswith('.py')]
        pep8style = pep8.StyleGuide(paths=python_files)
        report = pep8style.check_files()  # Verbose by default, will print
        if report.total_errors:
            raise RuntimeError('PEP8 StyleCheck failed. See STDOUT above.')


if __name__ == '__main__':
    unittest.main()
