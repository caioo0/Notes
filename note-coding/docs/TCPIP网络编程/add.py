import pandas as pd
import numpy as np

for i in np.arange(17,26):

    a = "{}".format(i)
    b = "part"+ a + '.md'
    file = open(b, 'w')