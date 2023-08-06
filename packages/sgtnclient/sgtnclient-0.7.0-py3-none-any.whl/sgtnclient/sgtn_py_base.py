# coding=utf-8
#
# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: EPL-2.0
#

import sys

if sys.version_info.major <= 2:
    from sgtn_py2_base import SgtnPyBase
elif sys.version_info.major == 3 and sys.version_info.minor < 7:
    from sgtn_py3_base import SgtnPyBase
else:
    from sgtn_py37_base import SgtnPyBase

pybase = SgtnPyBase()


class SgtnException(Exception):
    pass
