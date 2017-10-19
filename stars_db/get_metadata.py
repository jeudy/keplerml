from os import listdir
from os.path import join

from astropy.io import fits

def get_list_of_dicts(dire):
    """
    Obtiene las listas de diccionarios para uso con las funciones de stars_db_manager

    (str) dire: Directorio en donde se encuentran los fits

    """
    list_of_dicts_lightcurve_metadata = []
    list_of_dicts_metadata = []
    archivos = listdir(dire)
    for i in range(len(archivos)):
        archivos[i] = join(dire, archivos[i])
    for archivo in archivos:
        list_of_dicts_lightcurve_metadata.append(get_star_lightcurve_metadata(archivo))
        list_of_dicts_metadata.append(get_star_metadata(archivo))
    return (list_of_dicts_metadata, list_of_dicts_lightcurve_metadata)

def get_star_lightcurve_metadata(fits_arch):
    """
    Obtiene los metadatos de la curva de luz de un archivo fits para uso con las funciones de stars_db_manager

    (str) fits_arch: Archivo del que se obtendran los metadatos
    """

    try:
        hdu = fits.open(fits_arch)
    except IOError as ex:
        print "Error procesando FIT file: {0} - {1}".format(fits_arch, str(ex))
        return {}

    lightcurve_metadata = {'kepler_id':hdu[1].header["KEPLERID"],
                    'source_filename':fits_arch,
                    'exposure':hdu[1].header["EXPOSURE"],
                    'bjd_ref_integer':check_if_null(hdu[1].header["BJDREFI"]),
                    'bjd_ref_fraction':check_if_null(hdu[1].header["BJDREFF"]),
                    'time_elapsed':check_if_null(hdu[1].header["TELAPSE"]),
                    'time_live':check_if_null(hdu[1].header["LIVETIME"]),
                    'time_start':check_if_null(hdu[1].header["TSTART"]),
                    'time_stop':check_if_null(hdu[1].header["TSTOP"]),
                    'lc_start':check_if_null(hdu[1].header["LC_START"]),
                    'lc_end':check_if_null(hdu[1].header["LC_END"]),
                    'deadtime_correction':check_if_null(hdu[1].header["DEADC"]),
                    'bin_time':check_if_null(hdu[1].header["TIMEPIXR"]),
                    'relative_time_error':check_if_null(hdu[1].header["TIERRELA"]),
                    'absolute_time_error':check_if_null(hdu[1].header["TIERABSO"]),
                    'integration_time':check_if_null(hdu[1].header["INT_TIME"]),
                    'readout_time':check_if_null(hdu[1].header["READTIME"]),
                    'frame_time':check_if_null(hdu[1].header["FRAMETIM"]),
                    'number_of_frames':check_if_null(hdu[1].header["NUM_FRM"]),
                    'time_resolution':check_if_null(hdu[1].header["TIMEDEL"]),
                    'observation_date_start':format_time_data(hdu[1].header["DATE-OBS"]),
                    'observation_date_end':format_time_data(hdu[1].header["DATE-END"]),
                    'background_substracted':check_if_null(hdu[1].header["BACKAPP"]),
                    'deadtime_applied':check_if_null(hdu[1].header["DEADAPP"]),
                    'vignetting_correction':check_if_null(hdu[1].header["VIGNAPP"]),
                    'gain':check_if_null(hdu[1].header["GAIN"]),
                    'read_noise':check_if_null(hdu[1].header["READNOIS"]),
                    'read_per_cadence':check_if_null(hdu[1].header["NREADOUT"]),
                    'mean_black':check_if_null(hdu[1].header["MEANBLCK"]),
                    'long_cadence_fixed_offset':check_if_null(hdu[1].header["LCFXDOFF"]),
                    'short_cadence_fixed_offset':check_if_null(hdu[1].header["SCFXDOFF"]),
                    'crowd_sap':check_if_null(hdu[1].header["CROWDSAP"]),
                    'target_variability':check_if_null(hdu[1].header["PDCVAR"])}
    hdu.close()
    return lightcurve_metadata

def format_time_data(timestamp):
    """
    Cambia el formato de tiempo que se utiliza en los fits a uno que se utiliza en MySQL

    (str) timestamp: Tiempo que se va a cambiar
    """
    return timestamp.replace('T', ' ').replace('Z', '')

def get_star_metadata(fits_arch):
    """
    Obtiene los metadatos de un archivo fits para uso con las funciones de stars_db_manager

    (str) fits_arch: Archivo del que se obtendran los metadatos
    """
    try:
        hdu = fits.open(fits_arch)
    except IOError as ex:
        print "Error procesando FIT file: {0} - {1}".format(fits_arch, str(ex))
        return {}
    metadata = {'kepler_id':hdu[0].header["KEPLERID"],
                    'source_filename':fits_arch,
                    'confirmed':check_if_confirmed(hdu[0].header["KEPLERID"]),
                    'negative':check_if_false_positive(hdu[0].header["KEPLERID"]),
                    'channel':check_if_null(hdu[0].header["CHANNEL"]),
                    'sky_group':check_if_null(hdu[0].header["SKYGROUP"]),
                    'module':check_if_null(hdu[0].header["MODULE"]),
                    'output':check_if_null(hdu[0].header["OUTPUT"]),
                    'quarter':check_if_null(hdu[0].header["QUARTER"]),
                    'season':check_if_null(hdu[0].header["SEASON"]),
                    'data_release':check_if_null(hdu[0].header["DATA_REL"]),
                    'observing_mode':check_if_null(hdu[0].header["OBSMODE"]),
                    'coordinates_ra':check_if_null(hdu[0].header["RA_OBJ"]),
                    'coordinates_dec':check_if_null(hdu[0].header["DEC_OBJ"]),
                    'ssds_g_magnitude':check_if_null(hdu[0].header["GMAG"]),
                    'ssds_r_magnitude':check_if_null(hdu[0].header["RMAG"]),
                    'ssds_i_magnitude':check_if_null(hdu[0].header["IMAG"]),
                    'ssds_z_magnitude':check_if_null(hdu[0].header["ZMAG"]),
                    'j_magnitude':check_if_null(hdu[0].header["JMAG"]),
                    'h_magnitude':check_if_null(hdu[0].header["HMAG"]),
                    'k_magnitude':check_if_null(hdu[0].header["KMAG"]),
                    'kepler_magnitude':check_if_null(hdu[0].header["KEPMAG"]),
                    'gr_color':check_if_null(hdu[0].header["GRCOLOR"]),
                    'jk_color':check_if_null(hdu[0].header["JKCOLOR"]),
                    'gk_color':check_if_null(hdu[0].header["GKCOLOR"]),
                    'effective_temperature':check_if_null(hdu[0].header["TEFF"]),
                    'surface_gravity':check_if_null(hdu[0].header["LOGG"]),
                    'fe_h_metallicity':check_if_null(hdu[0].header["FEH"]),
                    'radius':check_if_null(hdu[0].header["RADIUS"]),
                    'load_timestamp':check_if_null(hdu[0].header["DATE"])}
    hdu.close()
    return metadata

def check_if_confirmed(kplr_id):
    with open('Kepler_confirmed_list.txt', 'r') as f:
        for lines in f:
            if "kplr{zeroes}{ids}".format(zeroes='0'*(9-len(str(kplr_id))), ids=kplr_id) == lines.strip():
                return True
    return False

def check_if_false_positive(kplr_id):
    with open('false_positives_list.txt', 'r') as f:
        for lines in f:
            if "kplr{zeroes}{ids}".format(zeroes='0'*(9-len(str(kplr_id))), ids=kplr_id) == lines.strip():
                return True
    return False

def check_if_null(abt):
    if str(type(abt)) == "<class 'astropy.io.fits.card.Undefined'>":
        return None
    else:
        return abt
