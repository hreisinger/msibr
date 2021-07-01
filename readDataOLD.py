import os
import numpy as np
import serpentTools as st

import matplotlib.pyplot as plt



st.verbosity = 'critical'


variableNames = []

cwdStart = os.getcwd()
folders = os.listdir(cwdStart)

print(cwdStart)

keffArray = np.zeros((len(folders), 101))

conversionArray = np.zeros((len(folders), 101))

slitOrder = np.array([])


for j in range(0, len(folders)):
    heightOrder = np.array([])
    folderName = folders[j]
    if folderName == 'readData.py' or folderName == 'run_all.py':
        print('pass', folderName)
        pass
    else:
        slitOrder = np.append(slitOrder, folderName)
        os.chdir('{}\{}'.format(cwdStart, folderName))
        cwd = os.getcwd()
        files = os.listdir(cwd)
        step = 0
        for i in range(0, len(files)):
            fileName = files[i]
            if fileName[-1] != 'm':
                pass
            else:
                heightOrder = np.append(heightOrder, fileName)
                res = st.readDataFile(fileName)
                keffArray[j,step] = res.resdata['absKeff'][0]
                conversionArray[j,step] = res.resdata['conversionRatio'][0]

                step += 1
        print(j / len(folders) * 100)

for i in range(0, len(slitOrder)):
    slitOrder[i] = slitOrder[i][5:-1]

for i in range(0, len(heightOrder)):
    heightOrder[i] = heightOrder[i][12:15]

os.chdir(cwdStart)

slitOrder = slitOrder.astype(np.float)
heightOrder = heightOrder.astype(np.int)

print(slitOrder)
print(heightOrder)

X, Y = np.meshgrid(heightOrder,slitOrder)
Z1 = keffArray[~np.all(keffArray == 0, axis=1)]
Z2 = conversionArray[~np.all(conversionArray == 0, axis=1)]

plt.contourf(X, Y, Z1, 20, cmap='RdGy')
plt.title('k-eff')
plt.xlabel('height')
plt.ylabel('slit')
plt.colorbar()
plt.savefig('keffArray.png')
plt.show()

plt.contourf(X, Y, Z2, 20, cmap='RdGy')
plt.title('conversion ratio')
plt.xlabel('height')
plt.ylabel('slit')
plt.colorbar()
plt.savefig('convArray.png')
plt.show()


print(keffArray)
print(conversionArray)