#
# invitae-hw-variant-search/src/invitae-vs-core/setup.py ---
#

from __future__ import (
    absolute_import,
)

import os
from distutils.core import (
    setup,
)

#####

setup(
    name="invitae-vs-core",
    version="0.0.1",
    description="FIXME",
    author="FIXME",
    url="FIXME",
    install_requires=[
        "pandas",
        "sqlalchemy>=1.4.0",
    ],
    packages=[
        "invitae_vs_core",
    ],
    # where to find the src.
    package_dir={
        'invitae_vs_core': 'invitae_vs_core',
    },
    entry_points={
        'console_scripts': [
            "invitae-vs-core = invitae_vs_core.invitae_vs_core_main:main_entry",
        ],
    },
)
