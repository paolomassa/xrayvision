"""
======================================
Solar Orbiter/STIX Visibility Imaging
======================================

Imports

"""

import pickle
import urllib.request

import astropy.units as apu
import matplotlib.pyplot as plt

from xrayvision.clean import vis_clean
from xrayvision.imaging import vis_psf_map, vis_to_map
from xrayvision.mem import mem

###############################################################################
# Create images from STIX visibility data.
#
# The STIX data has already been prepared and stored in python pickle format
# the variables can be simply restored.

stix_data = pickle.load(urllib.request.urlopen("https://pub099.cs.technik.fhnw.ch/demo/stix_vis.pkl"))

time_range, energy_range, offset, stix_vis = stix_data
stix_vis.phase_centre = [0, 0] * apu.arcsec
stix_vis.offset = offset

###############################################################################
# Lets have a look at the point spread function (PSF) or dirty beam

psf_map = vis_psf_map(stix_vis, shape=(129, 129) * apu.pixel, pixel_size=2 * apu.arcsec / apu.pix, scheme="uniform")
psf_map.plot()

###############################################################################
# Back projection

backproj_map = vis_to_map(stix_vis, shape=(129, 129) * apu.pixel, pixel_size=2 * apu.arcsec / apu.pix, scheme="uniform")
backproj_map.plot()

###############################################################################
# Clean

clean_map, model_map, resid_map = vis_clean(
    stix_vis,
    shape=[129, 129] * apu.pixel,
    pixel_size=[2, 2] * apu.arcsec / apu.pix,
    clean_beam_width=20 * apu.arcsec,
    niter=100,
)
clean_map.plot()

###############################################################################
# MEM

mem_map = mem(stix_vis, shape=[129, 129] * apu.pixel, pixel_size=[2, 2] * apu.arcsec / apu.pix)
mem_map.plot()

###############################################################################
# Comparison
fig = plt.figure(figsize=(10, 10))
fig.add_subplot(221, projection=psf_map)
fig.add_subplot(222, projection=backproj_map)
fig.add_subplot(223, projection=clean_map)
fig.add_subplot(224, projection=mem_map)
axs = fig.get_axes()
psf_map.plot(axes=axs[0])
axs[0].set_title("PSF")
backproj_map.plot(axes=axs[1])
axs[1].set_title("Back Projection")
clean_map.plot(axes=axs[2])
axs[2].set_title("Clean")
mem_map.plot(axes=axs[3])
axs[3].set_title("MEM")
plt.show()
