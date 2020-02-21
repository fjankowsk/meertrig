import astropy.units as units
from astropy.time import Time
import pytz
import voeventparse as vp


def generate_voevent(params, is_test):
    """
    Generate a VOEvent.

    Parameters
    ----------
    params: dict
        Parameters of the event.
    is_test: bool
        Determines whether the event is a test.

    Returns
    -------
    vostring: str
        The VOEvent as a pretty-printed string dump.

    Raises
    ------
    lxml.etree.DocumentInvalid
        If the event packet does not comply to the VOEvent standard.
    """

    z = params['dm'] / 1200.0  # may change
    errDeg = params['beam_semi_major'] / 60.0

    # parse utc
    utc = Time(params['utc'], format='iso', scale='utc')

    # construct ivorn
    ivorn = '{0}{1}{2}/{3}'.format(
        params['name'],
        utc.strftime('%H'),
        utc.strftime('%M'),
        utc.mjd
    )

    if is_test:
        role = vp.definitions.roles.test
    else:
        role = vp.definitions.roles.observation

    v = vp.Voevent(
        stream='nl.astron.apertif/alert',
        stream_id=ivorn,
        role=role
    )

    # author origin information
    vp.set_who(
        v,
        date=Time.now().datetime,
        author_ivorn=params['author_ivorn']
    )

    # author contact information
    vp.set_author(
        v,
        title=params['title'],
        contactName=params['contact_name'],
        contactEmail=params['contact_email'],
        shortName=params['short_name']
    )

    # parameter definitions

    # backend-specific parameters
    beam_sMa = vp.Param(
        name='beam_semi-major_axis',
        unit='MM',
        ucd='instr.beam;pos.errorEllipse;phys.angSize.smajAxis',
        ac=True,
        value=params['beam_semi_major']
    )

    beam_sma = vp.Param(
        name='beam_semi-minor_axis',
        unit='MM',
        ucd='instr.beam;pos.errorEllipse;phys.angSize.sminAxis',
        ac=True,
        value=params['beam_semi_minor']
    )

    beam_rot = vp.Param(
        name='beam_rotation_angle',
        unit='Degrees',
        ucd='instr.beam;pos.errorEllipse;instr.offset',
        ac=True,
        value=params['beam_rotation_angle']
    )

    tsamp = vp.Param(
        name='sampling_time',
        value=params['tsamp'],
        unit='ms',
        ucd='time.resolution',
        ac=True
    )

    centre_freq = vp.Param(
        name='centre_frequency',
        value=params['cfreq'],
        unit='MHz',
        ucd='em.freq;instr',
        ac=True
    )

    bw = vp.Param(
        name='bandwidth',
        value=params['bandwidth'],
        unit='MHz',
        ucd='instr.bandwidth',
        ac=True
    )

    nchan = vp.Param(
        name='nchan',
        value=str(params['nchan']),
        dataType='int',
        ucd='meta.number;em.freq;em.bin',
        unit='None'
    )

    npol = vp.Param(
        name='npol',
        value=str(params['npol']),
        dataType='int',
        unit='None'
    )

    bits = vp.Param(
        name='bits_per_sample',
        value=str(params['bits']),
        dataType='int',
        unit='None'
    )

    gain = vp.Param(
        name='gain',
        value=params['gain'],
        unit='K/Jy',
        ac=True
    )

    tsys = vp.Param(
        name='tsys',
        value=params['tsys'],
        unit='K',
        ucd='phot.antennaTemp',
        ac=True
    )

    backend = vp.Param(
        name='backend',
        value=params['backend']
    )

    beam = vp.Param(
        name='beam',
        value=str(params['beam']),
        unit='None',
        dataType='int'
    )

    beam.Description = 'Detection beam number out of a total of up to 768 beams on the sky.'

    v.What.append(
        vp.Group(
            params=[
                beam_sMa, beam_sma, beam_rot,
                tsamp, centre_freq, bw,
                nchan, npol, bits,
                gain, tsys, backend, beam
            ],
            name='observatory parameters'
        )
    )

    # event parameters
    DM = vp.Param(
        name='dm',
        ucd='phys.dispMeasure',
        unit='pc/cm^3',
        ac=True,
        value=params['dm']
    )

    DM_err = vp.Param(
        name='dm_err',
        ucd='stat.error;phys.dispMeasure',
        unit='pc/cm^3',
        ac=True,
        value=params['dm_err']
    )

    Width = vp.Param(
        name='width',
        ucd='time.duration;src.var.pulse',
        unit='ms',
        ac=True,
        value=params['width']
    )

    SNR = vp.Param(
        name='snr',
        ucd='stat.snr',
        unit='None',
        ac=True,
        value=params['snr']
    )

    Flux = vp.Param(
        name='flux',
        ucd='phot.flux',
        unit='Jy',
        ac=True,
        value=params['flux']
    )

    Flux.Description = 'Calculated from radiometer equation. Not calibrated.'

    Gl = vp.Param(
        name='gl',
        value=str(params['gl']),
        ucd='pos.galactic.lon',
        unit='Degrees',
        ac=True
    )

    Gb = vp.Param(
        name='gb',
        value=str(params['gb']),
        ucd='pos.galactic.lat',
        unit='Degrees',
        ac=True
    )

    v.What.append(
        vp.Group(
            params=[DM, DM_err, Width, SNR, Flux, Gl, Gb],
            name='event parameters'
        )
    )

    # advanced parameters (note, change script if using a differeing MW model)
    mw_dm = vp.Param(
        name='MW_dm_limit',
        value=params['mw_dm_limit'],
        unit='pc/cm^3',
        ac=True
    )

    mw_model = vp.Param(
        name='galactic_electron_model',
        value=params['galactic_electron_model']
    )

    redshift_inferred = vp.Param(
        name='redshift_inferred',
        ucd='src.redshift',
        unit='None',
        value=z
    )

    redshift_inferred.Description = 'Redshift estimated using z = DM/1200.0 (Ioka 2003)'

    v.What.append(
        vp.Group(
            params=[mw_dm, mw_model, redshift_inferred],
            name='advanced parameters'
        )
    )

    # WhereWhen
    coords = vp.Position2D(
        ra=str(params['ra']),
        dec=str(params['dec']),
        err=errDeg,
        units='deg',
        system=vp.definitions.sky_coord_system.utc_icrs_geo
    )

    # add utc timezone info that is required for vp
    obs_time = utc.datetime.replace(tzinfo=pytz.UTC)

    vp.add_where_when(
        v,
        coords=coords,
        obs_time=obs_time,
        observatory_location=params['observatory_location']
    )

    # Why
    vp.add_why(
        v,
        importance=params['importance']
    )
    v.Why.Name = params['name']

    # debug output
    #for item in [v.Who, v.What, v.WhereWhen, v.Why]:
    #    print(vp.prettystr(item))

    # check if the packet is voevent v2.0 compliant
    if not vp.valid_as_v2_0(v):
        # print debug output
        vp.assert_valid_as_v2_0(v)

    return vp.prettystr(v)
