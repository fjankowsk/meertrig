#
#   2020 Fabian Jankowski
#   VOEvent class.
#

from astropy.time import Time
import pytz
import voeventparse as vp
import fourpiskytools

from meertrig.dm_helpers import get_mw_dm


class VOEvent:
    def __init__(self, host, port):
        """
        Class to handle VOEvents.

        Parameters
        ----------
        host: str
            The name or IP of the VOEvent broker to use.
        port: int
            The port to use to submit VOEvent to on the broker.
        """

        self.host = host
        self.port = port


    def generate_event(self, params, is_test):
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
        v: ~voeventparse.Voevent
            The created VOEvent packet.

        Raises
        ------
        lxml.etree.DocumentInvalid
            If the event packet does not comply to the VOEvent standard.
        """

        # determine milky way dm
        mw_dm = get_mw_dm(params['gl'], params['gb'], params['galactic_electron_model'])

        # round to 2 significant digits and convert to string
        mw_dm = "{0:.2f}".format(mw_dm)

        # inferred redshift
        z = params['dm'] / 1200.0

        # positional uncertainty
        errDeg = params['beam_semi_major'] / 60.0

        # parse utc
        utc = Time(params['utc'], format='iso', scale='utc')

        # construct stream
        stream = '{0}/alert'.format(params['author_ivorn'])

        # construct ivorn
        ivorn = '{0}_FRB{1}/{2:.6f}'.format(
            params['name'],
            utc.strftime(r'%Y%m%d_%H%M%S'),
            utc.mjd
        )

        # switch between test and on-sky events
        if is_test:
            role = vp.definitions.roles.test
        else:
            role = vp.definitions.roles.observation

        v = vp.Voevent(
            stream=stream,
            stream_id=ivorn,
            role=role
        )

        # 1) Who (author origin information)
        vp.set_who(
            v,
            date=Time.now().datetime,
            author_ivorn=params['author_ivorn']
        )

        # 2) author contact information
        vp.set_author(
            v,
            title=params['title'],
            contactName=params['contact_name'],
            contactEmail=params['contact_email'],
            shortName=params['short_name']
        )

        # meta data
        internal = vp.Param(
            name='internal',
            value=str(params['internal']),
            dataType='int',
            unit='None'
        )

        internal.Description = 'If 1, event should be distributed among the MeerTRAP collaboration only. Open distribution if 0.'

        open_alert = vp.Param(
            name='open_alert',
            value=str(params['open_alert']),
            dataType='int',
            unit='None'
        )

        open_alert.Description = 'If 1, this is an open event. 0 if not.'

        test = vp.Param(
            name='test',
            value=str(params['test']),
            dataType='int',
            unit='None'
        )

        test.Description = 'If 1, this is a test event. 0 if not.'

        product_id = vp.Param(
            name='product_id',
            value=str(params['product_id']),
            dataType='string',
            unit='None'
        )

        product_id.Description = 'This parameter is relevant to the MPIfR Filterbank Beamformer instrument at MeerKAT only. It designates the sub-array in which the event was discovered.'

        # 3) What (meta data)
        v.What.append(
            vp.Group(
                params=[internal, open_alert, test, product_id],
                name='meta information'
            )
        )

        # instrument-specific parameters
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
            value=params['backend'],
            dataType='string'
        )

        beam = vp.Param(
            name='beam',
            value=str(params['beam']),
            unit='None',
            dataType='int'
        )

        beam.Description = 'Detection beam number out of a total of up to 768 beams on the sky.'

        # 4) What (observatory parameters)
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
            ucd='phot.flux;em.radio',
            unit='Jy',
            ac=True,
            value=params['flux']
        )

        Flux.Description = 'Calculated using the radiometer equation. Not calibrated.'

        Gl = vp.Param(
            name='gl',
            value=str(params['gl']),
            ucd='pos.galactic.lon',
            unit='Degrees',
            dataType='float'
        )

        Gb = vp.Param(
            name='gb',
            value=str(params['gb']),
            ucd='pos.galactic.lat',
            unit='Degrees',
            dataType='float'
        )

        # 5) What (event parameters)
        v.What.append(
            vp.Group(
                params=[DM, DM_err, Width, SNR, Flux, Gl, Gb],
                name='event parameters'
            )
        )

        # advanced parameters
        mw_dm = vp.Param(
            name='MW_dm_limit',
            value=params['mw_dm_limit'],
            unit='pc/cm^3',
            dataType='float'
        )

        mw_model = vp.Param(
            name='galactic_electron_model',
            value=params['galactic_electron_model'],
            dataType='string'
        )

        redshift_inferred = vp.Param(
            name='redshift_inferred',
            ucd='src.redshift',
            unit='None',
            value=z,
            ac=True
        )

        redshift_inferred.Description = 'Redshift estimated using z = DM/1200.0 (Ioka 2003)'

        # 6) What (advanced parameters)
        v.What.append(
            vp.Group(
                params=[mw_dm, mw_model, redshift_inferred],
                name='advanced parameters'
            )
        )

        # event position
        coords = vp.Position2D(
            ra=str(params['ra']),
            dec=str(params['dec']),
            err=errDeg,
            units='deg',
            system=vp.definitions.sky_coord_system.utc_icrs_geo
        )

        # add utc timezone info that is required for vp
        obs_time = utc.datetime.replace(tzinfo=pytz.UTC)

        # 7) WhereWhen
        vp.add_where_when(
            v,
            coords=coords,
            obs_time=obs_time,
            observatory_location=params['observatory_location']
        )

        # 8) How
        vp.add_how(
            v,
            descriptions=params['descriptions']
        )

        # 9) Why
        vp.add_why(
            v,
            importance=params['importance']
        )

        v.Why.Description = 'Probability of event being an astrophysical detection, based on machine-learning classifier.'

        # check if the packet is voevent v2.0 compliant
        vp.assert_valid_as_v2_0(v)

        print(vp.prettystr(v))

        return v


    def send_event(self, voevent):
        """
        Send an event to the VOEvent broker.

        Parameters
        ----------
        voevent: str
            The VOEvent to be send.

        Raises
        ------
        lxml.etree.DocumentInvalid
            If the event packet does not comply to the VOEvent standard.
        """

        # check if the packet is voevent v2.0 compliant
        vp.assert_valid_as_v2_0(voevent)

        # we could wrap 'comet-sendvo' here ourselves to avoid using fourpiskytools
        # it just does that for us
        fourpiskytools.comet.send_voevent(voevent, self.host, self.port)
