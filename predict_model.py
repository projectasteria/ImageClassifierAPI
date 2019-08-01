import yaml, json, logging, os, shutil

def predict_model(model_definition, data_csv, experiment_name):
    
    try:
        shutil.rmtree("results/{}_results".format(experiment_name))
        print ("This experiment already exists. Removing the existing model")
        
    except:
        pass
        
    run_file = "results/{}".format(experiment_name)+"_run_0\model"

    os.system("ludwig predict --data_csv {} -od results\{} --model_path {} &> file.log".format(data_csv, experiment_name+"_results", run_file))

# model_definition = "mnist_png/model_definition.yaml"
# data_csv = "mnist_png/mnist_dataset_testing.csv"
# experiment_name = "test_exp"

# predict_model(model_definition, data_csv, experiment_name)