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

        self.clr = clr
        self.lbl = lbl

        plt.plot(self.xArray, self.yArray, '.', lw=1, color=self.clr, label=self.lbl)
        plt.plot(self.xArray, self.yLine, lw=1, color=self.clr, alpha=0.25)
        #plt.fill_between(self.xArray, self.yArray - self.yErrorArray,
        #                 self.yArray + self.yErrorArray,
        #                 color=self.clr, alpha=0.2)

        print(self.lbl, self.slope, self.slopeError)


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
    exceptions = ['runAll.py', 'readAllControlRod.py', 'keff.png', 'reactivity.png', 'conv.png','reactivity.png']

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

    centralKeff = keffArray[:, 0]
    centralKeffError = keffArray[:, 0]
    centralConversion = conversionArray[:, 0]
    centralReactivity = reactivity(centralKeff, centralKeffError)
    centralReactivityError = centralReactivity[1]
    centralReactivity = centralReactivity[0]
    
    outerKeff = keffArray[0, :]
    outerKeffError = keffArray[0, :]
    outerConversion = conversionArray[0, :]
    outerReactivity = reactivity(outerKeff,outerKeffError)
    outerReactivityError = outerReactivity[1]
    outerReactivity = outerReactivity[0]


    bothKeff = np.diag(keffArray)
    bothKeffError = np.diag(keffArray)
    bothConversion = np.diag(conversionArray)
    bothReactivity = reactivity(bothKeff, bothKeffError)
    bothReactivityError = bothReactivity[1]
    bothReactivity = bothReactivity[0]

    Order = np.arange(0,6)

    plotGraph(Order, centralReactivity-centralReactivity[0], centralReactivityError, 'Central Insertion', 'red')
    plotGraph(Order, outerReactivity-outerReactivity[0], outerReactivityError, 'Cluster Insertion', 'blue')
    #plotGraph(Order, bothReactivity, bothReactivityError, 'both Insertion', 'green')
    plt.legend()
    plt.grid()
    # plt.title('Reactivity')
    plt.xlabel('Inserted Rods/Clusters')
    plt.ylabel('Reactivity [pcm]')
    plt.savefig('reactivity.png')
    plt.show()


if __name__ == '__main__':
    main()
