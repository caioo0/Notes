import pandas as pd
import numpy as np

for i in np.arange(6,17):

    a = "{}".format(i)
    b = "part"+ a + '.md'
    file = open(b, 'w')