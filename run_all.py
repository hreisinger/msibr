import os, shutil

cwdStart = os.getcwd()
folders = os.listdir(cwdStart)
ppn = input("Enter ppn")
exceptions = ['run_all.py']
for j in range(0, len(folders)):
	folderName = folders[j]
	if folderName in exceptions:
		print('pass', folderName)
		pass
	else:
		dirName = '{}_inProgress'.format(folderName)
		scr_dir = '{}/{}'.format(cwdStart, folderName)
		dest_dir = '{}/{}'.format(cwdStart, dirName)
		shutil.copytree(scr_dir,dest_dir)

		os.chdir(dest_dir)
		cwd = os.getcwd()
		files = os.listdir(cwd)
		for i in range(0, len(files)):
			fileName = files[i]
			if fileName is 'run_all.py':
				pass
			else:
				cmdString = 'dos2unix {}'.format(fileName)
				os.system(cmdString)
		for i in range(0, len(files)):
			fileName = files[i]
			if fileName in exceptions:
				pass
			else:
				cmdString = 'sss2 -omp {} {}'.format(ppn, fileName)
				os.system(cmdString)
				#print(fileName)
		os.chdir(cwdStart)
		os.rename(dirName, '{}_done'.format(folderName))


