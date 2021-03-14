import setuptools

with open("README.md", "r") as fh:
  long_description=fh.read()

setuptools.setup(
  name='NPytdl',
  version='0.3.4',
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
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=[
    'youtube_dl>=2020.11.12'
    'aiohttp>=3.6.0'
  ],
  include_package_data=True,
)
