from setuptools import setup, find_packages

setup(name='PyEvolv',
      version='1.2',
      description='An Evoloution Simulator written in pygame',
      url='https://github.com/peerlator/PyEvolv/',
      author='peerlator',
      author_email='peer.rheinboldt@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      zip_safe=False,
      entry_points = {
        'console_scripts': ['pyevolv=PyEvolv.cli:main'],
      },
      include_package_data=True
     )