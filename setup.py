from setuptools import setup

setup(name='sat_locality',
      version='0.0.1',
      description='An experiment on SAT instance locality',
      url='http://github.com/storborg/funniest',
      author='Benjamin Ran',
      author_email='benjaminran2@gmail.com',
      license='MIT',
      packages=['sat_locality'],
      entry_points = {
          'console_scripts': ['sl=sat-locality.runner:main'],
      }
      zip_safe=False)
