import os
def mk_dir(file_path):

    folder = os.path.exists(file_path)
    if not folder:
        os.makedirs(file_path)