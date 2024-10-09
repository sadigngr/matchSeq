def _read(_PATH1,_PATH2):

    with open(_PATH1,"r") as f:
        f.readline()
        buffer = f.read().replace("\n","")

    with open(_PATH2,"r") as r :
        r.readline()
        _buffer = r.read().replace("\n","")

    return buffer,_buffer
