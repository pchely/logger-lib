from setuptools import find_packages, setup

setup(
    name='pchelog',
    packages=find_packages(),
    version='0.3',
    description='Библиотека с возможностью логирования в MySQL БД и в файл',
    url='https://github.com/pchely/pchelog',
    author='ivanlut',
    license='MIT',
    install_requires=['pymysql', 'requests'],
    zip_safe=False
)
