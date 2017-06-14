import sys
import datetime
import time
from get_metadata import get_list_of_dicts, get_star_lightcurve_metadata, get_star_metadata
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Float, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from os import listdir
from os.path import join
import warnings

DB_USER = 'root'
#DB_PASS = 'jBV205760292'
DB_PASS = 'cinespa'
DB_DATABASE = 'kepler_stars'
DB_HOST = '127.0.0.1'

DB_URI = "mysql+mysqldb://{user}:{password}@{host}/{database}".format(user=DB_USER,
                                                                      password=DB_PASS,
                                                                      host=DB_HOST,
                                                                      database=DB_DATABASE)

engine = create_engine("mysql+mysqldb://{user}:{password}@{host}/{database}".format(user=DB_USER,
                                                                                    password=DB_PASS,
                                                                                    host=DB_HOST,
                                                                                    database=DB_DATABASE),
                                                                                    pool_recycle=280)

Session = scoped_session(sessionmaker(bind=engine))

class StarsDBManager(object):

    def __init__(self):
        self.metadata = MetaData()
        self.metadata.bind = engine
        self.metadata.reflect()

    def get_binded_metadata(self):
        return self.metadata

    def create_schema(self):

        metadata = MetaData()

        # Tabla para almacenar los metadatos de la estrella
        # Del HDU[0].headers de los FITS files

        star_metadata_table = Table("stars_metadata", metadata,
                                    Column('kepler_id', String(100), primary_key=True),
                                    Column('source_filename', String(100), primary_key=True),
                                    Column('confirmed', Boolean, nullable=False),
                                    Column('negative', Boolean, nullable=False),
                                    Column('channel', Integer, nullable=True),
                                    Column('sky_group', Integer, nullable=True),
                                    Column('module', Integer, nullable=True),
                                    Column('output', Integer, nullable=True),
                                    #Column('quarter', Integer, nullable=False),
                                    Column('quarter', Integer, nullable=True),
                                    #Column('season', Integer, nullable=False),
                                    Column('season', Integer, nullable=True),
                                    Column('data_release', Integer, nullable=True),
                                    Column('observing_mode', String(255), nullable=True),
                                    #Column('coordinates_ra', Float, nullable=False),
                                    Column('coordinates_ra', Float, nullable=True),
                                    #Column('coordinates_dec', Float, nullable=False),
                                    Column('coordinates_dec', Float, nullable=True),
                                    Column('ssds_g_magnitude', Float, nullable=True),
                                    Column('ssds_r_magnitude', Float, nullable=True),
                                    Column('ssds_i_magnitude', Float, nullable=True),
                                    Column('ssds_z_magnitude', Float, nullable=True),
                                    Column('j_magnitude', Float, nullable=True),
                                    Column('h_magnitude', Float, nullable=True),
                                    Column('k_magnitude', Float, nullable=True),
                                    #Column('kepler_magnitude', Float, nullable=False),
                                    Column('kepler_magnitude', Float, nullable=True),
                                    Column('gr_color', Float, nullable=True),
                                    Column('jk_color', Float, nullable=True),
                                    Column('gk_color', Float, nullable=True),
                                    #Column('effective_temperature', Float, nullable=False),
                                    Column('effective_temperature', Float, nullable=True),
                                    Column('surface_gravity', Float, nullable=True),
                                    Column('fe_h_metallicity', Float, nullable=True),
                                    #Column('radius', Float, nullable=False),
                                    #Column('load_timestamp', DateTime, nullable=False)
                                    Column('radius', Float, nullable=True),
                                    Column('load_timestamp', DateTime, nullable=True),)

        # Tabla para almacenar los metadatos de la curva de luz
        # Del HDU[1].headers de los FITS files

        star_lightcurve_table = Table("star_lightcurve", metadata,
                                    Column('kepler_id', String(100), primary_key=True),
                                    Column('source_filename', String(100), primary_key=True),
                                    #Column('exposure', Float, nullable=False),
                                    Column('exposure', Float, nullable=True),
                                    Column('bjd_ref_integer', Integer, nullable=True),  # BJDREFI
                                    Column('bjd_ref_fraction', Float, nullable=True),  # BJDREFF
                                    #Column('time_elapsed', Float, nullable=False), # TELAPSE
                                    Column('time_elapsed', Float, nullable=True), # TELAPSE
                                    #Column('time_live', Float, nullable=False), # LIVETIME
                                    #Column('time_start', Float, nullable=False), # TSTART
                                    #Column('time_stop', Float, nullable=False), # TSTOP
                                    #Column('lc_start', Float, nullable=False), # LC_START
                                    #Column('lc_end', Float, nullable=False), # LC_END
                                    Column('time_live', Float, nullable=True), # LIVETIME
                                    Column('time_start', Float, nullable=True), # TSTART
                                    Column('time_stop', Float, nullable=True), # TSTOP
                                    Column('lc_start', Float, nullable=True), # LC_START
                                    Column('lc_end', Float, nullable=True), # LC_END
                                    Column('deadtime_correction', Float, nullable=True), # DEADC
                                    Column('bin_time', Float, nullable=True), # TIMEPIXR
                                    Column('relative_time_error', Float, nullable=True), # TIERRELA
                                    Column('absolute_time_error', Float, nullable=True), # TIERABSO
                                    #Column('integration_time', Float, nullable=False), # INT_TIME
                                    Column('integration_time', Float, nullable=True), # INT_TIME
                                    Column('readout_time', Float, nullable=True), # READTIME
                                    Column('frame_time', Float, nullable=True), # FRAMETIM
                                    #Column('number_of_frames', Integer, nullable=False), # NUM_FRM
                                    Column('number_of_frames', Integer, nullable=True), # NUM_FRM
                                    Column('time_resolution', Float, nullable=True), # TIMEDEL
                                    #Column('observation_date_start', DateTime, nullable=False), # DATE-OBS
                                    #Column('observation_date_end', DateTime, nullable=False), # DATE-END
                                    #Column('background_substracted', Boolean, nullable=False), # BACKAPP
                                    #Column('deadtime_applied', Boolean, nullable=False), # DEADAPP
                                    #Column('vignetting_correction', Boolean, nullable=False), # DEADAPP
                                    #Column('gain', Float, nullable=False), # GAIN
                                    #Column('read_noise', Float, nullable=False), # READNOIS
                                    Column('observation_date_start', DateTime, nullable=True), # DATE-OBS
                                    Column('observation_date_end', DateTime, nullable=True), # DATE-END
                                    Column('background_substracted', Boolean, nullable=True), # BACKAPP
                                    Column('deadtime_applied', Boolean, nullable=True), # DEADAPP
                                    Column('vignetting_correction', Boolean, nullable=True), # DEADAPP
                                    Column('gain', Float, nullable=True), # GAIN
                                    Column('read_noise', Float, nullable=True), # READNOIS
                                    Column('read_per_cadence', Integer, nullable=True), # NREADOUT
                                    Column('mean_black', Integer, nullable=True), # MEANBLCK
                                    Column('long_cadence_fixed_offset', Integer, nullable=True), # LCFXDOFF
                                    Column('short_cadence_fixed_offset', Integer, nullable=True), # SCFXDOFF
                                    Column('crowd_sap', Float, nullable=True), # CROWDSAP
                                    Column('target_variability', Float, nullable=True), # PDCVAR
                                    )

        star_metadata_table.drop(engine, checkfirst=True)
        star_lightcurve_table.drop(engine, checkfirst=True)

        metadata.create_all(engine)


    def insert_star_metadata(self, statements, verbose=False):
        """
        statements: es una lista de diccionarios donde cada key es una columna de la tabla
        """

        if not verbose:
             warnings.filterwarnings("ignore")

        try:

            metadata = self.get_binded_metadata()

            star_metadata_table = metadata.tables['stars_metadata']

            connection = engine.connect()

            trans = connection.begin()
            result = connection.execute(star_metadata_table.insert(), statements)
            trans.commit()

            connection.close()
        except IntegrityError:
            if verbose:
                print "ERROR: {0}".format(statements)

    def insert_star_lightcurve_metadata(self, statements, verbose=False):
        """
        statements: es una lista de diccionarios donde cada key es una columna de la tabla
        """
        if not verbose:
             warnings.filterwarnings("ignore")
             
        try:

            metadata = self.get_binded_metadata()

            star_lightcurve_table = metadata.tables['star_lightcurve']

            connection = engine.connect()

            trans = connection.begin()
            result = connection.execute(star_lightcurve_table.insert(), statements)
            trans.commit()

            connection.close()
        except IntegrityError:
            if verbose:
                print "ERROR: {0}".format(statements)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Indique la accion: crear"
        exit(1)

    accion = sys.argv[1]

    if accion == "crear":
        StarsDBManager().create_schema()
    elif accion == "bruteforce":
        path = sys.argv[2]
        tup = get_list_of_dicts(path)
        StarsDBManager().insert_star_metadata(tup[0])
        StarsDBManager().insert_star_lightcurve_metadata(tup[1])
    elif accion == 'insertar':
        path = sys.argv[2]
        archivos = listdir(path)
        for i in range(len(archivos)):
            archivos[i] = join(path, archivos[i])

        print "Total de archivos en directorio: {0}".format(len(archivos))

        raw_input('Presione ENTER para empezar...')

        i = 0

        list_of_dicts_lightcurve_metadata = []
        list_of_dicts_metadata = []
        suspects = file("suspects.sh", "w")        
        suspects.write("#!/bin/bash \n")
        for archivo in archivos:

            i += 1
            list_of_dicts_lightcurve_metadata.append(get_star_lightcurve_metadata(archivo))
            list_of_dicts_metadata.append(get_star_metadata(archivo))
            suspects.write("cp " + archivo + " ../../prueba/ \n")

            if i > 0 and i % 100 == 0:
                print "Procesando {0} de {1}".format(i, len(archivos))
                StarsDBManager().insert_star_metadata(list_of_dicts_metadata)
                StarsDBManager().insert_star_lightcurve_metadata(list_of_dicts_lightcurve_metadata)
                list_of_dicts_lightcurve_metadata = []
                list_of_dicts_metadata = []

        # Procesa el remanente

        if list_of_dicts_lightcurve_metadata:
            StarsDBManager().insert_star_metadata(list_of_dicts_metadata)
            StarsDBManager().insert_star_lightcurve_metadata(list_of_dicts_lightcurve_metadata)


        print "DONE!"
