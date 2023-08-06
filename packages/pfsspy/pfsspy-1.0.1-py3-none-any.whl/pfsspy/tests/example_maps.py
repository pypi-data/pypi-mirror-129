import numpy as np
import pytest
from astropy.time import Time
from sunpy.map import Map

import pfsspy


@pytest.fixture
def zero_map():
    # Test a completely zero input
    ns = 30
    nphi = 20
    nr = 10
    rss = 2.5
    br = np.zeros((nphi, ns))
    header = pfsspy.utils.carr_cea_wcs_header(Time('1992-12-21'), br.shape)
    input_map = Map((br.T, header))

    input = pfsspy.Input(input_map, nr, rss)
    output = pfsspy.pfss(input)
    return input, output


@pytest.fixture
def dipole_map():
    ntheta = 30
    nphi = 20

    phi = np.linspace(0, 2 * np.pi, nphi)
    theta = np.linspace(-np.pi / 2, np.pi / 2, ntheta)
    theta, phi = np.meshgrid(theta, phi)

    def dipole_Br(r, theta):
        return 2 * np.sin(theta) / r**3

    br = dipole_Br(1, theta)
    header = pfsspy.utils.carr_cea_wcs_header(Time('1992-12-21'), br.shape)
    header['bunit'] = 'nT'
    return Map((br.T, header))


@pytest.fixture
def dipole_result(dipole_map):
    nr = 10
    rss = 2.5

    input = pfsspy.Input(dipole_map, nr, rss)
    output = pfsspy.pfss(input)
    return input, output


@pytest.fixture
def gong_map():
    """
    Automatically download and unzip a sample GONG synoptic map.
    """
    return pfsspy.sample_data.get_gong_map()


@pytest.fixture
def adapt_map():
    """
    Automatically download and unzip a sample GONG synoptic map.
    """
    return pfsspy.sample_data.get_adapt_map()
