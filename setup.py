from setuptools import find_packages, setup

setup(
    include_package_data = True,
    name="NHFTools",
    version="0.0.0",
    description="Test for setting up shared tools",
    packages=find_packages(),
    install_requires=['pillow', 'datetime'],
    license="",
    author='klafontant',
    author_email='klafontant@newhudonfacades.com'
)