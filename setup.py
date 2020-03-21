import os.path
from setuptools import setup

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'meertrig', 'version.py')

    with open(version_file, 'r') as f:
        raw = f.read()

    items = {}
    exec(raw, None, items)

    return items['__version__']

setup(name='meertrig',
      version=get_version(),
      description='MeerTRAP VOEvent Trigger Tools.',
      url='https://bitbucket.org/jankowsk/meertrig',
      author='Fabian Jankowski',
      author_email='fjankowsk at gmail.com',
      license='MIT',
      packages=['meertrig'],
      install_requires=[
            'astropy',
            'numpy',
            'pygedm',
            'pytz',
            'pyyaml'
      ],
      zip_safe=False)
