##############################################################################
# Copyright 2009, Gerhard Weis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  * Neither the name of the authors nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT
##############################################################################
"""
Test cases for the isodate module.
"""
import datetime as dt
import time

import pytest

from isodate import DT_EXT_COMPLETE, LOCAL, strftime, tzinfo

TEST_CASES = (
    (
        dt.datetime(2012, 12, 25, 13, 30, 0, 0, LOCAL),
        DT_EXT_COMPLETE,
        "2012-12-25T13:30:00+10:00",
    ),
    # DST ON
    (
        dt.datetime(1999, 12, 25, 13, 30, 0, 0, LOCAL),
        DT_EXT_COMPLETE,
        "1999-12-25T13:30:00+11:00",
    ),
    # microseconds
    (
        dt.datetime(2012, 10, 12, 8, 29, 46, 69178),
        "%Y-%m-%dT%H:%M:%S.%f",
        "2012-10-12T08:29:46.069178",
    ),
    (
        dt.datetime(2012, 10, 12, 8, 29, 46, 691780),
        "%Y-%m-%dT%H:%M:%S.%f",
        "2012-10-12T08:29:46.691780",
    ),
)

ORIG = {
    "STDOFFSET": tzinfo.STDOFFSET,
    "DSTOFFSET": tzinfo.DSTOFFSET,
    "DSTDIFF": tzinfo.DSTDIFF,
    "localtime": time.localtime,
}


# local time zone mock function
def localtime_mock(secs):
    """
    mock time.localtime so that it always returns a time_struct with
    tm_idst=1
    """
    tt = ORIG["localtime"](secs)
    # before 2000 everything is dst, after 2000 no dst.
    if tt.tm_year < 2000:
        dst = 1
    else:
        dst = 0
    tt = (
        tt.tm_year,
        tt.tm_mon,
        tt.tm_mday,
        tt.tm_hour,
        tt.tm_min,
        tt.tm_sec,
        tt.tm_wday,
        tt.tm_yday,
        dst,
    )
    return time.struct_time(tt)


def setup_module(module):
    """setup any state specific to the execution of the given module."""
    # override all saved values with fixtures.
    # calculate LOCAL TZ offset, so that this test runs in
    # every time zone
    tzinfo.STDOFFSET = dt.timedelta(seconds=36000)  # assume LOC = +10:00
    tzinfo.DSTOFFSET = dt.timedelta(seconds=39600)  # assume DST = +11:00
    tzinfo.DSTDIFF = tzinfo.DSTOFFSET - tzinfo.STDOFFSET
    time.localtime = localtime_mock


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
    # restore test fixtures
    tzinfo.STDOFFSET = ORIG["STDOFFSET"]
    tzinfo.DSTOFFSET = ORIG["DSTOFFSET"]
    tzinfo.DSTDIFF = ORIG["DSTDIFF"]
    time.localtime = ORIG["localtime"]


@pytest.mark.parametrize("dt, format, expectation", TEST_CASES)
def test_format(dt, format, expectation):
    """
    Take date object and create ISO string from it.
    This is the reverse test to test_parse.
    """
    assert strftime(dt, format) == expectation
