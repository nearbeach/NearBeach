import setuptools
import codecs
import os.path

# Used to read the file
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

# Used to extract out the __version__
def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

# Used to read the readme file
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NearBeach",
    version=get_version('NearBeach/__init__.py'),
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
        'boto3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
