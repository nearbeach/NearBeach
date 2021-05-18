import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NearBeach",
    version="0.28.2",
    author="Luke Christopher Clarke",
    author_email="luke@nearbeach.org",
    description="NearBeach - an open source project management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robotichead/NearBeach",
    packages=setuptools.find_packages(),
    install_requires=[
	'django',
	'simplejson',
	'pillow',
	'urllib3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
