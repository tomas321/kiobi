from setuptools import setup, find_packages

setup(name='kiobi',
      version='0.0.1rc1',
      description='import and export Kibana objects',
      url='http://github.com/tomas321/kiobi',
      author='Tomas Bellus',
      author_email='tomas.bellus@gmail.com',
      packages=find_packages(),
      # scripts=['path/to/executable/scripts'],
      install_requires=['requests', 'elasticsearch'])
