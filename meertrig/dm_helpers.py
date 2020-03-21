# -*- coding: utf-8 -*-
#
#   2020 Fabian Jankowski
#   Milky Way DM related helper functions.
#

import pygedm


def get_mw_dm(gl, gb):
    """
    Determine the Galactic Milky Way contribution to the dispersion measure
    for a given sightline.

    We return the result from the YMW16 model.

    Parameters
    ----------
    gl: float
        Galactic longitude in degrees.
    gb: float
        Galactic latitude in degrees.

    Returns
    -------
    dm_ymw16: float
        The Milky Way DM.
    """

    # 30 kpc
    dist = 30 * 1000

    dm_ymw16, _ = pygedm.dist_to_dm(gl, gb, dist, mode='gal', method='ymw16')

    return dm_ymw16.value
