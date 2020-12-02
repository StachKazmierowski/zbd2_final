import numpy as np
import pandas as pd
from main import columns_counts
from main import days_counts
from main import CLASSES_COUNT
np.set_printoptions(suppress=True)

DAYS_COUNTS_NUMBER = len(days_counts)
columns_counts = [1,4,16,64,256, 512, 1024]

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
    # print(df.shape)
    for i in range ((DAYS_COUNTS_NUMBER ) * 6):
        results.append(df[i * CLASSES_COUNT : (i+1) * CLASSES_COUNT].mean())
    return results



print((parse_results(columns_counts[6], days_counts[6])[5]))

#%%
results_name = []
results = []
for ccount in columns_counts:
    # print(ccount)
    for dcount in days_counts:
        results.append(parse_results(ccount, dcount))
        # print(dcount)
print(results[0][5])
print(results[48][5])
#%%
    # res = np.array(results)
res = np.array(results)
print(res[0][41])
print(res[48][41])
# print(res)
# res = np.around(res, decimals=3)
# print(res.shape)
print(res[:,0:])
#%%
res_names = ["res_csv", "res_csv_long","res_local","res_local_long","res_cstore","res_cstore_long"]
heads = []
rowes = []
for dcount in days_counts:
    heads.append(str(dcount))
for ccount in columns_counts:
    for dcount in days_counts:
        rowes.append(str(ccount) + "-columns_" + str(dcount) + "-days")
res_csv = res[:,0:7]
res_csv_long = res[:,7:14]
res_local  = res[:,14:21]
res_local_long = res[:,21:28]
res_cstore = res[:,28:35]
res_cstore_long = res[:,35:42]
print(res)
res_np = [res_csv,res_csv_long,res_local,res_local_long,res_cstore,res_cstore_long]
# for i in range(7):
#     res_csv[:, i] = res[:,6*i]
#     res_csv_long[:,i] = res[:,6*i + 1]
#     res_local[:, i] = res[:,6*i + 2]
#     res_local_long[:, i] = res[:,6*i + 3]
#     res_cstore[:, i] = res[:,6*i + 4]
#     res_cstore_long[:, i] = res[:,6*i + 5]
#     print(res[:,6*i + 5])
#%%
print(res_cstore_long)

#%%
print((res_csv))
for i in range(6):
    df = pd.DataFrame(res_np[i], columns=heads, index=rowes)
    print(res_names[i])
    print(df)
    df.to_csv("./results/" + res_names[i])


