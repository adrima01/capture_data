from scipy.stats import randint

import sklearn
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay, \
    classification_report, roc_auc_score
from sklearn.tree import export_graphviz, plot_tree, DecisionTreeClassifier
from IPython.display import Image
from IPython.display import display
import graphviz


companies = ["amazon", "ameli", "amendes", "atandt", "credit_agricole", "luxtrust", "microsoft", "netflix", "orange", "paypal"]
for company in companies:
    print(company)
    data_path = "datasets/" + company + "_dataset.csv"
    data_all = pd.read_csv(data_path)
    # get rid of NaN values, if present
    data_all = data_all.dropna()
    data_all = data_all.drop_duplicates()
    print(data_all.shape)

    uuids = data_all['uuid']
    columns_to_drop = ['uuid', 'dir_path', 'malicious', '3rd_party_hits', 'latitude', 'longitude','domain_length','form_presence',
                        'number_links',
                        'number_empty_links',
                        'number_links_domain']
    data_all = data_all.drop(columns=columns_to_drop)
    data_all['hash_screenshot'] = pd.to_numeric(data_all['hash_screenshot'], errors='coerce')
    data_all['hash_favicon'] = pd.to_numeric(data_all['hash_favicon'], errors='coerce')
    data_all['hash_screenshot'] = np.log1p(data_all['hash_screenshot'])
    data_all['hash_favicon'] = np.log1p(data_all['hash_favicon'])

    print(data_all.columns.tolist())
    data_all[['hash_screenshot', 'hash_favicon']].isna().sum()
    # Überprüfen auf inf
    np.isinf(data_all[['hash_screenshot', 'hash_favicon']]).sum()

    # Überprüfen auf sehr große Werte
    (data_all[['hash_screenshot', 'hash_favicon']] > np.finfo(np.float32).max).sum()


    X = data_all.drop('company_site', axis=1)
    y = data_all['company_site']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    uuids_train = uuids.iloc[X_train.index]
    uuids_test = uuids.iloc[X_test.index]

    #print(X_train.shape)
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    X_test_classified_as_1 = X_test[y_pred == 1]
    results = pd.DataFrame({
        'uuid': uuids_test,
        'actual': y_test,
        'prediction': y_pred
    })
    # Ergebnisse in eine CSV-Datei speichern
    results.to_csv(company + '_results.csv', index=False)

    # Option 1: Ausgabe der Datenpunkte
    print("Daten, die als 1 klassifiziert wurden:")
    print(X_test_classified_as_1)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    param_dist = {'n_estimators': randint(50,500),
                  'max_depth': randint(1,20)}

   #Create a random forest classifier
    """rc = RandomForestClassifier()

    # Use random search to find the best hyperparameters
    rand_search = RandomizedSearchCV(rc,
                                     param_distributions = param_dist,
                                     n_iter=5,
                                     cv=5)

    # Fit the random search object to the data
    rand_search.fit(X_train, y_train)
    best_rf = rand_search.best_estimator_

    # Print the best hyperparameters
    print('Best hyperparameters:',  rand_search.best_params_)
    # Generate predictions with the best model
    y_pred = best_rf.predict(X_test)

    # Create the confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    ConfusionMatrixDisplay(confusion_matrix=cm).plot();
    plt.figure(figsize=(20, 10))
    plot_tree(rf.estimators_[0], feature_names=X_train.columns, filled=True, max_depth=4, impurity=False)
    plt.show()"""
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print(indices)
    plt.figure(figsize=(13, 16))

    plt.bar(range(X_train.shape[1]), importances[indices], align='center')
    plt.xticks(range(X_train.shape[1]), X_train.columns[indices], rotation=90)
    plt.xlim([-1, X_train.shape[1]])
    plt.xlabel('Feature')
    plt.ylabel('Importance')
    plt.title(company)
    plt.show()

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

    cv_scores = cross_val_score(rf, X, y, cv=5)
    print("Cross-Validation Scores:", cv_scores)
    print("Average CV Score:", np.mean(cv_scores))
    print(classification_report(y_test, y_pred))

    y_prob = rf.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    print("AUC:", auc)


    # Korrelation berechnen
    korrelation_matrix = data_all.corr(method='pearson')
    print(korrelation_matrix)