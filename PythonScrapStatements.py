# -*- coding: <utf-8> -*-

# ------------------------------------------------------------------------------
#
# Monetary Policy Interdependence
#   Script No. 0: Read Central Bank Statements
#
# Authors : Kim, Hyok Jung(Department of Economics, UC Davis)
#
# Date : October 21st, 2017
#
# Note : Fixed bug in PyPFD2
#
# ------------------------------------------------------------------------------

# Python standard libraries
import sys
import os

# User defined classes
from Cls_ECB import Cls_ECB
from Cls_USA import Cls_USA

# Read the current path of the script or .exe file
#   Add case of 'except' to make p2exe work well
try:
    WorkPath = os.path.dirname(os.path.abspath(__file__))
except NameError:
    WorkPath = os.path.dirname(os.path.abspath(sys.argv[0]))

# ------------------------------------------------------------------------------------
# European Central Bank
# ------------------------------------------------------------------------------------
ECBObj = Cls_ECB()

OutECB = ECBObj.MainGetData()

OutECB.to_excel(WorkPath+'/ECB/CollectedECB.xlsx', header=True, 
                index=False)

# ------------------------------------------------------------------------------------
# FRB
# ------------------------------------------------------------------------------------
USAObj = Cls_USA()
OutUSA = USAObj.MainGetData()

OutUSA.to_excel(WorkPath+'/USA/CollectedUSA.xlsx', header=True,
                index=False)