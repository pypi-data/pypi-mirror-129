# MIT License
#
# Copyright (c) 2021 mmb L (Python port)
# Copyright (c) 2021 Wolf Garbe (Original C# implementation)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

"""symspellpy

.. moduleauthor:: mmb L <mammothb@hotmail.com>
.. moduleauthor:: Wolf Garbe <wolf.garbe@faroo.com>
"""

__version__ = "6.7.3"

import logging
import os

from . import editdistance, helpers
from .symspellpy import SymSpell
from .verbosity import Verbosity

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "WARNING"),
    format="%(asctime)s %(levelname)s:%(message)s",
)
