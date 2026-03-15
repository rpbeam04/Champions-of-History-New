import unittest


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests", pattern="tests.py")
    runner = unittest.TextTestRunner(verbosity=2)
    raise SystemExit(not runner.run(suite).wasSuccessful())