class MaxSizeError(Exception):

    def __init__(self):
        self.errorMsg = "Maximum size is reached, exitting..."
        super().__init__(self.errorMsg)

class BadArgsError(Exception):
    
    def __init__(self):
        self.errorMsg ="""
        
        Bad arguments were given. Usage : matchseq --seqFiles [path-to-first-seqFile] [path-to-second-seqFile] --coords(optional) [path-to-coordsFile] --filter(optional)
        
        See matchseq -h or --help for help.
        """
        super().__init__(self.errorMsg)
