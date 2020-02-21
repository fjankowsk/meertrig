import argparse
from datetime import datetime

from astropy.coordinates import SkyCoord
import astropy.units as units
import yaml

from meertrig.voevent import generate_voevent


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
        '--mw_dm',
        type=float
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

    # parse coordinates
    c = SkyCoord(
        ra=args.ra,
        dec=args.dec,
        unit=(units.degree, units.degree),
        frame='icrs'
    )

    g = c.galactic

    params = {
        'utc': args.utc,
        'author_ivorn': 'uk.manchester',
        'title': 'Test event',
        'contact_name': 'Fabian Jankowski',
        'contact_email': 'Test@test.com',
        'short_name': 'Test event',
        'beam_semi_major': args.semiMaj,
        'beam_semi_minor': args.semiMin,
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
        'beam': 123,
        'dm': args.dm,
        'dm_err': args.dm_err,
        'width': args.width,
        'snr': args.snr,
        'flux': args.flux,
        'ra': c.ra.deg,
        'dec': c.dec.deg,
        'gl': g.l.deg,
        'gb': g.b.deg,
        'mw_dm_limit': args.mw_dm,
        'galactic_electron_model': 'ymw16',
        'observatory_location': 'MeerKAT',
        'name': args.name,
        'importance': args.importance,
        'internal': 1,
        'test': 1
    }

    vostr = generate_voevent(params, False)
    print(vostr)

    print('All done.')

if __name__ == "__main__":
    main()
