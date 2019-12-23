from grocio_utils import *
import numpy as np
from pprint import pprint
import random

random.seed(1234)

# Use this to check whether the calculation is correct.

print('Calculation Started')
similarity_connectivity_calc('../SummaryTable/SummaryTable_Test.xlsx', 'SerialRecall', name_option='Test')
similarity_connectivity_calc('../SummaryTable/SummaryTable_Test.xlsx', 'SerialReconstruction', name_option='Test')
print('Calculation Ended')
