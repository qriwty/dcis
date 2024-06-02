import unittest


suite = unittest.defaultTestLoader.discover('tests')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

print("\nSummary:")
print(f"Ran {result.testsRun} tests")
if result.wasSuccessful():
    print("Suite of tests: Success")
else:
    print("Suite of tests: Failures/Errors")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
