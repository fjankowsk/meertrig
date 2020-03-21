#
#   Generate VOEvent from the commandline.
#

import argparse

from astropy.coordinates import SkyCoord
import astropy.units as units
import yaml

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
        description='Generate a VOEvent.'
    )

    parser.add_argument(
        'utc',
        help='The UTC of the event.'
    )

    parser.add_argument(
        'ra',
        type=str,
        help='RA in hms notation.'
    )

    parser.add_argument(
        'dec',
        type=str,
        help='Dec in dms notation.'
    )

    parser.add_argument(
        'dm',
        type=float,
        help='Dispersion measure in pc/cm3.'
    )

    parser.add_argument(
        '--dm_err',
        type=float,
        default=2.0,
        help='Unvertainty of dispersion measure in pc/cm3.'
    )

    parser.add_argument(
        '--width',
        type=float,
        help='The full pulse width at 50 per cent maximum (?) in ms.'
    )

    parser.add_argument(
        '--snr',
        type=float,
        help='The optimised S/N ratio.'
    )

    parser.add_argument(
        '--flux',
        type=float,
        help='The flux density in Jy.'
    )

    parser.add_argument(
        '--semiMaj',
        type=float,
        default=15.0,
        help='Beam semi-major axis in arcmin.'
    )

    parser.add_argument(
        '--semiMin',
        type=float,
        default=15.0,
        help='Beam semi-minor axis in arcmin.'
    )

    parser.add_argument(
        '--name',
        default='FRB'
    )

    parser.add_argument(
        '--importance',
        type=float,
        default=0.0
    )

    args = parser.parse_args()

    return args


#
# MAIN
#

def main():
    args = parse_args()

    defaults = get_config('defaults.yml')

    # treat email address
    defaults['contact_email'] = defaults['contact_email'].replace(' AT ', '@')

    # parse coordinates
    coord = SkyCoord(
        ra=args.ra,
        dec=args.dec,
        unit=(units.degree, units.degree),
        frame='icrs'
    )

    mw_dm = get_mw_dm(coord.galactic.l.deg, coord.galactic.b.deg)

    # round to 2 significant digits and convert to string
    mw_dm = "{0:.2f}".format(mw_dm)

    event_params = {
        'utc': args.utc,
        'title': 'Detection of test event',
        'short_name': 'Test event',
        'beam_semi_major': args.semiMaj,
        'beam_semi_minor': args.semiMin,
        'beam_rotation_angle': 0.0,
        'tsamp': 0.367,
        'cfreq': 1284.0,
        'bandwidth': 856.0,
        'nchan': 4096,
        'beam': 123,
        'dm': args.dm,
        'dm_err': args.dm_err,
        'width': args.width,
        'snr': args.snr,
        'flux': args.flux,
        'ra': coord.ra.deg,
        'dec': coord.dec.deg,
        'gl': coord.galactic.l.deg,
        'gb': coord.galactic.b.deg,
        'mw_dm_limit': mw_dm,
        'name': args.name,
        'importance': args.importance,
        'internal': 1,
        'open_alert': 0,
        'test': 1,
        'product_id': 'array_1'
    }

    params = defaults.copy()
    params.update(event_params)

    v = VOEvent(host='localhost', port=8089)
    v.generate_event(params, True)

    print('All done.')


if __name__ == "__main__":
    main()
