import numpy as np

def accumarray(data,length):
    values,counts=np.unique(data,return_counts=True)
    while(len(counts)<length):
        counts=np.append(counts,[0])
    return counts
# ind =np.array([1, 1, 4, 2, 4, 3])
# print(accumarray(ind,6))