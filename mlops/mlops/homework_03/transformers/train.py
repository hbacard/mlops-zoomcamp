from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

categorical_features = ['PULocationID','DOLocationID']
target = 'duration'

@transformer
def transform(df, *args, **kwargs):
    
    dv = DictVectorizer()
    df_features = df[categorical_features]
    X_dict = df_features.to_dict(orient='records')

    # creating train data
    X_train = dv.fit_transform(X_dict)
    y_train = df[target]


    # modeling 
    lr = LinearRegression()
    # training
    lr.fit(X_train, y_train)

    print(lr.intercept_)


    return lr, dv