# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Test for driven controls
"""

import os

import numpy as np
import pytest

from qctrlopencontrols.exceptions.exceptions import ArgumentsValueError
from qctrlopencontrols import DrivenControl

from qctrlopencontrols.driven_controls import (
    UPPER_BOUND_SEGMENTS, UPPER_BOUND_RABI_RATE, UPPER_BOUND_DETUNING_RATE)


def _remove_file(filename):
    """Removes the file after test done
    """

    if os.path.exists(filename):
        os.remove(filename)
    else:
        raise IOError('Could not find file {}'.format(
            filename))


def test_driven_controls():

    """Tests the construction of driven controls
    """
    _rabi_rates = [np.pi, np.pi, 0]
    _azimuthal_angles = [np.pi/2, 0, -np.pi]
    _detunings = [0, 0, 0]
    _durations = [1, 2, 3]

    _name = 'driven_control'

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=_durations,
        name=_name)

    assert np.allclose(driven_control.rabi_rates, _rabi_rates)
    assert np.allclose(driven_control.durations, _durations)
    assert np.allclose(driven_control.detunings, _detunings)
    assert np.allclose(driven_control.azimuthal_angles, _azimuthal_angles)

    assert driven_control.name == _name

    driven_control = DrivenControl(
        rabi_rates=None,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=_durations,
        name=_name)

    assert np.allclose(driven_control.rabi_rates, np.array([0., 0., 0.]))
    assert np.allclose(driven_control.durations, _durations)
    assert np.allclose(driven_control.detunings, _detunings)
    assert np.allclose(driven_control.azimuthal_angles, _azimuthal_angles)

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=None,
        detunings=_detunings,
        durations=_durations,
        name=_name)

    assert np.allclose(driven_control.rabi_rates, _rabi_rates)
    assert np.allclose(driven_control.durations, _durations)
    assert np.allclose(driven_control.detunings, _detunings)
    assert np.allclose(driven_control.azimuthal_angles, np.array([0., 0., 0.]))

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=None,
        durations=_durations,
        name=_name)

    assert np.allclose(driven_control.rabi_rates, _rabi_rates)
    assert np.allclose(driven_control.durations, _durations)
    assert np.allclose(driven_control.detunings, np.array([0., 0., 0.]))
    assert np.allclose(driven_control.azimuthal_angles, _azimuthal_angles)

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=None,
        name=_name)

    assert np.allclose(driven_control.rabi_rates, _rabi_rates)
    assert np.allclose(driven_control.durations, np.array([1., 1., 1.]))
    assert np.allclose(driven_control.detunings, _detunings)
    assert np.allclose(driven_control.azimuthal_angles, _azimuthal_angles)

    driven_control = DrivenControl()
    assert np.allclose(driven_control.rabi_rates, np.array([np.pi]))
    assert np.allclose(driven_control.durations, np.array([1.]))
    assert np.allclose(driven_control.detunings, np.array([0.]))
    assert np.allclose(driven_control.azimuthal_angles, np.array([0.]))

    with pytest.raises(ArgumentsValueError):
        _ = DrivenControl(rabi_rates=[-1])
        _ = DrivenControl(detunings=[-1])
        _ = DrivenControl(durations=[0])
        _ = DrivenControl(rabi_rates=[1.1 * UPPER_BOUND_RABI_RATE])
        _ = DrivenControl(detunings=[1.1 * UPPER_BOUND_DETUNING_RATE])
        _ = DrivenControl(rabi_rates=[1] * UPPER_BOUND_SEGMENTS + [1])
        _ = DrivenControl()
        _ = DrivenControl(rabi_rates=[1, 2], azimuthal_angles=[1, 2, 3],
                          detunings=None, durations=None)

def test_control_export():

    """Tests exporting the control to a file
    """
    _rabi_rates = [5 * np.pi, 4 * np.pi, 3 * np.pi]
    _azimuthal_angles = [np.pi / 4, np.pi / 3, 0]
    _detunings = [0, 0, np.pi]
    _durations = [2, 2, 1]

    _name = 'driven_control'

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=_durations,
        name=_name
    )

    _filename = 'driven_control_qctrl_cylindrical.csv'
    driven_control.export_to_file(
        filename=_filename,
        file_format='Q-CTRL expanded',
        file_type='CSV',
        coordinates='cylindrical')

    _filename = 'driven_control_qctrl_cartesian.csv'
    driven_control.export_to_file(
        filename=_filename,
        file_format='Q-CTRL expanded',
        file_type='CSV',
        coordinates='cartesian')

    _filename = 'driven_control_qctrl_cylindrical.json'
    driven_control.export_to_file(
        filename=_filename,
        file_format='Q-CTRL expanded',
        file_type='JSON',
        coordinates='cylindrical')

    _filename = 'driven_control_qctrl_cartesian.json'
    driven_control.export_to_file(
        filename=_filename,
        file_format='Q-CTRL expanded',
        file_type='JSON',
        coordinates='cartesian')

    _remove_file('driven_control_qctrl_cylindrical.csv')
    _remove_file('driven_control_qctrl_cartesian.csv')
    _remove_file('driven_control_qctrl_cylindrical.json')
    _remove_file('driven_control_qctrl_cartesian.json')

def test_plot_data():
    """
    Test the plot data produced for a driven control.
    """
    _rabi_rates = [np.pi, 2 * np.pi, np.pi]
    _azimuthal_angles = [0, np.pi/2, -np.pi/2]
    _detunings = [0, 1, 0]
    _durations = [1, 1.25, 1.5]

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=_durations
    )

    x_amplitude = [np.pi, 0., 0.]
    y_amplitude = [0., 2*np.pi, -np.pi]

    plot_data = driven_control.export(
        dimensionless_rabi_rate=False, coordinates='cartesian'
    )

    assert np.allclose([point['duration'] for point in plot_data['X amplitude']], _durations)
    assert np.allclose([point['duration'] for point in plot_data['Y amplitude']], _durations)
    assert np.allclose([point['duration'] for point in plot_data['Detuning']], _durations)

    assert np.allclose([point['value'] for point in plot_data['X amplitude']], x_amplitude)
    assert np.allclose([point['value'] for point in plot_data['Y amplitude']], y_amplitude)
    assert np.allclose([point['value'] for point in plot_data['Detuning']], _detunings)

def test_pretty_print():

    """Tests pretty output of driven control
    """

    _maximum_rabi_rate = 2*np.pi
    _maximum_detuning = 1.0
    _rabi_rates = [np.pi, 2 * np.pi, np.pi]
    _azimuthal_angles = [0, np.pi / 2, -np.pi / 2]
    _detunings = [0, 1, 0]
    _durations = [1., 1., 1.]

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=_durations
    )

    _pretty_rabi_rates = [str(_rabi_rate/_maximum_rabi_rate)
                          for _rabi_rate in _rabi_rates]
    _pretty_azimuthal_angles = [str(azimuthal_angle/np.pi)
                                for azimuthal_angle in _azimuthal_angles]
    _pretty_detunings = [str(detuning/_maximum_detuning)
                         for detuning in _detunings]
    _pretty_durations = [str(duration/3.) for duration in _durations]
    _pretty_rabi_rates = ','.join(_pretty_rabi_rates)
    _pretty_azimuthal_angles = ','.join(_pretty_azimuthal_angles)
    _pretty_detunings = ','.join(_pretty_detunings)
    _pretty_durations = ','.join(_pretty_durations)

    _pretty_string = []
    _pretty_string.append('Rabi Rates = [{}] x {}'.format(
        _pretty_rabi_rates, _maximum_rabi_rate))
    _pretty_string.append('Azimuthal Angles = [{}] x pi'.format(
        _pretty_azimuthal_angles))
    _pretty_string.append('Detunings = [{}] x {}'.format(
        _pretty_detunings, _maximum_detuning))
    _pretty_string.append('Durations = [{}] x 3.0'.format(
        _pretty_durations))

    _pretty_string = '\n'.join(_pretty_string)

    assert str(driven_control) == _pretty_string

    _maximum_rabi_rate = 0.
    _maximum_detuning = 1.0
    _rabi_rates = [0., 0., 0.]
    _azimuthal_angles = [0, np.pi / 2, -np.pi / 2]
    _detunings = [0, 1, 0]
    _durations = [1., 1., 1.]

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=_durations
    )

    _pretty_rabi_rates = ['0', '0', '0']
    _pretty_azimuthal_angles = [str(azimuthal_angle / np.pi)
                                for azimuthal_angle in _azimuthal_angles]
    _pretty_detunings = [str(detuning / _maximum_detuning)
                         for detuning in _detunings]
    _pretty_durations = [str(duration / 3.) for duration in _durations]
    _pretty_rabi_rates = ','.join(_pretty_rabi_rates)
    _pretty_azimuthal_angles = ','.join(_pretty_azimuthal_angles)
    _pretty_detunings = ','.join(_pretty_detunings)
    _pretty_durations = ','.join(_pretty_durations)

    _pretty_string = []
    _pretty_string.append('Rabi Rates = [{}] x {}'.format(
        _pretty_rabi_rates, _maximum_rabi_rate))
    _pretty_string.append('Azimuthal Angles = [{}] x pi'.format(
        _pretty_azimuthal_angles))
    _pretty_string.append('Detunings = [{}] x {}'.format(
        _pretty_detunings, _maximum_detuning))
    _pretty_string.append('Durations = [{}] x 3.0'.format(
        _pretty_durations))

    _pretty_string = '\n'.join(_pretty_string)

    assert str(driven_control) == _pretty_string

    _maximum_rabi_rate = 2 * np.pi
    _maximum_detuning = 0.
    _rabi_rates = [np.pi, 2 * np.pi, np.pi]
    _azimuthal_angles = [0, np.pi / 2, -np.pi / 2]
    _detunings = [0, 0., 0]
    _durations = [1., 1., 1.]

    driven_control = DrivenControl(
        rabi_rates=_rabi_rates,
        azimuthal_angles=_azimuthal_angles,
        detunings=_detunings,
        durations=_durations
    )

    _pretty_rabi_rates = [str(_rabi_rate / _maximum_rabi_rate)
                          for _rabi_rate in _rabi_rates]
    _pretty_azimuthal_angles = [str(azimuthal_angle / np.pi)
                                for azimuthal_angle in _azimuthal_angles]
    _pretty_detunings = ['0', '0', '0']
    _pretty_durations = [str(duration / 3.) for duration in _durations]
    _pretty_rabi_rates = ','.join(_pretty_rabi_rates)
    _pretty_azimuthal_angles = ','.join(_pretty_azimuthal_angles)
    _pretty_detunings = ','.join(_pretty_detunings)
    _pretty_durations = ','.join(_pretty_durations)

    _pretty_string = []
    _pretty_string.append('Rabi Rates = [{}] x {}'.format(
        _pretty_rabi_rates, _maximum_rabi_rate))
    _pretty_string.append('Azimuthal Angles = [{}] x pi'.format(
        _pretty_azimuthal_angles))
    _pretty_string.append('Detunings = [{}] x {}'.format(
        _pretty_detunings, _maximum_detuning))
    _pretty_string.append('Durations = [{}] x 3.0'.format(
        _pretty_durations))

    _pretty_string = '\n'.join(_pretty_string)

    assert str(driven_control) == _pretty_string
