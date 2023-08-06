import os
import site
import sys
from distutils.sysconfig import get_python_lib

import io
from setuptools import find_packages, setup

# Allow editable install into user site directory.
# See https://github.com/pypa/pip/issues/7953.
site.ENABLE_USER_SITE = '--user' in sys.argv[1:]

# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "src"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break


setup(
    name             = 'weather_impact_middleware',
    version          = '1.0',
    description      = 'weather impact middleware',
    author           = 'JangSuHyeok',
    author_email     = 'hyeokdev@gmail.com',
    url              = 'https://gitlab.com/latteonterrace/python_start.git',
    download_url     = 'https://gitlab.com/latteonterrace/python_start.git',
    install_requires = [],
    packages= find_packages(),
    keywords         = ['weatherimpact', 'middleware'],
    python_requires  = '>=3',
    zip_safe=False,
    package_data={'': []},
    include_package_data=True,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ]
)


if overlay_warning:
    sys.stderr.write("""

========
WARNING!
========

You have just installed Django over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
Django. This is known to cause a variety of problems. You
should manually remove the

%(existing_path)s

directory and re-install Django.

""" % {"existing_path": existing_path})
