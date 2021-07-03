#
# invitae-hw-variant-search/src/invitae-vs-server/setup.py ---
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
    name="invitae-vs-server",
    version="0.0.1",
    description="FIXME",
    author="FIXME",
    url="FIXME",
    install_requires=[
        #
        "invitae-vs-core",
        #
        "flask",
        "flask-bootstrap",
        "flask-debug",
        "flask-nav",
        #
        "gunicorn",
    ],
    packages=[
        "invitae_vs_server",
    ],
    # where to find the src.
    package_dir={
        'invitae_vs_server': 'invitae_vs_server',
    },
    entry_points={
        'console_scripts': [
            "invitae-vs-server = invitae_vs_server.invitae_vs_server_main:main_entry",
        ],
    },
)
