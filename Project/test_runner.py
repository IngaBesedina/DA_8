import unittest

import utest_students


testLoad = unittest.TestLoader()
suites = testLoad.loadTestsFromModule(utest_students)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suites)
