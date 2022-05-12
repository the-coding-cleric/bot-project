from setuptools import setup
import requirements
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = []
with open('build/requirements.txt') as f:
    for req in requirements.parse(f):
        if req.name:
            name = req.name.replace('-', '_')
            full_line = name + ''.join([''.join(list(spec)) for spec in req.specs])
            install_requires.append(full_line)

setup(name="bot",
      version="1.0",
      author="jediknight112, charlielin1988",
      author_email="n/a",
      description="Script to fill out website forms with fake data",
      url="https://github.com/charlielin1988/bot-project",
      install_requires=install_requires,
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.9',
      )
