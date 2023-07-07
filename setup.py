from setuptools import find_packages, setup

setup(
    name='sallytools',
    version='1.0.0',
    description='Create simple command line tools',
    url='git@github.com:mitchellharvey/clitool.git',
    author='Mitchell Harvey',
    author_email='',
    license='unlicense',
    packages=find_packages(),
    package_data={
    },
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[]
)
