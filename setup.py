from setuptools import setup

setup(name='trove_python',
      version='0.1',
      description='Python tools for working with Trove Australia.',
      url='https://github.com/Trove-Toolshed',
      author='Tim Sherratt',
      author_email='tim@discontents.com.au',
      license='MIT',
      packages=['trove_python', 'trove_python.trove_core', 'trove_python.trove_zotero', 'trove_python.trove_harvest'],
      zip_safe=False)