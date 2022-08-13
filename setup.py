from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in etms_support_backend/__init__.py
from etms_support_backend import __version__ as version

setup(
	name="etms_support_backend",
	version=version,
	description=".",
	author="ebkar",
	author_email="admin@ebkar.ly",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
