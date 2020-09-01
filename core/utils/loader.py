import os

def get_path(folder, file):
    cwd = os.getcwd()
    get_absolute_path = os.path.join(cwd + "/" + folder + "/" + file)
    return get_absolute_path
    

