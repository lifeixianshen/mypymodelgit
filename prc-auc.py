import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score,precision_recall_curve,auc


def prc_roc(csvfile,y_lab,y_pred_lab):
    cont = pd.read_csv(csvfile)
    y = np.asarray(cont[y_lab])
    y_pred = np.negative(np.asarray(cont[y_pred_lab]))
    roc = roc_auc_score(y,y_pred)
    precision, recall, _ = precision_recall_curve(y, y_pred)
    prc = auc(recall, precision)
    return print(prc,roc)


if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    print("The start time is: " + str(start))
    prc_roc('fingerprint_10000_dcsc_test.csv','values','docking score')
    end = datetime.datetime.now()
    print ("The end time is: " + str(end))
    print("The function run time is : "+str(end - start))