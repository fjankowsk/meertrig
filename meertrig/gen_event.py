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
        '--dm',
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
        '--ra',
        type=float,
        help='RA in degrees.'
    )

    parser.add_argument(
        '--dec',
        type=float,
        help='Dec in degrees.'
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
        '--ymw16',
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

    parser.add_argument(
        '--utc',
        default=datetime.utcnow(),
        help='The UTC of the event (default: now).'
    )

    args = parser.parse_args()

    return args


#
# MAIN
#

def main():
    args = parse_args()

    with open('config/observatory_params.yml') as fd:
        params = yaml.load(fd.read())

    # parse coordinates
    c = SkyCoord(
        ra=args.ra,
        dec=args.dec,
        units=(units.degree, units.degree),
        frame='icrs'
    )

    g = c.galactic
    gl = g.l.deg
    gb = g.b.deg

    event = {
        'dm': args.dm,
        'dm_err': args.dm_err,
        'width': args.width,
        'snr': args.snr,
        'flux': args.flux,
        'ra': args.ra,
        'dec': args.dec,
        'beam_semi_major': args.semiMaj,
        'beam_semi_minor': args.semiMin,
        'beam_rotation_angle': 0,
        'tsamp': 0,
        'ymw16': args.ymw16,
        'name': args.name,
        'importance': args.importance,
        'utc': args.utc,
        'gl': gl,
        'gb': gb,
        'short_name': 'FRB detection'
    }

    params.update(event)

    generate_voevent(params)

if __name__ == "__main__":
    main()
