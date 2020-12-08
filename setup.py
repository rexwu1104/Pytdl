import setuptools

with open("README.md", "r") as fh:
  long_description=fh.read()

setuptools.setup(
  name='Pytdl',
  version='0.1.2',
  scripts=['Pytdl'] ,
  author="Black Lotus",
  author_email="rexwu1104@gmail.com",
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
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=[
    'youtube_dl>=2020.11.12',
    'pafy>=0.5.5',
    'bs4>=0.0.1',
    'aiohttp>=3.7.2'
  ],
)