import setuptools


setuptools.setup(
     name='zeratool',  
     version='2.0.1',
     scripts=['bin/zerapwn.py'] ,
     author="Christoppher Roberts",
     author_email="",
     description="Automatic Exploit Generation (AEG) and remote flag capture for exploitable CTF problems",
     url="https://github.com/ChrisTheCoolHut/Zeratool",
     packages=["zeratool"],
     install_package_data=True,
     install_requires=[
     "angr",
     "capstone",
     "r2pipe",
     "claripy",
     "IPython",
     "timeout_decorator",
     "pwntools",
     "tox",
     "tqdm",
     ],

 )
