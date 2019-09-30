from setuptools import setup, find_packages

from auto_sync._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_deps = [
                 'pyinstaller',
                 'wheel',
                 'twine'
             ],

setup(name='auto-sync',
      version=__version__,
      description='Sync Tool Automator',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[],
      url='https://github.com/vossen-adobe/auto-sync',
      maintainer='Danimae Vossen',
      maintainer_email='vossen.dm@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_data={
          'auto_sync': ['resources/*'],
      },
      install_requires=[
          'click',
          'click-default-group',
          'pyyaml'
      ],
      extras_require={
          'setup': setup_deps,
      },
      setup_requires=setup_deps,
      entry_points={
          'console_scripts': [
              'auto_sync = auto_sync.app:cli',
          ]
      },
      )
