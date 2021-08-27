import os

ppn = input("ppn = ")

cwdStart = os.getcwd()
folders1 = os.listdir(cwdStart)
exceptions = ['runAll.py']
for i in range(0, len(folders1)):
    f1 = folders1[i]
    if f1 in exceptions:
        pass
    else:
        dest1 = '{}/{}'.format(cwdStart, f1)
        os.chdir(dest1)
        cwd = os.getcwd()
        folders2 = os.listdir(cwd)
        for j in range(0,len(folders2)):
            f2 = folders2[j]
            dest2 = '{}/{}'.format(dest1, f2)
            os.chdir(dest2)
            cwd = os.getcwd()
            files = os.listdir(cwd)
            cmdString = 'qsub /home/hreisin1/runSerpent/runSerpent{}.sh'.format(ppn)
            os.system(cmdString)
            os.chdir('..')
        os.chdir('..')