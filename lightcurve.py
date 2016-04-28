import numpy as np

from astropy.io import fits

def lightcurve(archivo):
    """
    Extrae datos relevantes de los .fits
    Los datos que extrae son los mismos que se usaron en el estudio de Debray y Wu
    """
    hdu = fits.open(archivo)
    datos = np.array(hdu[1].data.tolist())
    tiempo = datos[:, 0]
    sap_flux = datos[:, 3]
    sap_bkg = datos[:, 5]
    pcdsap_flux = datos[:, 7]
    mom_centr1 = datos[:, 14]
    mom_centr2 = datos[:, 16]
    pos_corr1 = datos[:, 18]
    pos_corr2 = datos[:, 19]
    hdu.close()
    return [tiempo, sap_flux, sap_bkg, pcdsap_flux, mom_centr1, mom_centr2, pos_corr1, pos_corr2]