class MaxSizeError(Exception):

    def __init__(self):
        self.errorMsg = "Maximum size is reached, exitting..."
        super().__init__(self.errorMsg)

class BadArgsError(Exception):
    
    def __init__(self):
        self.errorMsg ="Bad arguments were given. Usage : python3 matchTable.py -seqFiles [path-to-first-seqFile] [path-to-second-seqFile] -coords(optional) [path-to-coordsFile]"
        super().__init__(self.errorMsg)
