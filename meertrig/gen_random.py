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
from meertrig.voevent import VOEvent


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
        default=300,
        help='Emit one event every period seconds (default: 300).'
    )

    args = parser.parse_args()

    return args


def generate_random_event(v, nr):
    """
    Generate a random VOEvent.

    Parameters
    ----------
    v: ~meertrip.VOEvent
        VOEvent instance.
    nr: int
        The number of the event.
    """

    # generate random parameters
    utc = Time.now().iso
    ra = np.random.uniform(0, 360)
    dec = np.random.uniform(-90, 25)
    beam = np.random.randint(1, 768)
    dm = np.random.uniform(200, 5000)
    mw_dm = dm - 100.0
    width = np.random.uniform(2, 30)
    snr = np.random.uniform(10, 50)
    flux = 0.1 * snr
    name = 'TestEvent{0}'.format(nr)
    importance = np.random.uniform(0.5, 1)

    # parse coordinates
    c = SkyCoord(
        ra=ra,
        dec=dec,
        unit=(units.degree, units.degree),
        frame='icrs'
    )

    g = c.galactic

    params = {
        'utc': utc,
        'author_ivorn': 'uk.manchester.meertrap',
        'title': 'Detection of test event',
        'short_name': 'Test event',
        'contact_name': 'Fabian Jankowski',
        'contact_email': 'Test@test.com',
        'beam_semi_major': 64.0,
        'beam_semi_minor': 28.8,
        'beam_rotation_angle': 0.0,
        'tsamp': 0.367,
        'cfreq': 1284.0,
        'bandwidth': 856.0,
        'nchan': 4096,
        'npol': 2,
        'bits': 8,
        'gain': 2.0, # XXX
        'tsys': 20.0, # XXX
        'backend': 'MeerTRAP',
        'beam': beam,
        'dm': dm,
        'dm_err': 1.0,
        'width': width,
        'snr': snr,
        'flux': flux,
        'ra': c.ra.deg,
        'dec': c.dec.deg,
        'gl': g.l.deg,
        'gb': g.b.deg,
        'mw_dm_limit': mw_dm,
        'galactic_electron_model': 'ymw16',
        'observatory_location': 'MeerKAT',
        'name': name,
        'descriptions': ['Transient detected using the MeerTRAP real-time single-pulse search pipeline.'],
        'importance': importance,
        'internal': 1,
        'open_alert': 0,
        'test': 1
    }

    vostr = v.generate_event(params, True)

    return vostr


#
# MAIN
#

def main():
    args = parse_args()

    config = get_config()

    v = VOEvent(
        host=config['broker']['host'],
        port=config['broker']['port']
    )

    nr = 0

    while True:
        ve = generate_random_event(v, nr)
        ve.send_event(ve)

        nr += 1
        sleep(args.period)

    print('All done.')


if __name__ == "__main__":
    main()
