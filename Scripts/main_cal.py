from grocio_utils import *
import numpy as np
from pprint import pprint
import random

random.seed(1234)

print('Calculation Started')
similarity_connectivity_calc('../SummaryTable/SummaryTable.xlsx', 'SerialRecall')
similarity_connectivity_calc('../SummaryTable/SummaryTable.xlsx', 'SerialReconstruction')
similarity_connectivity_calc('../SummaryTable/SummaryTable.xlsx', 'ItemCorrect')
similarity_connectivity_calc('../SummaryTable/SummaryTable.xlsx', 'OrderErrors')
print('Calculation Ended')
