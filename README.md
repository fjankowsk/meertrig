# MeerTRAP Trigger Tools #

This repository contains realtime VOEvent triggering software for the MeerTRAP project at the MeerKAT telescope. The code is mainly developed for Python 3 (and in particular version 3.7), but Python 2 (e.g. version 2.7) should work fine.

## Author ##

The software is primarily developed and maintained by Fabian Jankowski. For more information, feel free to contact me via: fabian.jankowski at manchester.ac.uk.

## Citation ##

If you make use of the software, please add a link to this repository and cite our upcoming paper.

## Installation ##

The easiest and recommended way to install the software is through `pip` directly from the bitbucket repository. For example, to install the master branch of the code, use the following command:

`pip3 install git+https://bitbucket.org/jankowsk/meertrig.git@master`

## Example Usage ##

The `meertrig` software makes it easy to construct and emit a VOEvent packet to a given VOEvent broker. An example is given below.

```python
from meertrig import VOEvent

params = {
    'utc': utc,
    'title': 'Detection of test event',
    'short_name': 'Test event',
    'beam_semi_major': semiMaj,
    'beam_semi_minor': semiMin,
    'beam_rotation_angle': 0.0,
    'tsamp': 0.367,
    'cfreq': 1284.0,
    'bandwidth': 856.0,
    'nchan': 4096,
    'beam': 123,
    'dm': dm,
    'dm_err': dm_err,
    'width': width,
    'snr': snr,
    'flux': flux,
    'ra': coord.ra.deg,
    'dec': coord.dec.deg,
    'gl': coord.galactic.l.deg,
    'gb': coord.galactic.b.deg,
    'name': name,
    'importance': importance,
    'internal': 1,
    'open_alert': 0,
    'test': 1,
    'product_id': product_id
}

v = VOEvent(host=hostname, port=port)
ve = v.generate_event(params, True)
v.send_event(ve)
```
