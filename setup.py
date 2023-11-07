from setuptools import find_packages, setup

setup(
    name='EchoData',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas"
    ],
    author='Erfan Yazdpour',
    author_email='e.yazdpour@gmail.com',
    description='A comprehensive data export tool for analyzing and reporting campaign performance across various marketing platforms',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eyazdpour/EchoData',
)
