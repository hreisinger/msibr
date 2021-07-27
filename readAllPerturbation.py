import os
import matplotlib.pyplot as plt
import numpy as np
import serpentTools as st

class plotGraph:
    def __init__(self, xArray, yArray, yErrorArray, lbl=None, clr=None):
        self.xArray = xArray.flatten()
        self.yArray = yArray.flatten()
        self.yErrorArray = yErrorArray.flatten()

        self.fit = OLSfit(xArray, yArray, yErrorArray)

        self.slope = self.fit[0]
        self.slopeError = self.fit[1]
        self.intercept = self.fit[2]
        self.interceptError = self.fit[3]

        self.yLine = self.slope * self.xArray + self.intercept

        plt.plot(self.xArray, self.yArray, '.', lw=1, color=clr)
        plt.plot(self.xArray, self.yLine, lw=1, color=clr, label=lbl)



        pass

def reactivity(keff, keffError):
    reactivityArray = (keff - 1) / keff * 1e5
    reactivityArray_error = keffError / keff * 1e5
    return [reactivityArray, reactivityArray_error]


def OLSfit(x, y, dy=None):
    """Find the best fitting parameters of a linear fit to the data through the
    method of ordinary least squares estimation. (i.e. find m and b for
    y = m*x + b)

    Args:
        x: Numpy array of independent variable data
        y: Numpy array of dependent variable data. Must have same size as x.
        dy: Numpy array of dependent variable standard deviations. Must be same
            size as y.

    Returns: A list with four floating point values. [m, dm, b, db]
    """
    if dy is None:
        # if no error bars, weight every point the same
        dy = np.ones(x.size)
    denom = np.sum(1 / dy ** 2) * np.sum((x / dy) ** 2) - (np.sum(x / dy ** 2)) ** 2
    m = (np.sum(1 / dy ** 2) * np.sum(x * y / dy ** 2) -
         np.sum(x / dy ** 2) * np.sum(y / dy ** 2)) / denom
    b = (np.sum(x ** 2 / dy ** 2) * np.sum(y / dy ** 2) -
         np.sum(x / dy ** 2) * np.sum(x * y / dy ** 2)) / denom
    dm = np.sqrt(np.sum(1 / dy ** 2) / denom)
    db = np.sqrt(np.sum(x / dy ** 2) / denom)
    return [m, dm, b, db]


def main():
    exceptions = ['runAll.py', 'readAllShutDown.py', 'keff.png', 'reactivity.png','conv.png']

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
    print(v2Order)
    print(keffArray)
    print(kErrorArray)

    v1Order = np.linspace(-100, 100, 5)

    plotGraph(v1Order, keffArray[0], kErrorArray[0], 'Blanket',     'blue')
    plotGraph(v1Order, keffArray[1], kErrorArray[1], 'Fuel',        'red')
    plotGraph(v1Order, keffArray[2], kErrorArray[2], 'Graphite',    'green')
    plt.legend()
    plt.grid()
    # plt.title('k-eff')
    plt.xlabel('Temperature [°C]')
    plt.ylabel(r'k$_{eff}$')
    plt.savefig('keff.png')
    plt.show()

    # blanket_conversion = plotGraph(v1Order,conversionArray[0],conversionArray[0])
    '''
    ctrlRD_keff = [keffArray[0], kErrorArray[0]]
    noCtrlRD_keff = [keffArray[1], kErrorArray[1]]

    ctrlRD_conversion = conversionArray[0]
    noCtrlRD_conversion = conversionArray[1]

    ctrlRD_reactivity = reactivity(*ctrlRD_keff)
    noCtrlRD_reactivity = reactivity(*noCtrlRD_keff)

    ctrlRD_fit = OLSfit(v1Order, ctrlRD_reactivity[0].flatten(), ctrlRD_reactivity[1].flatten())
    ctrlRD_slope = ctrlRD_fit[0]
    ctrlRD_slopeError = ctrlRD_fit[1]
    ctrlRD_intercept = ctrlRD_fit[2]

    noCtrlRD_fit = OLSfit(v1Order, noCtrlRD_reactivity[0].flatten(), noCtrlRD_reactivity[1].flatten())
    noCtrlRD_slope = noCtrlRD_fit[0]
    noCtrlRD_slopeError = noCtrlRD_fit[1]
    noCtrlRD_intercept = noCtrlRD_fit[2]


    Xline = v1Order
    ctrlYline = ctrlRD_slope * Xline + ctrlRD_intercept
    noCtrlYline = noCtrlRD_slope * Xline + noCtrlRD_intercept



    plt.plot(v1Order, ctrlRD_keff[0].flatten(), label='Control Rods')
    plt.plot(v1Order, noCtrlRD_keff[0].flatten(), label='No Control Rods')
    plt.legend()
    plt.grid()
    # plt.title('k-eff')
    plt.xlabel('Temperature [°C]')
    plt.ylabel(r'k$_{eff}$')
    plt.savefig('keff.png')
    plt.show()

    plt.plot(v1Order, ctrlRD_conversion.flatten(), label='Control Rods')
    plt.plot(v1Order, noCtrlRD_conversion.flatten(), label='No Control Rods')
    plt.legend()
    plt.grid()
    # plt.title('conversion ratio')
    plt.xlabel('Temperature [°C]')
    plt.ylabel('Conversion ratio')
    plt.savefig('conv.png')
    plt.show()

    plt.plot(v1Order, ctrlRD_reactivity[0], '.', lw=1)
    plt.plot(v1Order, noCtrlRD_reactivity[0], '.', lw=1)

    plt.fill_between(v1Order, ctrlRD_reactivity[0] - ctrlRD_reactivity[1],
                     ctrlRD_reactivity[0] + ctrlRD_reactivity[1],
                     color='gray', alpha=0.2)
    plt.fill_between(v1Order, noCtrlRD_reactivity[0] - noCtrlRD_reactivity[1],
                     noCtrlRD_reactivity[0] + noCtrlRD_reactivity[1],
                     color='gray', alpha=0.2)

    plt.plot(Xline, ctrlYline, lw=1, color='blue', label='Control Rods In')
    plt.plot(Xline, noCtrlYline, lw=1, color='red', label='Control Rods Out')

    CTRL_fitSTR = 'Control Rod SLope: {} ± {}'.format(np.round(ctrlRD_slope, 7), np.round(ctrlRD_slopeError, 7))
    noCTRL_fitSTR = 'No Control Rod SLope: {} ± {}'.format(np.round(noCtrlRD_slope, 7),
                                                           np.round(noCtrlRD_slopeError, 7))
    plt.annotate(CTRL_fitSTR, (560, -7000), bbox=dict(boxstyle='round', fc='0.8'),  # New param
                 ha='center',
                 va='center')
    plt.annotate(noCTRL_fitSTR, (570, 0), bbox=dict(boxstyle='round', fc='0.8'),  # New param
                 ha='center',
                 va='center')
    plt.legend()
    plt.grid()
    # plt.title('Reactivity')
    plt.xlabel('Temperature [°C]')
    plt.ylabel('Reactivity [pcm]')
    plt.savefig('reactivity.png')
    plt.show()'''


if __name__ == '__main__':
    main()
