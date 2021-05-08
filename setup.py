from setuptools import find_packages, setup

setup(
    name='loggerlib',
    packages=find_packages(),
    version='0.1',
    description='Библиотека с возможностью логирования в MySQL БД и в файл',
    url='https://github.com/pchely/logger-lib',
    author='ivanlut',
    license='MIT',
    install_requires=['pymysql'],
    long_description=open('README.md').read(),
    zip_safe=False
)
