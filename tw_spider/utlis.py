import os

def mkdirs(dirs):
    '''
    Make directory if the directory doesn't exist
    
    Args:
        dirs[string]: the name of the directory
    '''
    if not os.path.exists(dirs):
        os.makedirs(dirs)