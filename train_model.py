import yaml,json, logging, os, shutil, multiprocessing

def run_job(command):
    os.system(command)

def train_model(model_definition, output_dir, data_csv, experiment_name, log_file):
    
    dir_list = os.listdir(output_dir)
    print(dir_list)
    if 'training.log' in dir_list:
        a = open(output_dir+'/training.log','r')
        data = (a.readlines())[::-1]

        for x in data:
            if "Epoch" in x:
                return (x[:-1])
        return ("Training Started")

    try:
        shutil.rmtree("{}/{}_run_0".format(output_dir,experiment_name))
        print ("This experiment already exists. Removing the existing model")

    except:
        pass

    command = "ludwig train --data_csv {} --output_directory {} --experiment_name {} --model_definition_file {} > {}".format(data_csv, output_dir, experiment_name, model_definition, log_file)

    print (command)
    p = multiprocessing.Process(target=run_job, args=(command,))
    p.start()
    return True


# model_definition = "mnist_png/model_definition.yaml"
# data_csv = "mnist_png/mnist_dataset_training.csv"
# experiment_name = "test_exp"

# train_model(model_definition, data_csv, experiment_name)
