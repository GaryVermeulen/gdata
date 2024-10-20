# itmlwp2.py
# Introduction to Machine Learning with Python (2017)
# Follow along and testing Chp. 2

import mglearn

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, colorConverter, LinearSegmentedColormap

import numpy as np

# In[2]:
# generate dataset
#X, y = mglearn.datasets.make_forge()
# plot dataset
#mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
#plt.legend(["Class 0", "Class 1"], loc=4)
#plt.xlabel("First feature")
#plt.ylabel("Second feature")
#print("X.shape: {}".format(X.shape))
#
#plt.show()


# In[3]:
#X, y = mglearn.datasets.make_wave(n_samples=40)
#plt.plot(X, y, 'o')
#plt.ylim(-3, 3)
#plt.xlabel("Feature")
#plt.ylabel("Target")
#
#plt.show()


# In[4]:
#from sklearn.datasets import load_breast_cancer
#cancer = load_breast_cancer()
#print("cancer.keys(): \n{}".format(cancer.keys()))
# In[5]:
#print("Shape of cancer data: {}".format(cancer.data.shape))
# In[6]:
#print("Sample counts per class:\n{}".format(
#    {n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
# In[7]:
#print("Feature names:\n{}".format(cancer.feature_names))

# In[8]:
## scikit no longer supports the boston dataset
##from sklearn.datasets import load_boston
##boston = load_boston()
##print("Data shape: {}".format(boston.data.shape))
## use california instead...
#from sklearn.datasets import fetch_california_housing
#housing = fetch_california_housing()
#from sklearn.datasets import fetch_openml
#print("Data shape: {}".format(housing.data.shape))
#print(housing.DESCR)

# In[10]:
#mglearn.plots.plot_knn_classification(n_neighbors=1)
#plt.show()
# In[11]:
#mglearn.plots.plot_knn_classification(n_neighbors=3)
#plt.show()

"""
# In[12]:
from sklearn.model_selection import train_test_split
X, y = mglearn.datasets.make_forge()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
# In[13]:
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=3)
# In[14]:
clf.fit(X_train, y_train)
# In[15]:
print("Test set predictions: {}".format(clf.predict(X_test)))
# In[16]:
print("Test set accuracy: {:.2f}".format(clf.score(X_test, y_test)))

# In[17]:
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
for n_neighbors, ax in zip([1, 3, 9], axes):
    # the fit method returns the object self, so we can instantiate
    # and fit in one line
    clf = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, y)
    mglearn.plots.plot_2d_separator(clf, X, fill=True, eps=0.5, ax=ax, alpha=.4)
    mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
    ax.set_title("{} neighbor(s)".format(n_neighbors))
    ax.set_xlabel("feature 0")
    ax.set_ylabel("feature 1")
axes[0].legend(loc=3)

plt.show()
"""

"""
# In[18]:
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split # Implied/loaded earlier
from sklearn.neighbors import KNeighborsClassifier # Implied/loaded earlier

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=66)

training_accuracy = []
test_accuracy = []
# try n_neighbors from 1 to 10
neighbors_settings = range(1, 11)

for n_neighbors in neighbors_settings:
    # build the model
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train, y_train)
    # record training set accuracy
    training_accuracy.append(clf.score(X_train, y_train))
    # record generalization accuracy
    test_accuracy.append(clf.score(X_test, y_test))

plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()

# In[19]:
#mglearn.plots.plot_knn_regression(n_neighbors=1)
#plt.show()

# In[20]:
mglearn.plots.plot_knn_regression(n_neighbors=3)
plt.show()
"""

"""
# In[21]:
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

X, y = mglearn.datasets.make_wave(n_samples=40)

# split the wave dataset into a training and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# instantiate the model and set the number of neighbors to consider to 3
reg = KNeighborsRegressor(n_neighbors=3)
# fit the model using the training data and training targets
reg.fit(X_train, y_train)

# In[22]:
print("Test set predictions:\n{}".format(reg.predict(X_test)))

# In[23]:
print("Test set R^2: {:.2f}".format(reg.score(X_test, y_test)))



#from sklearn.neighbors import KNeighborsRegressor
# In[24]:
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
# create 1,000 data points, evenly spaced between -3 and 3
line = np.linspace(-3, 3, 1000).reshape(-1, 1)
for n_neighbors, ax in zip([1, 3, 9], axes):
    # make predictions using 1, 3, or 9 neighbors
    reg = KNeighborsRegressor(n_neighbors=n_neighbors)
    reg.fit(X_train, y_train)
    ax.plot(line, reg.predict(line))
    ax.plot(X_train, y_train, '^', c=mglearn.cm2(0), markersize=8)
    ax.plot(X_test, y_test, 'v', c=mglearn.cm2(1), markersize=8)

    ax.set_title(
        "{} neighbor(s)\n train score: {:.2f} test score: {:.2f}".format(
            n_neighbors, reg.score(X_train, y_train),
            reg.score(X_test, y_test)))
    ax.set_xlabel("Feature")
    ax.set_ylabel("Target")

axes[0].legend(["Model predictions", "Training data/target",
    "Test data/target"], loc="best") 

plt.show()
"""

# In[25]:
#mglearn.plots.plot_linear_regression_wave()

# In[26]:
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#X, y = mglearn.datasets.make_wave(n_samples=60)
#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

#lr = LinearRegression().fit(X_train, y_train)

# In[27]:
#print("lr.coef_: {}".format(lr.coef_))
#print("lr.intercept_: {}".format(lr.intercept_))
#
# In[28]:
#print("Training set score: {:.2f}".format(lr.score(X_train, y_train)))
#print("Test set score: {:.2f}".format(lr.score(X_test, y_test)))

# In[29]:
#X, y = mglearn.datasets.load_extended_boston()

#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
#lr = LinearRegression().fit(X_train, y_train)
#
# In[30]:
#print("Training set score: {:.2f}".format(lr.score(X_train, y_train)))
#print("Test set score: {:.2f}".format(lr.score(X_test, y_test)))

# In[31]:
from sklearn.linear_model import Ridge

#ridge = Ridge().fit(X_train, y_train)
#print("Training set score: {:.2f}".format(ridge.score(X_train, y_train)))
#print("Test set score: {:.2f}".format(ridge.score(X_test, y_test)))

# In[32]:
#ridge10 = Ridge(alpha=10).fit(X_train, y_train)
#print("Training set score: {:.2f}".format(ridge10.score(X_train, y_train)))
#print("Test set score: {:.2f}".format(ridge10.score(X_test, y_test)))

# In[33]:
#ridge01 = Ridge(alpha=0.1).fit(X_train, y_train)
#print("Training set score: {:.2f}".format(ridge01.score(X_train, y_train)))
#print("Test set score: {:.2f}".format(ridge01.score(X_test, y_test)))
"""
# In[34]:
plt.plot(ridge.coef_, 's', label="Ridge alpha=1")
plt.plot(ridge10.coef_, '^', label="Ridge alpha=10")
plt.plot(ridge01.coef_, 'v', label="Ridge alpha=0.1")

plt.plot(lr.coef_, 'o', label="LinearRegression")
plt.xlabel("Coefficient index")
plt.ylabel("Coefficient magnitude")
plt.hlines(0, 0, len(lr.coef_))
plt.ylim(-25, 25)
plt.legend()

plt.show()
"""
# In[36]:
#from sklearn.linear_model import Lasso

#lasso = Lasso().fit(X_train, y_train)
#print("Training set score: {:.2f}".format(lasso.score(X_train, y_train)))
#rint("Test set score: {:.2f}".format(lasso.score(X_test, y_test)))
#print("Number of features used: {}".format(np.sum(lasso.coef_ != 0)))

# In[37]:
# we increase the default setting of "max_iter",
# otherwise the model would warn us that we should increase max_iter.
#lasso001 = Lasso(alpha=0.01, max_iter=100000).fit(X_train, y_train)
#print("Training set score: {:.2f}".format(lasso001.score(X_train, y_train)))
#print("Test set score: {:.2f}".format(lasso001.score(X_test, y_test)))
#print("Number of features used: {}".format(np.sum(lasso001.coef_ != 0)))

# In[38]:
#lasso00001 = Lasso(alpha=0.0001, max_iter=100000).fit(X_train, y_train)
#print("Training set score: {:.2f}".format(lasso00001.score(X_train, y_train)))
#print("Test set score: {:.2f}".format(lasso00001.score(X_test, y_test)))
#print("Number of features used: {}".format(np.sum(lasso00001.coef_ != 0)))

# In[39]:
#plt.plot(lasso.coef_, 's', label="Lasso alpha=1")
#plt.plot(lasso001.coef_, '^', label="Lasso alpha=0.01")
#plt.plot(lasso00001.coef_, 'v', label="Lasso alpha=0.0001")
#
#plt.plot(ridge01.coef_, 'o', label="Ridge alpha=0.1")
#plt.legend(ncol=2, loc=(0, 1.05))
#plt.ylim(-25, 25)
#plt.xlabel("Coefficient index")
#lt.ylabel("Coefficient magnitude")
#
#plt.show()


# In[40]:
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

#X, y = mglearn.datasets.make_forge()
#fig, axes = plt.subplots(1, 2, figsize=(10, 3))
#
#for model, ax in zip([LinearSVC(), LogisticRegression()], axes):
#    clf = model.fit(X, y)
#    mglearn.plots.plot_2d_separator(clf, X, fill=False, eps=0.5,
#    ax=ax, alpha=.7)
#    mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
#    ax.set_title("{}".format(clf.__class__.__name__))
#    ax.set_xlabel("Feature 0")
#    ax.set_ylabel("Feature 1")
#    
#axes[0].legend()
#
#plt.show()

# In[41]:
#mglearn.plots.plot_linear_svc_regularization()
#
#plt.show()

# In[42]:
# Throws a warning:
## Warning (from warnings module):
##   File "/home/gary/.local/lib/python3.10/site-packages/sklearn/linear_model/_logistic.py", line 469
##     n_iter_i = _check_optimize_result(
## ConvergenceWarning: lbfgs failed to converge (status=1):
## STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
##
## Increase the number of iterations (max_iter) or scale the data as shown in:
##     https://scikit-learn.org/stable/modules/preprocessing.html
## Please also refer to the documentation for alternative solver options:
##     https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
##
#from sklearn.datasets import load_breast_cancer
#
#cancer = load_breast_cancer()
#X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target, random_state=42)
#logreg = LogisticRegression().fit(X_train, y_train)
#print("Training set score: {:.3f}".format(logreg.score(X_train, y_train)))
#print("Test set score: {:.3f}".format(logreg.score(X_test, y_test)))

# In[43]:
#logreg100 = LogisticRegression(C=100).fit(X_train, y_train)
#print("Training set score: {:.3f}".format(logreg100.score(X_train, y_train)))
#print("Test set score: {:.3f}".format(logreg100.score(X_test, y_test)))

# In[44]:
#logreg001 = LogisticRegression(C=0.01).fit(X_train, y_train)
#print("Training set score: {:.3f}".format(logreg001.score(X_train, y_train)))
#print("Test set score: {:.3f}".format(logreg001.score(X_test, y_test)))

# In[45]:
#plt.plot(logreg.coef_.T, 'o', label="C=1")
#plt.plot(logreg100.coef_.T, '^', label="C=100")
#plt.plot(logreg001.coef_.T, 'v', label="C=0.001")
#plt.xticks(range(cancer.data.shape[1]), cancer.feature_names, rotation=90)
#plt.hlines(0, 0, cancer.data.shape[1])
#plt.ylim(-5, 5)
#plt.xlabel("Coefficient index")
#plt.ylabel("Coefficient magnitude")
#plt.legend()
#
#plt.show()

# In[46]:
## THROWS ERROR:
"""
Traceback (most recent call last):
  File "/usr/lib/python3.10/idlelib/run.py", line 578, in runcode
    exec(code, self.locals)
  File "/home/gary/src/s_p3/itmlwp2.py", line 354, in <module>
    lr_l1 = LogisticRegression(C=C, penalty="l1").fit(X_train, y_train)
  File "/home/gary/.local/lib/python3.10/site-packages/sklearn/base.py", line 1473, in wrapper
    return fit_method(estimator, *args, **kwargs)
  File "/home/gary/.local/lib/python3.10/site-packages/sklearn/linear_model/_logistic.py", line 1194, in fit
    solver = _check_solver(self.solver, self.penalty, self.dual)
  File "/home/gary/.local/lib/python3.10/site-packages/sklearn/linear_model/_logistic.py", line 67, in _check_solver
    raise ValueError(
ValueError: Solver lbfgs supports only 'l2' or None penalties, got l1 penalty.
"""


#for C, marker in zip([0.001, 1, 100], ['o', '^', 'v']):
#    #lr_l1 = LogisticRegression(C=C, penalty="l1").fit(X_train, y_train)
#    print("C = ", C)
#    lr_l1 = LogisticRegression(C=C, penalty="l2").fit(X_train, y_train)
#    print("Training accuracy of l1 logreg with C={:.3f}: {:.2f}".format(
#    C, lr_l1.score(X_train, y_train)))
#    print("Test accuracy of l1 logreg with C={:.3f}: {:.2f}".format(
#    C, lr_l1.score(X_test, y_test)))
#    plt.plot(lr_l1.coef_.T, marker, label="C={:.3f}".format(C))
#    
#plt.xticks(range(cancer.data.shape[1]), cancer.feature_names, rotation=90)
#plt.hlines(0, 0, cancer.data.shape[1])
#plt.xlabel("Coefficient index")
#plt.ylabel("Coefficient magnitude")
#plt.ylim(-5, 5)
#plt.legend(loc=3)
#
#plt.show()
#

# In[47]:
from sklearn.datasets import make_blobs

X, y = make_blobs(random_state=42)
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
#plt.xlabel("Feature 0")
#plt.ylabel("Feature 1")
#plt.legend(["Class 0", "Class 1", "Class 2"])

#plt.show()

# In[48]:
linear_svm = LinearSVC().fit(X, y)
#print("Coefficient shape: ", linear_svm.coef_.shape)
#print("Intercept shape: ", linear_svm.intercept_.shape)

# In[49]:
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
line = np.linspace(-15, 15)
for coef, intercept, color in zip(linear_svm.coef_, linear_svm.intercept_, ['b', 'r', 'g']):
    plt.plot(line, -(line * coef[0] + intercept) / coef[1], c=color)
    
plt.ylim(-10, 15)
plt.xlim(-10, 8)
plt.xlabel("Feature 0")
plt.ylabel("Feature 1")
plt.legend(['Class 0', 'Class 1', 'Class 2', 'Line class 0', 'Line class 1', 'Line class 2'], loc=(1.01, 0.3))

#plt.show()

# In[50]:
mglearn.plots.plot_2d_classification(linear_svm, X, fill=True, alpha=.7)
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
line = np.linspace(-15, 15)
for coef, intercept, color in zip(linear_svm.coef_, linear_svm.intercept_, ['b', 'r', 'g']):
    plt.plot(line, -(line * coef[0] + intercept) / coef[1], c=color)
    
plt.legend(['Class 0', 'Class 1', 'Class 2', 'Line class 0', 'Line class 1', 'Line class 2'], loc=(1.01, 0.3))
plt.xlabel("Feature 0")
plt.ylabel("Feature 1")

plt.show()
