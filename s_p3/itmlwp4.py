# itmlwp2.py
# Introduction to Machine Learning with Python (2017)
# Follow along and testing Chp. 2

import mglearn

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, colorConverter, LinearSegmentedColormap

import numpy as np

#In[2]:
import pandas as pd
"""
# The file has no headers naming the columns, so we pass header=None
# and provide the column names explicitly in "names"
data = pd.read_csv("/home/gary/src/s_p3/data/adult.data",
                   header=None, index_col=False,
                   names=['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                          'marital-status', 'occupation', 'relationship', 'race', 'gender',
                          'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
                          'income'])

# For illustration purposes, we only select some of the columns
data = data[['age', 'workclass', 'education', 'gender', 'hours-per-week','occupation', 'income']]

# IPython.display allows nice output formatting within the Jupyter notebook
#display(data.head())

print(data.head)

# In[3]:
#print(data.gender.value_counts())

print('-----')
print(data.age.value_counts())
print('-----')
print(data.workclass.value_counts())
print('-----')
print(data.education.value_counts())
print('-----')
print(data.gender.value_counts())
print('-----')
#print(data.hours-per-week.value_counts()) # Throwing error: AttributeError: 'DataFrame' object has no attribute 'hours'
print('-----')
print(data.occupation.value_counts())
print('-----')
print(data.income.value_counts())
print('---------')

# In[4]:
print("Original features:\n", list(data.columns), "\n")
print('-----')
data_dummies = pd.get_dummies(data)
print("Features after get_dummies:\n", list(data_dummies.columns))
print('-----')
lst_dd = list(data_dummies.columns)
for c in lst_dd:
    print(c)

# In[5]:
print('\n', data_dummies.head())
print('----------')

# In[6]:
#features = data_dummies.ix[:, 'age':'occupation_ Transport-moving']
features = data_dummies.loc[:, 'age':'occupation_ Transport-moving']

# Extract NumPy arrays
X = features.values
y = data_dummies['income_ >50K'].values

print("X.shape: {} y.shape: {}".format(X.shape, y.shape))

# In[7]:
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

print("Test score: {:.2f}".format(logreg.score(X_test, y_test)))
print('----------')

# In[8]:
# create a DataFrame with an integer feature and a categorical string feature
demo_df = pd.DataFrame({'Integer Feature': [0, 1, 2, 1],
                        'Categorical Feature': ['socks', 'fox', 'socks', 'box']})
#display(demo_df)
print(demo_df)

# In[9]:
print(pd.get_dummies(demo_df))

# In[10]:
demo_df['Integer Feature'] = demo_df['Integer Feature'].astype(str)

print(pd.get_dummies(demo_df, columns=['Integer Feature', 'Categorical Feature']))
"""

# In[11]:
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

X, y = mglearn.datasets.make_wave(n_samples=100)

line = np.linspace(-3, 3, 1000, endpoint=False).reshape(-1, 1)

reg = DecisionTreeRegressor(min_samples_split=3).fit(X, y)

"""
plt.plot(line, reg.predict(line), label="decision tree")
reg = LinearRegression().fit(X, y)

plt.plot(line, reg.predict(line), label="linear regression")
plt.plot(X[:, 0], y, 'o', c='k')
plt.ylabel("Regression output")
plt.xlabel("Input feature")
plt.legend(loc="best")

plt.show()
"""
"""
# In[12]:
bins = np.linspace(-3, 3, 11)

# In[13]:
which_bin = np.digitize(X, bins=bins)

#print("\nData points:\n", X[:5])
#print("\nBin membership for data points:\n", which_bin[:5])
#print("bins: {}".format(bins))

# In[14]:
from sklearn.preprocessing import OneHotEncoder

# transform using the OneHotEncoder
#encoder = OneHotEncoder(sparse=False)
encoder = OneHotEncoder(sparse_output=False)

# encoder.fit finds the unique values that appear in which_bin
encoder.fit(which_bin)

# transform creates the one-hot encoding
X_binned = encoder.transform(which_bin)

#print('\n', X_binned[:5])

# In[15]:
#print("X_binned.shape: {}".format(X_binned.shape))

# In[16]:
line_binned = encoder.transform(np.digitize(line, bins=bins))

reg = LinearRegression().fit(X_binned, y)

plt.plot(line, reg.predict(line_binned), label='linear regression binned')

reg = DecisionTreeRegressor(min_samples_split=3).fit(X_binned, y)

plt.plot(line, reg.predict(line_binned), label='decision tree binned')
plt.plot(X[:, 0], y, 'o', c='k')
plt.vlines(bins, -3, 3, linewidth=1, alpha=.2)
plt.legend(loc="best")
plt.ylabel("Regression output")
plt.xlabel("Input feature")

#plt.show()

# In[17]:
X_combined = np.hstack([X, X_binned])
print(X_combined.shape)


# In[18]:
reg = LinearRegression().fit(X_combined, y)

line_combined = np.hstack([line, line_binned])

plt.plot(line, reg.predict(line_combined), label='linear regression combined')

for bin in bins:
    plt.plot([bin, bin], [-3, 3], ':', c='k')

plt.legend(loc="best")
plt.ylabel("Regression output")
plt.xlabel("Input feature")
plt.plot(X[:, 0], y, 'o', c='k')

#plt.show()

# In[19]:
X_product = np.hstack([X_binned, X * X_binned])
print(X_product.shape)

# In[20]:
reg = LinearRegression().fit(X_product, y)

line_product = np.hstack([line_binned, line * line_binned])

plt.plot(line, reg.predict(line_product), label='linear regression product')

for bin in bins:
    plt.plot([bin, bin], [-3, 3], ':', c='k')
    
plt.plot(X[:, 0], y, 'o', c='k')
plt.ylabel("Regression output")
plt.xlabel("Input feature")
plt.legend(loc="best")

#plt.show()

# In[21]:
from sklearn.preprocessing import PolynomialFeatures
# include polynomials up to x ** 10:
# the default "include_bias=True" adds a feature that's constantly 1
poly = PolynomialFeatures(degree=10, include_bias=False)
poly.fit(X)
X_poly = poly.transform(X)

# In[22]:
print("X_poly.shape: {}".format(X_poly.shape))

# In[23]:
print("Entries of X:\n{}".format(X[:5]))
print("Entries of X_poly:\n{}".format(X_poly[:5]))

# In[24]:
#print("Polynomial feature names:\n{}".format(poly.get_feature_names()))
print("Polynomial feature names:\n{}".format(poly.get_feature_names_out()))

# In[26]:
reg = LinearRegression().fit(X_poly, y)

line_poly = poly.transform(line)

plt.plot(line, reg.predict(line_poly), label='polynomial linear regression')
plt.plot(X[:, 0], y, 'o', c='k')
plt.ylabel("Regression output")
plt.xlabel("Input feature")
plt.legend(loc="best")

#plt.show()

# In[26]:
from sklearn.svm import SVR

for gamma in [1, 10]:
    svr = SVR(gamma=gamma).fit(X, y)
    plt.plot(line, svr.predict(line), label='SVR gamma={}'.format(gamma))
    
plt.plot(X[:, 0], y, 'o', c='k')
plt.ylabel("Regression output")
plt.xlabel("Input feature")
plt.legend(loc="best")

plt.show()
"""
"""
from sklearn.preprocessing import PolynomialFeatures

# In[27]:
#from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()

#boston = load_boston()

#X_train, X_test, y_train, y_test = train_test_split(boston.data, boston.target, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(housing.data, housing.target, random_state=0)


# rescale data
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# In[28]:
poly = PolynomialFeatures(degree=2).fit(X_train_scaled)

X_train_poly = poly.transform(X_train_scaled)
X_test_poly = poly.transform(X_test_scaled)

print("X_train.shape: {}".format(X_train.shape))
print("X_train_poly.shape: {}".format(X_train_poly.shape))

# In[29]:
print("Polynomial feature names:\n{}".format(poly.get_feature_names_out()))

# In[30]:
from sklearn.linear_model import Ridge

ridge = Ridge().fit(X_train_scaled, y_train)
print("Score without interactions: {:.3f}".format(

ridge.score(X_test_scaled, y_test)))
ridge = Ridge().fit(X_train_poly, y_train)

print("Score with interactions: {:.3f}".format(ridge.score(X_test_poly, y_test)))

# In[31]:
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=100).fit(X_train_scaled, y_train)
print("Score without interactions: {:.3f}".format(rf.score(X_test_scaled, y_test)))

rf = RandomForestRegressor(n_estimators=100).fit(X_train_poly, y_train)
print("Score with interactions: {:.3f}".format(rf.score(X_test_poly, y_test)))
"""
"""
# In[32]:
rnd = np.random.RandomState(0)

X_org = rnd.normal(size=(1000, 3))

w = rnd.normal(size=3)

X = rnd.poisson(10 * np.exp(X_org))

y = np.dot(X_org, w)

# In[33]:
print("Number of feature appearances:\n{}".format(np.bincount(X[:, 0])))

# In[34]:
#bins = np.bincount(X[:, 0])
#
#plt.bar(range(len(bins)), bins, color='b')
#plt.ylabel("Number of appearances")
#plt.xlabel("Value")

#plt.show()

from sklearn.model_selection import train_test_split

# In[35]:
from sklearn.linear_model import Ridge

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

score = Ridge().fit(X_train, y_train).score(X_test, y_test)

print("Test score: {:.3f}".format(score))


# Because the value 0 appears in the data (and the logarithm is not defined at
# 0), we can’t actually just apply log, but we have to compute log(X + 1):
#
# In[36]:
X_train_log = np.log(X_train + 1)
X_test_log = np.log(X_test + 1)

# In[37]:
plt.hist(np.log(X_train_log[:, 0] + 1), bins=25, color='gray')
plt.ylabel("Number of appearances")
plt.xlabel("Value")

#plt.show()

# In[38]:
score = Ridge().fit(X_train_log, y_train).score(X_test_log, y_test)
print("Test score: {:.3f}".format(score))
"""

# In[39]:
from sklearn.datasets import load_breast_cancer
from sklearn.feature_selection import SelectPercentile
from sklearn.model_selection import train_test_split

cancer = load_breast_cancer()

# get deterministic random numbers
rng = np.random.RandomState(42)
noise = rng.normal(size=(len(cancer.data), 50))

# add noise features to the data
# the first 30 features are from the dataset, the next 50 are noise
X_w_noise = np.hstack([cancer.data, noise])
X_train, X_test, y_train, y_test = train_test_split(X_w_noise, cancer.target, random_state=0, test_size=.5)

# use f_classif (the default) and SelectPercentile to select 50% of features
select = SelectPercentile(percentile=50)
select.fit(X_train, y_train)

# transform training set
X_train_selected = select.transform(X_train)

print("X_train.shape: {}".format(X_train.shape))
print("X_train_selected.shape: {}".format(X_train_selected.shape))

# In[40]:
mask = select.get_support()
print(mask)

# visualize the mask -- black is True, white is False
plt.matshow(mask.reshape(1, -1), cmap='gray_r')
plt.xlabel("Sample index")

plt.show()

# In[41]:
from sklearn.linear_model import LogisticRegression

# transform test data
X_test_selected = select.transform(X_test)
lr = LogisticRegression()
lr.fit(X_train, y_train)

print("Score with all features: {:.3f}".format(lr.score(X_test, y_test)))

lr.fit(X_train_selected, y_train)

print("Score with only selected features: {:.3f}".format(lr.score(X_test_selected, y_test)))
