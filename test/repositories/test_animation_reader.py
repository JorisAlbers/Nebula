import os
from ...nebula.repositories.animation_reader import AnimationReader

def test_readFile_file_returnsLines():
    dirname = os.path.dirname(__file__)
    dir_path = os.path.join(dirname,"../../resources")
    file_name = "blue_dot.nebula.json"
    
    reader = AnimationReader(dir_path)
    lines = reader.readFile(file_name)
    print(lines)
    assert(lines is not None)
    assert(len(lines) > 0)