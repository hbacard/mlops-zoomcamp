import jsonify
import pickle

with open("my_model.bin", "rb") as f_bin:
    dv, model = pickle.load(f_bin)



def prepare(data):
    features = {}
    features['PULocationID'] = data.get('PULocationID')
    features['DOLocationID'] = data.get('DOLocationID')
    return features

def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]



test_features = {
    'PULocationID': 10, 
    'DOLocationID': 34
}

if __name__ == "__main__":
    X = dv.transform(test_features)
    print(X)
    print()
    print(predict(test_features))
    

