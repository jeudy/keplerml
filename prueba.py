import datetime
from stars_db import manager

# Recordar: usar los campos correctos para los metadatos de la estrella
# Usar todos los campos aun los nullables

if __name__ == "__main__":

    # Recordar que este fue un error que funciono
    estrella = {"kepler_id": "prueba001", "source_filename": "archivo.fits", "exposure": 0.5, "time_elapsed": 10, "time_live": 100,
                "time_start": 1000, "time_stop": 500, "lc_start": 0.6, "lc_end": 0.5, "quarter": 1, "season": 1,
                "coordinates_ra": 0.5, "coordinates_dec": 3.4, "kepler_magnitude": 10.5, "effective_temperature": 10.8, "radius": 1.0,
                "load_timestamp": datetime.datetime.now()}

    curva_meta = {"kepler_id": "prueba001", "source_filename": "archivo.fits", "exposure": 0.5, "time_elapsed": 10, "time_live": 100,
                "time_start": 1000, "time_stop": 500, "lc_start": 0.6, "lc_end": 0.5, "quarter": 1, "season": 1,
                "coordinates_ra": 0.5, "coordinates_dec": 3.4, "kepler_magnitude": 10.5, "effective_temperature": 10.8, "radius": 1.0,
                "load_timestamp": datetime.datetime.now()}

    manager.insert_star_metadata([estrella])
    manager.insert_star_lightcurve_metadata([curva_meta])

    print "Done"
