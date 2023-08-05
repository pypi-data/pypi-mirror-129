# Copyright 2021 Torsten Mehnert
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from skbuild import setup
from setuptools import find_packages
from pathlib import Path


def read_version():
    return Path('VERSION').read_text().replace('\n', '').replace('\r\n', '').strip()


setup(
    packages=find_packages(where='src'),
    version=read_version(),
    package_dir={"": "src"},
    cmake_install_dir="src/complatecpp",
    include_package_data=True,
    extras_require={"test": ["pytest"]},
)
