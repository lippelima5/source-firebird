#
# Copyright (c) 2024 Markware, LTDA., all rights reserved.
# -- Markware LTDA - www.markware.com.br
# -- contato@markware.com.br | (11)91727-7726
#


import sys

from airbyte_cdk.entrypoint import launch
from source_firebird import SourceFirebird

if __name__ == "__main__":
    source = SourceFirebird()
    launch(source, sys.argv[1:])
