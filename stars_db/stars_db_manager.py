import sys
import datetime
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Float, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy.orm import scoped_session, sessionmaker

DB_USER = 'root'
DB_PASS = 'jBV205760292'
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
                                    Column('quarter', Integer, nullable=False),
                                    Column('season', Integer, nullable=False),
                                    Column('data_release', Integer, nullable=True),
                                    Column('observing_mode', String(255), nullable=True),
                                    Column('coordinates_ra', Float, nullable=False),
                                    Column('coordinates_dec', Float, nullable=False),
                                    Column('ssds_g_magnitude', Float, nullable=True),
                                    Column('ssds_r_magnitude', Float, nullable=True),
                                    Column('ssds_i_magnitude', Float, nullable=True),
                                    Column('ssds_z_magnitude', Float, nullable=True),
                                    Column('j_magnitude', Float, nullable=True),
                                    Column('h_magnitude', Float, nullable=True),
                                    Column('k_magnitude', Float, nullable=True),
                                    Column('kepler_magnitude', Float, nullable=False),
                                    Column('gr_color', Float, nullable=True),
                                    Column('jk_color', Float, nullable=True),
                                    Column('gk_color', Float, nullable=True),
                                    Column('effective_temperature', Float, nullable=False),
                                    Column('surface_gravity', Float, nullable=True),
                                    Column('fe_h_metallicity', Float, nullable=True),
                                    Column('radius', Float, nullable=False),
                                    Column('load_timestamp', DateTime, nullable=False),)

        # Tabla para almacenar los metadatos de la curva de luz
        # Del HDU[1].headers de los FITS files

        star_lightcurve_table = Table("star_lightcurve", metadata,
                                    Column('kepler_id', String(100), primary_key=True),
                                    Column('source_filename', String(100), primary_key=True),
                                    Column('exposure', Float, nullable=False),
                                    Column('bjd_ref_integer', Integer, nullable=True),  # BJDREFI
                                    Column('bjd_ref_fraction', Float, nullable=True),  # BJDREFF
                                    Column('time_elapsed', Float, nullable=False), # TELAPSE
                                    Column('time_live', Float, nullable=False), # LIVETIME
                                    Column('time_start', Float, nullable=False), # TSTART
                                    Column('time_stop', Float, nullable=False), # TSTOP
                                    Column('lc_start', Float, nullable=False), # LC_START
                                    Column('lc_end', Float, nullable=False), # LC_END
                                    Column('deadtime_correction', Float, nullable=True), # DEADC
                                    Column('bin_time', Float, nullable=True), # TIMEPIXR
                                    Column('relative_time_error', Float, nullable=True), # TIERRELA
                                    Column('absolute_time_error', Float, nullable=True), # TIERABSO
                                    Column('integration_time', Float, nullable=False), # INT_TIME
                                    Column('readout_time', Float, nullable=True), # READTIME
                                    Column('frame_time', Float, nullable=True), # FRAMETIM
                                    Column('number_of_frames', Integer, nullable=False), # NUM_FRM
                                    Column('time_resolution', Float, nullable=True), # TIMEDEL
                                    Column('observation_date_start', DateTime, nullable=False), # DATE-OBS
                                    Column('observation_date_end', DateTime, nullable=False), # DATE-END
                                    Column('background_substracted', Boolean, nullable=False), # BACKAPP
                                    Column('deadtime_applied', Boolean, nullable=False), # DEADAPP
                                    Column('vignetting_correction', Boolean, nullable=False), # DEADAPP
                                    Column('gain', Float, nullable=False), # GAIN
                                    Column('read_noise', Float, nullable=False), # READNOIS
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


    def insert_star_metadata(self, statements):
        """
        statements: es una lista de diccionarios donde cada key es una columna de la tabla
        """

        metadata = self.get_binded_metadata()

        star_metadata_table = metadata.tables['stars_metadata']

        connection = engine.connect()

        trans = connection.begin()
        result = connection.execute(star_metadata_table.insert(), statements)
        trans.commit()

        connection.close()


    def insert_star_lightcurve_metadata(self, statements):
        """
        statements: es una lista de diccionarios donde cada key es una columna de la tabla
        """

        metadata = self.get_binded_metadata()

        star_lightcurve_table = metadata.tables['star_lightcurve']

        connection = engine.connect()

        trans = connection.begin()
        result = connection.execute(star_lightcurve_table.insert(), statements)
        trans.commit()

        connection.close()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Indique la accion: crear"
        exit(1)

    accion = sys.argv[1]

    if accion == "crear":
        StarsDBManager().create_schema()
