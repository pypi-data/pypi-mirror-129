# Introduction
Currently the cardiac explainable AI framework consists of these main components:
- Config
- Dataloader
- Model training
- Evaluation
- CAM module will be provided later

The idea is to setup the config to the needs of different experiments and run it to produce results.
The config class has many different parameters which are explained in detail in the following table.

| Supclass     | Variable Name         | Despriction                                                                                                                                                       | Default                                                                                 |
|--------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| File         | training_path         | Directory path to ACDC training data                                                                                                                              | E:/MasterThesis/MA_data/ACDC/training/training/                                         |
|              | output_dir            | Directory where all results will be saved. Results = Processed datasets, logs, models, config JSON, datasplits, performance metrics CSV, confusion matrix, ROCAUC | ../Results/Test/                                                                        |
|              | time                  | Time of creation in format: %Y%m%d-%H%M%S                                                                                                                         | datetime.datetime.now()                                                                 |
|              | filename_h5           | Filename of created dataset HDF5 file                                                                                                                             | acdc_ds_"+str(model.modeltype)+".hdf5                                                   |
|              | h5_path               | Filepath of dataset HDF5 file                                                                                                                                     | os.path.join(self.output_dir, self.filename_h5)                                         |
|              | csv_name              | Filename of CSV dataset file                                                                                                                                      | "acdc_ds_"+str(model.modeltype)+".csv"                                                  |
|              | csv_path              | Filepath of dataset CSV file                                                                                                                                      | os.path.join(self.output_dir,self.csv_name)                                             |
|              | logdir                | Directory to save log training data                                                                                                                               | os.path.join(self.output_dir,'logs')                                                    |
|              | experimentfolder      | Supfolder of experiments (e.g.: for specific task/modeltype)                                                                                                      | _'.join([model.task,model.modeltype])                                                   |
|              | experimentname        | Name of current run                                                                                                                                               | _'.join([model.method,self.time])                                                       |
|              | modeldir              | Directory to store model data (= models, config JSON, datasplits, performance metrics CSV, confusion matrix, ROCAUC)                                              | os.path.join(os.path.join(self.output_dir, self.experimentfolder), self.experimentname) |
| Data         | img_height            | Image height for all slices                                                                                                                                       | 224                                                                                     |
|              | img_width             | Image width for all slices                                                                                                                                        | 224                                                                                     |
|              | as_stack              | If single slices are fake as RGB (staked 3 times) = True. Or saved as greyscale (only 1 dim) = False                                                              | TRUE                                                                                    |
|              | nsplits               | Number of cross-validation splits                                                                                                                                 | 5                                                                                       |
|              | randomstate           | Seed for data                                                                                                                                                     | 1337                                                                                    |
|              | withmask              | If mask is included = True. Or if the segmentaiton masks are not used = False. (e.g. Not used if only classification is performed)                                | FALSE                                                                                   |
|              | diagnosis_dict        | Dictionary of the different classes                                                                                                                               | {'NOR': 0, 'MINF': 1, 'DCM': 2, 'HCM': 3, 'RV': 4}                                      |
|              | n_classes             | Number of classes. Here 5 different diagnosis, therefore 5 classes                                                                                                | 5                                                                                       |
|              | img_shape             | Shape of one processed MR slice. (img_height, img_width, number of stacks)                                                                                        | (self.img_height, self.img_width,3)                                                     |
| Model        | modeltype             | Type of NN model                                                                                                                                                  | vgg16                                                                                   |
|              | task                  | Task of the NN, either segmentation or classification                                                                                                             | classification                                                                          |
|              | weights               | Option for predefined weights                                                                                                                                     | None                                                                                    |
|              | batch_size            | Batch size                                                                                                                                                        | 8                                                                                       |
|              | shuffle_buffer_size   | Shuffle buffer size used for fitting the model to the data                                                                                                        | 2000                                                                                    |
|              | seed                  | Seed for model training                                                                                                                                           | 3574                                                                                    |
|              | base_learning_rate    | Starting learning rate                                                                                                                                            | 1,00E-02                                                                                |
|              | dense                 | Number dense                                                                                                                                                      | 1024                                                                                    |
|              | dropout               | Number of dropout                                                                                                                                                 | 0.2                                                                                     |
|              | method                | Method used for training                                                                                                                                          | training_from_scratch                                                                   |
|              | experiment_assignment | States which experiment this Model is assignet to                                                                                                                 | ex03_gradCAM                                                                            |
|              | loss_function         | Loss function                                                                                                                                                     | categorical_crossentropy                                                                |
| Augmentation | augmentation_type     | Type of augmentation. None, 'with_aug', and 'with_small_aug' to use predefined setting                                                                            | None                                                                                    |
|              | rotation_range        | Range of rotation                                                                                                                                                 | None                                                                                    |
|              | width_shift_range     | Range of width shift                                                                                                                                              | None                                                                                    |
|              | height_shift_range    | Range of height shift                                                                                                                                             | None                                                                                    |
|              | shear_range           | Range of shear                                                                                                                                                    | None                                                                                    |
|              | zoom_range            | Range of zoom                                                                                                                                                     | None                                                                                    |
|              | horizontal_flip       | If horizontal flip will be applied                                                                                                                                | FALSE                                                                                   |
|              | vertical_flip         | If vertical flip will be applied                                                                                                                                  | FALSE                                                                                   |

To generate results multiple steps have to be followed:
1. Processsed Dataset of ACDC
2. Training/Validation/Testing split of data
3. Training the model

## 1. Processsed Dataset of ACDC
To create a processed Dataset the dataloader needs to be used. However, first a config object needs to be created. The parameters for the config class at initiation have to be given as a dictionary. The only path that has to be set for preproccessing the data is the file.training_path which should lead to the directory of the ACDC data (currently saved in my GoogleDrive: https://drive.google.com/file/d/1WlhhPj6CagTHFbDqEuz5jjCEVPRqrL2e/view?usp=sharing)
#### ACDC Data 
initially downloaded from: https://acdc.creatis.insa-lyon.fr/
##### Reference
O. Bernard, A. Lalande, C. Zotti, F. Cervenansky, et al. "Deep Learning Techniques for Automatic MRI Cardiac Multi-structures Segmentation and Diagnosis: Is the Problem Solved ?" in IEEE Transactions on Medical Imaging, vol. 37, no. 11, pp. 2514-2525, Nov. 2018 doi: 10.1109/TMI.2018.2837502

### 1.1 Configuration class
The parameters of the config class can be set as dict for the initialization. Furthermore, an already existing config can be loaded. The parameters/variables need to be changed if other values instead of the default values should be used.
#### Example code
```python
import CXAI_config as CXAI

ds_params = {
    "data": {
            "as_stack": False,
            "diagnosis_dict": {
                "DCM": 2,
                "HCM": 3,
                "MINF": 1,
                "NOR": 0,
                "RV": 4
            },
            "img_height": 224,
            "img_width": 224,
            },
    "file": {
            "training_path": "E:/MasterThesis/MA_data/ACDC/training/training/",
            "experimentname": 'testnr1',
            },
    "model": {
            "modeltype": "own",
            "task": "classification"
            }
}

testclass = CXAI.Experiment_config(ds_params)
``` 

### 1.2 Dataloader Dataset creation
The dataloader consists of two parts. First the dataset_generator which prepares the ACDC dataset as HDF5 file and extract dataset information as CSV. The HDF5 file as well as the CSV s neccessary for the next steps.

#### Example code
```python
import CXAI_dataloader

dataloaderobj = CXAI_dataloader.dataset_generator(_config = testclass)
```
## 2. Dataloader Datasplit
To create datasplits and cross-validation the cv_dataloader class needs to be called. The patient selection as well as the train/test/validation split for each fold are ssaved into the defined output_dir. 
#### Example code
```python
cv_dataloaderobj = CXAI_dataloader.cv_dataloader(testclass)
```

## 3. Training the model
To train the model the a model_training object needs to be initialized before calling the train_model function. Almost all training parameters as well as model design are defined by the configuration class. In the train_model function at the end of each split the evaluation will be automatically done.
#### Example code
```python
import CXAI_model_training
model1 = CXAI_model_training.model_training(_config = testclass, _dataloader = cv_dataloaderobj).train_model()
```


### Example code to run framework
To create the first run through of the framework, this code could be used.

```python
import CXAI_config as CXAI
import CXAI_dataloader
import CXAI_model_training

ds_params = {
    "file": {
            "training_path": "E:/MasterThesis/MA_data/ACDC/training/training/"
            }
}

testclass = CXAI.Experiment_config(ds_params)
dataloaderobj = CXAI_dataloader.dataset_generator(_config = testclass)
cv_dataloaderobj = CXAI_dataloader.cv_dataloader(testclass)
model1 = CXAI_model_training.model_training(_config = testclass, _dataloader = cv_dataloaderobj).train_model()
```
