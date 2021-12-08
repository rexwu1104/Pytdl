import setuptools

with open("README.md", "r") as fh:
  long_description=fh.read()

setuptools.setup(
  name='NPytdl',
  version='4.0.1',
  author="bloodnight",
  author_email="rexwu9204@gmail.com",
  description="a new youtube_dl",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/rexwu1104/Pytdl",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=[
    'youtube_dl>=2020.11.12'
    'aiohttp>=3.6.0',
		'bs4>=0.0.1',
		'orjson>=3.6.4',
		'spotipy>=2.19.0'
  ],
  include_package_data=True,
)
