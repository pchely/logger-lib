from setuptools import find_packages, setup

setup(
    name='pchelog',
    packages=find_packages(),
    version='0.2',
    description='Библиотека с возможностью логирования в MySQL БД и в файл',
    url='https://github.com/pchely/pchelog',
    author='ivanlut',
    license='MIT',
    install_requires=['pymysql'],
    long_description=open('README.md').read(),
    zip_safe=False
)
