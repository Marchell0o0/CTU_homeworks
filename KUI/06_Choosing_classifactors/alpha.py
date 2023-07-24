import numpy as np
import matplotlib.pyplot as plt

predictions = [None]*5

# Load the classifier predictions
with open('C1.dsv', 'r') as file:
    predictions[0] = np.loadtxt(file, delimiter=',').astype(int)
with open('C2.dsv', 'r') as file:
    predictions[1] = np.loadtxt(file, delimiter=',').astype(int)
with open('C3.dsv', 'r') as file:
    predictions[2] = np.loadtxt(file, delimiter=',').astype(int)
with open('C4.dsv', 'r') as file:
    predictions[3] = np.loadtxt(file, delimiter=',').astype(int)
with open('C5.dsv', 'r') as file:
    predictions[4] = np.loadtxt(file, delimiter=',').astype(int)

# Load the correct answers
with open('GT.dsv', 'r') as file:
    truths = np.loadtxt(file).astype(int)

colors = ['b', 'g', 'r', 'c', 'm']

for k in range(5):
    there_is_zero_fpr = False

    TPR = []
    FPR = []
    for j in range(50):
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for i in range(100):
            prediction = predictions[k][i][j]
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
        TPR.append(TPR_value)
        FPR.append(FPR_value)

    plt.plot(FPR, TPR, color=colors[k], label='ROC curve '+str(k+1))
    # highlight the best parameter in red
    FPR = np.array(FPR)
    TPR = np.array(TPR)
    distances_squared = (FPR - 0)**2 + (TPR - 1)**2
    best_param_index = np.argmin(distances_squared)
    print(
        f"Set of data {k + 1}, best parameter is {FPR[best_param_index], TPR[best_param_index]} index {best_param_index}")
    # find parameters with FPR of 0
    zero_FPR_indices = np.where(FPR == 0)[0]

    if len(zero_FPR_indices) > 0:  # check that we have at least one index with FPR=0
        there_is_zero_fpr = True
        max_TPR_index = zero_FPR_indices[np.argmax(TPR[zero_FPR_indices])]
        print(
            f"Zero FPR parameter with highest TPR is {FPR[max_TPR_index], TPR[max_TPR_index]} index {max_TPR_index}")
        plt.scatter(FPR[max_TPR_index], TPR[max_TPR_index], color='blue')

    if not there_is_zero_fpr:
        print(f"No parameters with zero FPR found")

    plt.scatter(FPR[best_param_index], TPR[best_param_index], color='red')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend()
plt.grid(True)
plt.savefig('roc_curve.png')
