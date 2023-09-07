from setuptools import setup

setup(name='librarian',
      version='0.1.1',
      description='Video library name manager',
      url='https://github.com/retroceder/librarian',
      author='Maxim Gomozov',
      author_email='maximgomozoff@gmail.com',
      packages=['emi.librarian'],
      scripts=['bin/librarian'],
      install_requires=['colorama'],
      zip_safe=False)
