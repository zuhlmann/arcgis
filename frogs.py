# Every folder is a sub-package that needs to be imported
# this will require doing utils.<submodule>
import pyCatSim.utils as utils
# direct access i.e. PyCatSim.<submodule>
from .api import *


# CAT.PY
# Can switch order of a) and b) i.e. dependencies imported first
# a) INternal Classes
from ..utils import noises
# b) Dependencies
import difflib

# Documentation

# Simulates a jupyter cell ("jupyter-execute::"
# DK dislikes jupyter-execute because it's sensitive to spaces / line breaks
'''
.. jupyter-execute:
    import catPySim as cats
    nutmeg = cats.Cats(name='nutmeg',age=3, color='tortoiseshell')
    nutmeg.make_noise()    
'''

# TESTS
>>>cd tests
# will run the entire pytest
>>> pytest

#decorate with this if testing for failure == success
@pytest.mark.xfail

# test.yml
# this is to determine if need to pin dependencies in different setup files
 - name: Conda list
   run: |
     conda activate cat
     conda list
     
# Create conda env from enviromment file (Curt)
conda env create -f path/to/environemnt.yml -n <env_name>