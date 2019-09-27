from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


#est_deps = ['mock', 'pytest', 'pyyaml']

setup(name='auto_sync',
      version='1.0.0',
      description='Auto Sync for UST',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
      ],
      url='https://github.com/vossen-adobe/auto-sync',
      maintainer='Danimae Vossen',
      maintainer_email='vossen.dm@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['pyyaml'],
      tests_require=[],
      entry_points={
          'console_scripts': [
              'auto_sync = auto_sync.app:cli',
          ]
      },
      )

# twine upload --repository testpypi dist/*.tar.gz dist/*.whl
# twine upload dist/*.tar.gz dist/*.whl

# Github: https://github.com/vossen-adobe/auto-sync
# PyPI: https://pypi.org/project/ust-autosync