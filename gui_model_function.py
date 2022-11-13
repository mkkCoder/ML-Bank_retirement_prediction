# create function that gets as a parameter a new x (vector of features of a new patient) and a model  and returns the predicted y (the probability of the patient being Parkinsson)
from statistics import mode
import pandas as pd
import numpy as np
import pickle
import pymongo
from sklearn.preprocessing import MinMaxScaler, StandardScaler
# Disable warnings since they abstain us from understanding what is printed...
import warnings
warnings.filterwarnings("ignore")


def load_data_from_db_as_model(client, db):
    myclient = pymongo.MongoClient(client)
    mydb = myclient[db]
    mycollections = mydb.list_collection_names()
    # mycollections = [collection for collection in mycollections if model_name in collection]
    
    classifiers=[]
    for i in mycollections:        
        records=mydb[i].find()
        list_cr=list(records)
        for i in list_cr:
            for j in i['parameters']:
                i[j]=i['parameters'][j]
            del i['parameters']
            
        df=pd.DataFrame(list_cr)
        df['model']=df['model'].apply(lambda x: pickle.loads(x))
        classifier=df['model'][0]
        classifiers.append(classifier)
        
    return classifiers


# # make the data sutable for the prediction function
# myclient = pymongo.MongoClient(CLIENT)
# mydb = myclient['parkinson']
# mycon=mydb['test_to_mongo']
# records=mycon.find()
# patients=list(records)[0]['data']
# p = pickle.loads(patients)

# Xes = p[0]                      # Xes = X_test
# Yes = p[1]                      # Yes = Y_test
# scaler = p[2]                   # scaler = scaler


# new_np_x=np.array([[
# 197.076,206.896,192.055,0.00289,0.00001,0.00166,0.00168,0.00498,0.01098,0.097,0.00563,0.0068,0.00802,0.01689,0.00339,26.775,0.422229,0.741367,-7.3483,0.177551,1.743867,0.085569
# ]])


def predict_y(x):       # x need to be list of features in a list [[feature1,feature2,feature3,...],[feature1,feature2,feature3,...]]
    
    CLIENT='mongodb://localhost:27017'
    DATABASE='Bank_Prediction'




    
    new_pd_x = pd.DataFrame(x)
    print(new_pd_x)

    
    models=load_data_from_db_as_model(CLIENT,DATABASE)

    # make the predictions
    predictions=[]
    for model in models:
        y_pred = model.predict(new_pd_x)
        predictions.append(y_pred[0])
    # print(predictions, end='')
    
    # get the most common prediction (0 or 1)
    majority_vote=mode(predictions)
    
    if majority_vote==1:
        return 1
    else:
        return 0