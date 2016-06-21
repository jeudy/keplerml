import pandas as pd

ids = []

df = pd.read_csv('falsos_positivos.csv')

for r in df.values:
    ids.append(r[1])

for x in ids:
    str_id = str(x)
    str_id = "kplr" + "0" * (9 - len(str_id)) + str_id
    print str_id
