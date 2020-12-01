import numpy as np
import pandas as pd
from main import columns_counts
from main import days_counts
from main import CLASSES_COUNT
np.set_printoptions(suppress=True)

DAYS_COUNTS_NUMBER = len(days_counts)
columns_counts = [1,4,16,64,256, 512, 1024, 2048]

def parse_results(COLUMNS_COUNT, DAYS_NUMBER):
    CNAME = str(COLUMNS_COUNT)
    DNAME = str(DAYS_NUMBER)
    while len(CNAME) < 4:
        CNAME = '0' + CNAME
    while len(DNAME) < 4:
        DNAME = '0' + DNAME
    # Dodać wywalanie z results niepotrzebnych lini
    # Tu coś dodać trzeba do nazwy
    filename = 'results/res_script-' + CNAME + '_columns-' + DNAME + '_days' + '.sql'
    df = pd.read_csv(filename, header=None).to_numpy()
    results = []
    print(df.shape)
    for i in range ((DAYS_COUNTS_NUMBER ) * 6):
        results.append(df[i * CLASSES_COUNT : (i+1) * CLASSES_COUNT].mean())
    return results



print(len(parse_results(columns_counts[0], days_counts[0])))

#%%
results = []
for ccount in columns_counts:
    for dcount in days_counts:
        # print('soc')
        results.append(parse_results(ccount, dcount))
res = np.array(results)
print(np.around(res, decimals=3))
print(res.shape)
# for i in range(len(results)):
#     print(results[i])
# print(results)
# print(np.around(results, decimals=3))
