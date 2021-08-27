import os
import matplotlib.pyplot as plt
import numpy as np
import serpentTools as st

exceptions = ['runAll.py', 'readAll2D.py', 'keff.png', 'conversion.png']

cwdStart = os.getcwd()
folders1 = os.listdir(cwdStart)
folders1 = [x for x in folders1 if x not in exceptions]
v1Order = np.array([])

os.chdir('{}/{}'.format(cwdStart, folders1[0]))
cwd = os.getcwd()
folders2 = os.listdir(cwd)
folders2 = [x for x in folders2 if x not in exceptions]

f1Len = len(folders1)
f2Len = len(folders2)

os.chdir(cwdStart)

keffArray = np.zeros((f1Len, f2Len))
kErrorArray = np.zeros((f1Len, f2Len))
conversionArray = np.zeros((f1Len, f2Len))



for i in range(0, len(folders1)):
    f1 = folders1[i]
    v1Order = np.append(v1Order, f1)
    pDone = '{} {} %'.format(f1, np.round(i / f1Len * 100, 1))
    print("\u0332".join(pDone))

    dest1 = '{}/{}'.format(cwdStart, f1)
    os.chdir(dest1)

    cwd = os.getcwd()
    folders2 = os.listdir(cwd)
    folders2 = [x for x in folders2 if x not in exceptions]
    v2Order = np.array([])

    for j in range(0, len(folders2)):
        f2 = folders2[j]
        v2Order = np.append(v2Order, f2)
        print(' ➞ {}'.format(f2))

        dest2 = '{}/{}'.format(dest1, f2)
        os.chdir(dest2)

        cwd = os.getcwd()
        files = os.listdir(cwd)

        for file in files:
            if file.endswith('.m'):
                res = st.read(file)
                keffArray[i, j] = res.resdata['anaKeff'][0]
                kErrorArray[i, j] = res.resdata['anaKeff'][1]
                conversionArray[i, j] = res.resdata['conversionRatio'][0]
os.chdir(cwdStart)
print(v1Order)
print(keffArray)
v1Order = np.linspace(100, 160, 16)
v2Order = np.array([0.2941501540400644,
0.30264726306575795,
0.31114964651888677,
0.31965731423368204,
0.3281702760749692,
0.33668854193830455,
0.34521212175011406,
0.3537410254678228,
0.36227526307998836,
0.3708148446064463,
0.37935978009844007])
X, Y = np.meshgrid(v1Order,v2Order)

plt.contourf(X,Y,keffArray.T, 200, cmap='CMRmap')
plt.title('Multiplication Factor')
plt.xlabel('core height [cm]')
plt.ylabel('slit width [cm]')
plt.colorbar()
plt.savefig('keff.png')
plt.show()

plt.contourf(X,Y,conversionArray.T, 200, cmap='CMRmap')
plt.title('Conversion Ratio')
plt.xlabel('core height [cm]')
plt.ylabel('slit width [cm]')
plt.colorbar()
plt.savefig('conversion.png')
plt.show()




