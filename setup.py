from setuptools import setup, find_packages

setup(name = "matchSeq", 
      
      version = "0.1", 
      
      packages = find_packages(),
      
      entry_points = {
          "console_scripts" : [
              "matchseq=matchseq:main",
          ]
      }
      
      )
      
