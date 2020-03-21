# -*- coding: utf-8 -*-
#
#   2020 Fabian Jankowski
#   Milky Way DM related helper functions.
#

import pygedm


def get_mw_dm(gl, gb, model='ymw16'):
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
    model: str (default: ymw16)
        The Galactic free electron model to use.

    Returns
    -------
    dm: float
        The Milky Way DM.

    Raises
    ------
    NotImplementedError
        If the Galactic free electron model `model` is not implemented.
    """

    # 30 kpc
    dist = 30 * 1000

    if model in ['ne2001', 'ymw16']:
        pass
    else:
        raise NotImplementedError('Galactic free electron model not implemented: {0}'.format(model))

    dm, _ = pygedm.dist_to_dm(gl, gb, dist, mode='gal', method=model)

    return dm.value
