import os
def listfiles(rootDir): 
    list_dirs = os.walk(rootDir) 
    filepath_list = []
    for root, dirs, files in list_dirs:
        for f in files:
            filepath_list.append(os.path.join(root,f))
    return filepath_list