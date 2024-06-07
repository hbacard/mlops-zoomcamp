import mlflow
import pickle

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Taxi duration prediction")
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, **kwargs):
    model, vectorizer = data[0], data[1]
    with mlflow.start_run(run_name="saving_model"):
        mlflow.sklearn.log_model(model, "lr-duration-prediction")
        vectorizer_path = "dict_vectorizer.pkl"
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
        
        # loging vectorizer
        mlflow.log_artifact(vectorizer_path)

    # Specify your data exporting logic here


