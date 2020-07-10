import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='chainwalkers_utils',
    version='0.0.5',
    description='Collection of utilities to be used across chainwalkers repos',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='git@github.com:FlipsideCrypto/chainwalkers-utils.git',
    author='Brian Ford',
    author_email='brian@flipsidecrypto.com',
    license='unlicense',
    packages=setuptools.find_packages(),
    zip_safe=False
)