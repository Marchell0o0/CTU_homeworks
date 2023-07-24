import numpy as np


with open('C6.dsv', 'r') as file:
    tested_clasificator = np.loadtxt(file, delimiter=',').astype(int)

with open('GT.dsv', 'r') as file:
    truths = np.loadtxt(file).astype(int)


current_best = (0, 0.46)


def check_if_better():
    for j in range(50):
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for i in range(100):
            prediction = tested_clasificator[i][j]
            truth = truths[i]
            if prediction == 1:
                if prediction == truth:
                    TP += 1
                if prediction != truth:
                    FP += 1
            if prediction == 0:
                if prediction == truth:
                    TN += 1
                if prediction != truth:
                    FN += 1
        TPR_value = TP/(TP+FN)
        FPR_value = FP/(FP+TN)
        if (FPR_value == 0 and TPR_value > current_best[1]):
            return True
    return False
