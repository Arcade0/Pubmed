import os
import numpy as np
import pandas as pd
import json
from copy import deepcopy
import re
import random
from random import choice
import string
random.seed(10)

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from itertools import cycle
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
# -*- coding:utf-8 -*

def evaluate(standard, prediction):

    accuracy = accuracy_score(standard["golden"],
                            prediction["prediction"],
                            normalize=True,
                            sample_weight=None)
    precision = precision_score(standard["golden"],
                                prediction["prediction"],
                                labels=None,
                                pos_label='yes',
                                average='binary',
                                sample_weight=None,
                                zero_division='warn')
    recall = recall_score(standard["golden"],
                        prediction["prediction"],
                        labels=None,
                        pos_label='yes',
                        average='binary',
                        sample_weight=None,
                        zero_division='warn')
    f1 = f1_score(standard["golden"],
                prediction["prediction"],
                labels=None,
                pos_label='yes',
                average='binary',
                sample_weight=None,
                zero_division='warn')

    print("结果:", accuracy, precision, recall, f1)
    return accuracy, precision, recall, f1

def multiclass_score(standard, prediction):
    
    accuracy = accuracy_score(standard["golden"],
                            prediction["prediction"])
    precision = precision_score(standard["golden"],
                                prediction["prediction"],
                                average='weighted',
                                zero_division=1)
    recall = recall_score(standard["golden"],
                        prediction["prediction"],
                        average='weighted',
                        zero_division=1)
    f1 = f1_score(standard["golden"],
                prediction["prediction"],
                average='weighted',
                zero_division=1)

    print("结果:", accuracy, precision, recall, f1)
    return accuracy, precision, recall, f1
    
    # plot roc
def roc(standard, prediction, fig_path):
    
    standard.loc[standard["golden"] == "yes", "golden"] = 1
    standard.loc[standard["golden"] == "no", "golden"] = 0
    standard["minus"] = 1 - standard["golden"]
    standard_v = np.array(standard.values, dtype="float")

    prediction = prediction[["rate", "cut"]]
    prediction.columns = ["golden", "minus"]
    prediction_v = np.array(prediction.values, dtype="float")

    # Binarize the output
    y_test = standard_v
    y_score = prediction_v
    n_classes = y_score.shape[1]

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    
    fig = plt.figure()
    plt.plot(fpr[0], tpr[0], color='darkorange',
            lw=2, label='ROC curve (area = %0.2f)' % roc_auc[0])
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('REPEAT%s ROC curve' % re)
    plt.legend(loc="lower right")
    plt.show()
    fig.savefig("%s/roc_curve.png" % (fig_path))
