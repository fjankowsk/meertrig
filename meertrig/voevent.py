from datetime import datetime
import pytz
from xml.dom import minidom

import astropy.units as units
from astropy.time import Time
import voeventparse as vp


def generate_voevent(params):
    """
    Generate a VOEvent.

    Parameters
    ----------
    obs: dict
        Observatory parameters.
    event: dict
        Event parameters.
    """

    z = params['dm'] / 1200.0  # may change
    errDeg = params['beam_semi_major'] / 60.0

    # parse UTC
    utc = params['utc']
    utc_YY = int(utc[:4])
    utc_MM = int(utc[5:7])
    utc_DD = int(utc[8:10])
    utc_hh = int(utc[11:13])
    utc_mm = int(utc[14:16])
    utc_ss = float(utc[17:])
    t = Time('T'.join([utc[:10], utc[11:]]), scale='utc', format='isot')
    mjd = t.mjd

    now = Time.now()
    mjd_now = now.mjd

    ivorn = ''.join([params['name'], str(utc_hh), str(utc_mm), '/', str(mjd_now)])

    v = vp.Voevent(stream='nl.astron.apertif/alert', stream_id=ivorn, role=vp.definitions.roles.test)
    #v = vp.Voevent(stream='nl.astron.apertif/alert', stream_id=ivorn, role=vp.definitions.roles.observation)

    # author origin information
    vp.set_who(
        v,
        date=datetime.utcnow(),
        author_ivorn="nl.astron"
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

    # apertif-specific observing configuration
    # TODO: update parameters as necessary for new obs config
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

    bw = vp.Param(
        name='bandwidth',
        value=params['bandwidth'],
        unit='MHz',
        ucd='instr.bandwidth',
        ac=True
    )

    nchan = vp.Param(
        name='nchan',
        value=params['nchan'],
        dataType='int',
        ucd='meta.number;em.freq;em.bin',
        unit='None'
    )

    cf = vp.Param(
        name='centre_frequency',
        value=params['cfreq'],
        unit='MHz',
        ucd='em.freq;instr',
        ac=True
    )

    npol = vp.Param(
        name='npol',
        value='2',
        dataType='int',
        unit='None'
    )

    bits = vp.Param(
        name='bits_per_sample',
        value='8',
        dataType='int',
        unit='None'
    )

    gain = vp.Param(
        name="gain",
        value=1.0,
        unit="K/Jy",
        ac=True
    )

    tsys = vp.Param(
        name="tsys",
        value=75.0,
        unit="K",
        ucd="phot.antennaTemp",
        ac=True
    )

    backend = vp.Param(
        name="backend",
        value="ARTS"
    )

    # beam = vp.Param(name="beam", value= )

    v.What.append(
        vp.Group(
            params=[beam_sMa, beam_sma, beam_rot, tsamp, bw, nchan, cf, npol, bits, gain, tsys, backend],
            name='observatory parameters'
        )
    )

    # event parameters
    DM = vp.Param(
        name="dm",
        ucd="phys.dispMeasure",
        unit="pc/cm^3",
        ac=True,
        value=params['dm']
    )

    DM_err = vp.Param(
        name="dm_err",
        ucd="stat.error;phys.dispMeasure",
        unit="pc/cm^3",
        ac=True,
        value=params['dm_err']
    )

    Width = vp.Param(
        name="width",
        ucd="time.duration;src.var.pulse",
        unit="ms",
        ac=True,
        value=params['width']
    )

    SNR = vp.Param(
        name="snr",
        ucd="stat.snr",
        unit="None",
        ac=True,
        value=params['snr']
    )

    Flux = vp.Param(
        name="flux",
        ucd="phot.flux",
        unit="Jy",
        ac=True,
        value=params['flux']
    )

    Flux.Description = 'Calculated from radiometer equation. Not calibrated.'

    Gl = vp.Param(
        name="gl",
        ucd="pos.galactic.lon",
        unit="Degrees",
        ac=True,
        value=params['gl']
    )

    Gb = vp.Param(
        name="gb",
        ucd="pos.galactic.lat",
        unit="Degrees",
        ac=True,
        value=params['gb']
    )

    v.What.append(
        vp.Group(params=[DM, Width, SNR, Flux, Gl, Gb], name="event parameters")
    )
    # v.What.append(vp.Group(params=[DM, DM_err, Width, SNR, Flux, Gl, Gb], name="event parameters"))

    # advanced parameters (note, change script if using a differeing MW model)
    mw_dm = vp.Param(
        name="MW_dm_limit",
        unit="pc/cm^3",
        ac=True,
        value=params['ymw16']
    )

    mw_model = vp.Param(
        name="galactic_electron_model",
        value="YMW16"
    )

    redshift_inferred = vp.Param(
        name="redshift_inferred",
        ucd="src.redshift",
        unit="None",
        value=z
    )

    redshift_inferred.Description = "Redshift estimated using z = DM/1200.0 (Ioka 2003)"

    v.What.append(
        vp.Group(
            params=[mw_dm, mw_model, redshift_inferred],
            name='advanced parameters'
        )
    )

    # WhereWhen
    coords = vp.Position2D(
        ra=params['ra'],
        dec=params['dec'],
        err=errDeg,
        units='deg',
        system=vp.definitions.sky_coord_system.utc_icrs_geo
    )

    obs_time = datetime(utc_YY, utc_MM, utc_DD, utc_hh, utc_mm, int(utc_ss), tzinfo=pytz.UTC)

    vp.add_where_when(
        v,
        coords=coords,
        obs_time=obs_time,
        observatory_location="MKT"
    )

    # Why
    vp.add_why(
        v,
        importance=params['importance']
    )
    v.Why.Name = params['name']

    if vp.valid_as_v2_0(v):
        filename = '{0}.xml'.format(params['utc'])

        with open(filename, 'wb') as f:
            voxml = vp.dumps(v)
            xmlstr = minidom.parseString(voxml).toprettyxml(indent="   ")
            f.write(xmlstr)
            print(vp.prettystr(v.Who))
            print(vp.prettystr(v.What))
            print(vp.prettystr(v.WhereWhen))
            print(vp.prettystr(v.Why))
    else:
        print('Unable to write file {0}.xml'.format(params['name']))
