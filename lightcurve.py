import numpy as np

from astropy.io import fits

def lightcurve(archivo):
    """
    Extrae datos relevantes de los .fits
    """
    hdu = fits.open(archivo)
    datos = np.array(hdu[1].data.tolist())

    time = datos[:, 0]
    timecorr = datos[:, 1]
    cadenceco = datos[:, 2]
    sap_flux = datos[:, 3]
    sap_flux_err = datos[:, 4]
    sap_bkg = datos[:, 5]
    sap_bkg_err = datos[:, 6]
    pdcsap_flux = datos[:, 7]
    pdcsap_flux_err = datos[:, 8]
    sap_quality = datos[:, 9]
    psf_centr1 = datos[:, 10]
    psf_centr1_err = datos[:, 11]
    psf_centr2 = datos[:, 12]
    psf_centr2_err = datos[:, 13]
    mom_centr1 = datos[:, 14]
    mom_centr1_err = datos[:, 15]
    mom_centr2 = datos[:, 16]
    mom_centr2_err = datos[:, 17]
    pos_corr1 = datos[:, 18]
    pos_corr2 = datos[:, 19]

    hdu.close()
    return [time, timecorr, cadenceco, sap_flux, sap_flux_err, sap_bkg, sap_bkg_err, pdcsap_flux, pdcsap_flux_err, sap_quality, psf_centr1, psf_centr1_err, psf_centr2, psf_centr2_err, mom_centr1, mom_centr1_err, mom_centr2, mom_centr2_err, pos_corr1, pos_corr2]