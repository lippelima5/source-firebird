#
# Copyright (c) 2024 Markware, LTDA., all rights reserved.
# -- Markware LTDA - www.markware.com.br
# -- contato@markware.com.br | (11)91727-7726
#


from setuptools import find_packages, setup

MAIN_REQUIREMENTS = [
    "airbyte-cdk~=0.2",
    "fdb==2.0.2"
]

TEST_REQUIREMENTS = [
    "requests-mock~=1.9.3",
    "pytest-mock~=3.6.1",
    "pytest~=6.2",
    "connector-acceptance-test",
]

setup(
    name="source_firebird",
    description="Source implementation for Firebird.",
    author="Felippe Lima",
    author_email="felippe@markware.com.br",
    packages=find_packages(),
    install_requires=MAIN_REQUIREMENTS,
    package_data={"": ["*.json", "*.yaml"]},
    extras_require={
        "tests": TEST_REQUIREMENTS,
    },
)
