from setuptools import setup

setup(name='PyEvolv',
      version='1.1',
      description='An Evoloution Simulator written in pygame',
      url='https://github.com/peerlator/PyEvolv/',
      author='peerlator',
      author_email='peer.rheinboldt@gmail.com',
      license='MIT',
      packages=['grid_creator', 'game'],
      zip_safe=False,
      scripts=['PyEvolv']
      )