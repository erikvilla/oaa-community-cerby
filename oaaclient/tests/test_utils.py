"""
Copyright 2022 Veza Technologies Inc.

Use of this source code is governed by a the MIT
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
"""

import oaaclient.utils as utils
import os
import pytest

OAA_ICON_B64="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"


def test_encode_icon_file():

    assert os.path.isfile("tests/oaa_icon.png")
    b64_icon = utils.encode_icon_file("tests/oaa_icon.png")
    assert b64_icon is not None
    assert isinstance(b64_icon, str)

    assert b64_icon == OAA_ICON_B64