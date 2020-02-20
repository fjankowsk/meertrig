from datetime import datetime
import pytz
from xml.dom import minidom

import astropy.units as units
from astropy.time import Time
import voeventparse as vp


def generate_voevent(obs, event):
    """
    Generate a VOEvent.

    Parameters
    ----------
    obs: dict
        Observatory parameters.
    event: dict
        Event parameters.
    """

    z = event['dm'] / 1200.0  #May change
    errDeg = event['beam_semi_major'] / 60.0

    # Parse UTC
    utc = event['utc']
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

    ivorn = ''.join([event['name'], str(utc_hh), str(utc_mm), '/', str(mjd_now)]) 

    v = vp.Voevent(stream='nl.astron.apertif/alert', stream_id=ivorn, role=vp.definitions.roles.test)
    #v = vp.Voevent(stream='nl.astron.apertif/alert', stream_id=ivorn, role=vp.definitions.roles.observation)

    # Author origin information
    vp.set_who(v, date=datetime.datetime.utcnow(), author_ivorn="nl.astron")
    # Author contact information
    vp.set_author(v,
                  title=obs['title'],
                  contactName=obs['contact_name'],
                  contactEmail=obs['contact_email'],
                  shortName=event['short_name'])

    # Parameter definitions

    #Apertif-specific observing configuration %%TODO: update parameters as necessary for new obs config
    beam_sMa = vp.Param(name="beam_semi-major_axis",
                        unit="MM",
                        ucd="instr.beam;pos.errorEllipse;phys.angSize.smajAxis",
                        ac=True,
                        value=event['beam_semi_major'])

    beam_sma = vp.Param(name="beam_semi-minor_axis",
                        unit="MM",
                        ucd="instr.beam;pos.errorEllipse;phys.angSize.sminAxis",
                        ac=True,
                        value=event['beam_semi_minor'])

    beam_rot = vp.Param(name="beam_rotation_angle",
                        unit="Degrees",
                        ucd="instr.beam;pos.errorEllipse;instr.offset",
                        ac=True,
                        value=event['beam_rotation_angle'])

    tsamp = vp.Param(name="sampling_time",
                     value=event['tsamp'],
                     unit="ms",
                     ucd="time.resolution",
                     ac=True)

    bw = vp.Param(name="bandwidth",
                  value=300.0,
                  unit="MHz",
                  ucd="instr.bandwidth",
                  ac=True)

    nchan = vp.Param(name="nchan", value="1536", dataType="int", ucd="meta.number;em.freq;em.bin", unit="None")
    cf = vp.Param(name="centre_frequency", value=1400.0, unit="MHz", ucd="em.freq;instr", ac=True)
    npol = vp.Param(name="npol", value="2", dataType="int", unit="None")
    bits = vp.Param(name="bits_per_sample", value="8", dataType="int", unit="None")
    gain = vp.Param(name="gain", value=1.0, unit="K/Jy", ac=True)
    tsys = vp.Param(name="tsys", value=75.0, unit="K", ucd="phot.antennaTemp", ac=True)
    backend = vp.Param(name="backend", value="ARTS")
    # beam = vp.Param(name="beam", value= )

    v.What.append(vp.Group(params=[beam_sMa, beam_sma, beam_rot, tsamp, bw, nchan, cf, npol, bits, gain, tsys, backend], name="observatory parameters"))

    # event parameters
    DM = vp.Param(name="dm", ucd="phys.dispMeasure", unit="pc/cm^3", ac=True, value=event['dm'])
    # DM_err = vp.Param(name="dm_err", ucd="stat.error;phys.dispMeasure", unit="pc/cm^3", ac=True, value=dm_err)
    Width = vp.Param(name="width", ucd="time.duration;src.var.pulse", unit="ms", ac=True, value=event['width'])
    SNR = vp.Param(name="snr", ucd="stat.snr", unit="None", ac=True, value=event['snr'])
    Flux = vp.Param(name="flux", ucd="phot.flux", unit="Jy", ac=True, value=event['flux'])
    Flux.Description = "Calculated from radiometer equation. Not calibrated."
    Gl = vp.Param(name="gl", ucd="pos.galactic.lon", unit="Degrees", ac=True, value=event['gl'])
    Gb = vp.Param(name="gb", ucd="pos.galactic.lat", unit="Degrees", ac=True, value=event['gb'])

    v.What.append(vp.Group(params=[DM, Width, SNR, Flux, Gl, Gb], name="event parameters"))
    # v.What.append(vp.Group(params=[DM, DM_err, Width, SNR, Flux, Gl, Gb], name="event parameters"))

    #Advanced parameters (note, change script if using a differeing MW model)
    mw_dm = vp.Param(name="MW_dm_limit", unit="pc/cm^3", ac=True, value=event['ymw16'])
    mw_model = vp.Param(name="galactic_electron_model", value="YMW16")
    redshift_inferred = vp.Param(name="redshift_inferred", ucd="src.redshift", unit="None", value=z)
    redshift_inferred.Description = "Redshift estimated using z = DM/1200.0 (Ioka 2003)"

    v.What.append(vp.Group(params=[mw_dm, mw_model, redshift_inferred], name="advanced parameters"))

    # WhereWhen
    coords = vp.Position2D(ra=event['ra'],
                           dec=event['dec'],
                           err=errDeg,
                           units='deg',
                           system=vp.definitions.sky_coord_system.utc_icrs_geo)

    obs_time = datetime(utc_YY, utc_MM, utc_DD, utc_hh, utc_mm, int(utc_ss), tzinfo=pytz.UTC)

    vp.add_where_when(v,
                      coords=coords,
                      obs_time=obs_time,
                      observatory_location="MKT")

    # Why
    vp.add_why(v, importance=event['importance'])
    v.Why.Name = event['name']

    if vp.valid_as_v2_0(v):
        with open('%s.xml' % event['utc'], 'wb') as f:
            voxml = vp.dumps(v)
            xmlstr = minidom.parseString(voxml).toprettyxml(indent="   ")
            f.write(xmlstr)
            print(vp.prettystr(v.Who))
            print(vp.prettystr(v.What))
            print(vp.prettystr(v.WhereWhen))
            print(vp.prettystr(v.Why))
    else:
        print("Unable to write file %s.xml" % event['name'])
