# Cyclic Boosting Machines

![Build](https://github.com/Microsoft/cbm/workflows/Build/badge.svg)
![Python](https://img.shields.io/pypi/pyversions/cyclicbm.svg)
[![codecov](https://codecov.io/gh/microsoft/CBM/branch/main/graph/badge.svg?token=VRppFx2o8v)](https://codecov.io/gh/microsoft/CBM)
[![PyPI version](https://badge.fury.io/py/cyclicbm.svg)](https://badge.fury.io/py/cyclicbm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Academic Paper](https://img.shields.io/badge/academic-paper-7fdcf7)](https://arxiv.org/abs/2002.03425)

This is an efficient and Scikit-learn compatible implementation of the machine learning algorithm [Cyclic Boosting -- an explainable supervised machine learning algorithm](https://arxiv.org/abs/2002.03425), specifically for predicting count-data, such as sales and demand.

## Features

* Optimized for categorical features
* Continuous features are discretized using [pandas.qcut](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html).
* Date auto-expansion (weekday + month).
* Feature importance plots: categorical, continuous and interactions.
* Metrics to stop training: RMSE, L1, SMAPE.

## Usage

The CBM model predicts by multiplying the global mean with each weight estimate for each bin and feature. Thus the weights can be interpreted as % increase or decrease from the global mean. e.g. a weight of 1.2 for the bin _Monday_ of the feature _Day-of-Week_ can be interpreted as a 20% increase of the target.

<img src="https://render.githubusercontent.com/render/math?math=\hat{y}_i = \mu \cdot \product^{p}_{j=1} f^k_j"> with <img src="https://render.githubusercontent.com/render/math?math=k = \{x_{j,_i} \in b^k_j \}">

```bash
pip install cyclicbm
```

```python
import cbm
from sklearn.metrics import mean_squared_error

# load data using https://www.kaggle.com/c/demand-forecasting-kernels-only
train = pd.read_csv('data/train.csv', parse_dates=['date'])
test  = pd.read_csv('data/test.csv',  parse_dates=['date']) 

# feature engineering
min_date = train['date'].min()

def featurize(df):
    out = pd.DataFrame({
        # TODO: for prediction such features need separate modelling
        'seasonal' : (df['date'] - min_date).dt.days // 60,
        'store'    : df['store'], 
        'item'     : df['item'], 
        'date'     : df['date'],
        # <name-1> _X_ <name-2> to mark interaction features
        'item_X_month': df['item'].astype(str) + '_' + df['date'].dt.month.astype(str)
    })
    
    return out

x_train_df = featurize(train)
x_test_df  = featurize(test)
y_train = train['sales']

# model training
model = cbm.CBM()
model.fit(x_train_df, y_train)

# test on train error
y_pred_train = model.predict(x_train_df).flatten()
print('RMSE', mean_squared_error(y_pred_train, y_train, squared=False))

# plotting
model.plot_importance(figsize=(20, 20), continuous_features=['seasonal'])
```

![Feature Importance Plot](images/cbm_kaggle.png)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
