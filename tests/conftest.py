import pytest
import casatasks
import os
from astropy.utils.data import download_file


# create a fixture for temporary MS file itself
@pytest.fixture(scope="session")
def ms_cont_path(tmp_path_factory):
    # Generate a continuum MS

    # load test FITS file provided by package
    # assuming we're running from top directory
    fits_path = "tests/logo_cont.fits"
    fits_path = download_file(
        "https://zenodo.org/record/4711811/files/logo_cont.fits",
        cache=True,
        pkgname="visread",
    )

    # use the tmp_path directory provided by pytest to automatically
    # clean up all of the files when we're done
    outdir = str(tmp_path_factory.mktemp("cont"))

    inbright = 2e-5  # Jy/pixel
    indirection = "J2000 04h55m10.98834s +030.21.58.879285"

    # change to outdir
    curdir = os.getcwd()
    os.chdir(outdir)

    casatasks.simobserve(
        skymodel=fits_path,
        inbright="{:}Jy/pixel".format(inbright),
        incenter="230GHz",
        indirection=indirection,
        inwidth="8GHz",
        hourangle="transit",
        totaltime="3600s",
        graphics="none",
        overwrite=True,
        obsmode="int",  # interferometer
        antennalist=curdir + "/" + "tests/alma.cycle7.7.cfg",
    )

    os.chdir(curdir)
    ms_path = outdir + "/sim/sim.alma.cycle7.7.ms"

    return ms_path


@pytest.fixture(scope="session")
def ms_cube_path(tmp_path_factory):
    # Generate an MS for a spectral cube

    # load test FITS file provided by package
    # assuming we're running from top directory
    fits_path = download_file(
        "https://zenodo.org/record/4711811/files/logo_cube.fits",
        cache=True,
        pkgname="visread",
    )

    # use the tmp_path directory provided by pytest to automatically
    # clean up all of the files when we're done
    outdir = str(tmp_path_factory.mktemp("cube"))

    # change to outdir
    curdir = os.getcwd()
    os.chdir(outdir)

    casatasks.simobserve(
        skymodel=fits_path,
        hourangle="transit",
        totaltime="3600s",
        graphics="none",
        thermalnoise="tsys-atm",
        overwrite=True,
        obsmode="int",  # interferometer
        antennalist=curdir + "/" + "tests/alma.cycle7.7.cfg",
    )

    os.chdir(curdir)
    ms_path = outdir + "/sim/sim.alma.cycle7.7.ms"

    return ms_path


# path to MS cube with MODEL_DATA column