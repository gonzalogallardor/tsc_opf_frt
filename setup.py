from setuptools import setup

setup(
    name='tsc_opf',
    version='0.1',
    author='gonzalo.gallardor@alumnos.usm.cl',
    author_email='',
    packages=['tsc_opf'],
    entry_points={
          'console_scripts': [
              'tsc_opf = tsc_opf.cli:run_cli'
          ]
           },
    scripts='',
    url='',
    license='',
    description='',
    long_description='',
    install_requires=[],
)