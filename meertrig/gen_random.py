#
#   2020 Fabian Jankowski
#   Generate periodic VOEvents with randomised content.
#

import argparse
from time import sleep

from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as units
import numpy as np

from meertrig.config_helpers import get_config
from meertrig.dm_helpers import get_mw_dm
from meertrig.voevent import VOEvent

# astropy.units generates members dynamically, pylint therefore fails
# disable the corresponding pylint test for now
# pylint: disable=E1101


def parse_args():
    """
    Parse the commandline arguments.
    """

    parser = argparse.ArgumentParser(
        description='Generate VOEvents with random content.'
    )

    parser.add_argument(
        '--period',
        type=float,
        default=3600,
        help='Emit one event every period seconds (default: 3600).'
    )

    args = parser.parse_args()

    return args


def generate_random_event(v, t_defaults, nr):
    """
    Generate a random VOEvent.

    Parameters
    ----------
    v: ~meertrip.VOEvent
        VOEvent instance.
    t_defaults: dict
        Dictionary with default parameters for the VOEvents.
    nr: int
        The number of the event.
    """

    params = t_defaults.copy()

    # generate random parameters
    utc = Time.now().iso
    ra = np.random.uniform(0, 360)
    dec = np.random.uniform(-90, 25)
    beam = np.random.randint(1, 768)
    dm = np.random.uniform(200, 5000)
    width = np.random.uniform(2, 30)
    snr = np.random.uniform(10, 50)
    flux = 0.1 * snr
    name = 'TestEvent{0}'.format(nr)
    importance = np.random.uniform(0.5, 1)
    product_id = 'array_1'

    # parse coordinates
    coord = SkyCoord(
        ra=ra,
        dec=dec,
        unit=(units.degree, units.degree),
        frame='icrs'
    )

    mw_dm = get_mw_dm(coord.galactic.l.deg, coord.galactic.b.deg)

    event_params = {
        'utc': utc,
        'title': 'Detection of test event',
        'short_name': 'Test event',
        'beam_semi_major': 64.0 / 60.0,
        'beam_semi_minor': 28.8 / 60.0,
        'beam_rotation_angle': 0.0,
        'tsamp': 0.367,
        'cfreq': 1284.0,
        'bandwidth': 856.0,
        'nchan': 4096,
        'beam': beam,
        'dm': dm,
        'dm_err': 1.0,
        'width': width,
        'snr': snr,
        'flux': flux,
        'ra': coord.ra.deg,
        'dec': coord.dec.deg,
        'gl': coord.galactic.l.deg,
        'gb': coord.galactic.b.deg,
        'mw_dm_limit': mw_dm,
        'name': name,
        'importance': importance,
        'internal': 1,
        'open_alert': 0,
        'test': 1,
        'product_id': product_id
    }

    params.update(event_params)

    vostr = v.generate_event(params, True)

    return vostr


#
# MAIN
#

def main():
    args = parse_args()

    config = get_config('config.yml')
    defaults = get_config('defaults.yml')

    # treat email address
    defaults['contact_email'] = defaults['contact_email'].replace(' AT ', '@')

    v = VOEvent(
        host=config['broker']['host'],
        port=config['broker']['port']
    )

    nr = 0

    while True:
        ve = generate_random_event(v, defaults, nr)
        v.send_event(ve)

        nr += 1
        sleep(args.period)

    print('All done.')


if __name__ == "__main__":
    main()
