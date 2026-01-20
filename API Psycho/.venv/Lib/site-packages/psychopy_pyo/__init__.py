#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Originally from the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2022 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

"""Audio backend for playback using Pyo (http://ajaxsoundstudio.com/software/pyo/).
"""

__version__ = '0.0.1'

from .backend_pyo import (
    init,
    get_devices_infos,
    get_input_devices,
    get_output_devices,
    getDevices,
    SoundPyo)

