# itmlwp2.py
# Introduction to Machine Learning with Python (2017)
# Follow along and testing Chp. 2

import mglearn

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, colorConverter, LinearSegmentedColormap

import numpy as np

"""
# In[54]:
X = np.array([[0, 1, 0, 1],
              [1, 0, 1, 1],
              [0, 0, 0, 1],
              [1, 0, 1, 0]])

y = np.array([0, 1, 0, 1])

# In[55]:
counts = {}
for label in np.unique(y):
    # iterate over each class
    # count (sum) entries of 1 per feature
    counts[label] = X[y == label].sum(axis=0)
print("Feature counts:\n{}".format(counts))
"""

# In[56]:
#mglearn.plots.plot_animal_tree()
#
#plt.show()

"""
# In[58]:
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer # Carry-over
from sklearn.model_selection import train_test_split # Carry-over

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target, random_state=42)

#tree = DecisionTreeClassifier(random_state=0)
#tree.fit(X_train, y_train)
#print("Accuracy on training set: {:.3f}".format(tree.score(X_train, y_train)))
#print("Accuracy on test set: {:.3f}".format(tree.score(X_test, y_test)))

# In[59]:
tree = DecisionTreeClassifier(max_depth=4, random_state=0)
tree.fit(X_train, y_train)
print("Accuracy on training set: {:.3f}".format(tree.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(tree.score(X_test, y_test)))

# In[61][61]:
from sklearn.tree import export_graphviz

export_graphviz(tree, out_file="tree.dot", class_names=["malignant", "benign"],
                feature_names=cancer.feature_names, impurity=False, filled=True)

import graphviz

with open("tree.dot") as f:
    dot_graph = f.read()
#print(graphviz.Source(dot_graph))

# In[62]:
print("Feature importances:\n{}".format(tree.feature_importances_))

# My play...
mysum = 0
for f in tree.feature_importances_:
    mysum = mysum + f
print('mysum: ', round(mysum, 2))

# In[63]:
def plot_feature_importances_cancer(model):
    n_features = cancer.data.shape[1]
    plt.barh(range(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), cancer.feature_names)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")

    plt.show()
    
#plot_feature_importances_cancer(tree)

# In[64]:
tree = mglearn.plots.plot_tree_not_monotone()
# display(tree) # display in not defined
tree.view()
"""

# In[65]:
import pandas as pd
ram_prices = pd.read_csv("data/ram_price.csv")

#plt.semilogy(ram_prices.date, ram_prices.price)
#plt.xlabel("Year")
#plt.ylabel("Price in $/Mbyte")
#plt.show()

"""
# In[66]:
from sklearn.tree import DecisionTreeRegressor

# use historical data to forecast prices after the year 2000
data_train = ram_prices[ram_prices.date < 2000]
data_test = ram_prices[ram_prices.date >= 2000]

print(type(data_train))
print(data_train)

np_df = data_train.to_numpy()

print(type(np_df))
print(np_df)

# predict prices based on date
##X_train = data_train.date[:, np.newaxis]
## orginal code throws error:
## Traceback (most recent call last):
##  File "/usr/lib/python3.10/idlelib/run.py", line 578, in runcode
##    exec(code, self.locals)
##  File "/home/gary/src/s_p3/itmlwp2-NB.py", line 115, in <module>
##    X_train = data_train.date[:, np.newaxis]
##  File "/home/gary/.local/lib/python3.10/site-packages/pandas/core/series.py", line 1153, in __getitem__
##    return self._get_with(key)
##  File "/home/gary/.local/lib/python3.10/site-packages/pandas/core/series.py", line 1163, in _get_with
##    return self._get_values_tuple(key)
##  File "/home/gary/.local/lib/python3.10/site-packages/pandas/core/series.py", line 1203, in _get_values_tuple
##    disallow_ndim_indexing(result)
##  File "/home/gary/.local/lib/python3.10/site-packages/pandas/core/indexers/utils.py", line 341, in disallow_ndim_indexing
##    raise ValueError(
## ValueError: Multi-dimensional indexing (e.g. `obj[:, None]`) is no longer supported. Convert to a numpy array before indexing instead.
##
## needs more work: X_train = np_df.date[:, np.newaxis]

# we use a log-transform to get a simpler relationship of data to target
y_train = np.log(data_train.price)

tree = DecisionTreeRegressor().fit(X_train, y_train)
linear_reg = LinearRegression().fit(X_train, y_train)

# predict on all data
X_all = ram_prices.date[:, np.newaxis]

pred_tree = tree.predict(X_all)
pred_lr = linear_reg.predict(X_all)

# undo log-transform
price_tree = np.exp(pred_tree)
price_lr = np.exp(pred_lr)

# incomplete due to ValueError above
"""


# In[89]:
# display(mglearn.plots.plot_logistic_regression_graph()) # NO display
# print(mglearn.plots.plot_logistic_regression_graph())

# In[91]:
line = np.linspace(-3, 3, 100)
plt.plot(line, np.tanh(line), label="tanh")
plt.plot(line, np.maximum(line, 0), label="relu")
plt.legend(loc="best")
plt.xlabel("x")
plt.ylabel("relu(x), tanh(x)")
plt.show()


