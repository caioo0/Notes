import os
def getfiles(path1):
    for filepath,dirnames,filenames in os.walk(path1):
            for filename in filenames:
                print ('* [%s](./docs/go/%s)' %(filename,filename))

path1 = r"D:\www\learning\caioo0.github.io\note-coding\docs\go"
getfiles(path1)