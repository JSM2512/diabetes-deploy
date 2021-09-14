from django.shortcuts import render
from django.http import HttpResponse
import joblib
import pandas as pd
reloadModel=joblib.load('./models/ModelforDiabetes.pkl')
# Create your views here.

# ------------- DATABASE CONNECTION-------------
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://jaiwant:jaiwant@113406@cluster0-shard-00-00.vtex2.mongodb.net:27017,cluster0-shard-00-01.vtex2.mongodb.net:27017,cluster0-shard-00-02.vtex2.mongodb.net:27017/diabetesDB?ssl=true&replicaSet=atlas-k3jdce-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

collectionD=dbname["diabetesTable"]

# from django.conf import settings
# my_client = pymongo.MongoClient(settings.DB_NAME)

# # First define the database name
# dbname = my_client['diabetesDB']

# # Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection)
# collection_name = dbname["diabetesTable"]

# import pymongo 
# import urllib 

# mongo_uri = "mongodb://jaiwant:" + urllib.quote("jaiwant@113406") + "@0.0.0.0:27001/"
# client = pymongo.MongoClient(mongo_uri)
# ----------------------------------------------

def index(request):
    temp = {}
    temp['Pregnancies'] = 6
    temp['Glucose'] = 148
    temp['BloodPressure'] = 72
    temp['SkinThickness'] = 35
    temp['Insulin'] = 0
    temp['BMI_year'] = 33.6
    temp['DiabetesPedigreeFunction'] = 0.627
    temp['Age'] = 50
    context={'temp':temp}
    return render(request,'index.html',context)
    # return HttpResponse({'a':1})
def predictDia(request):
    print(request)
    if request.method=='POST':
        temp = {}
        temp['Pregnancies'] = request.POST.get('pregVal')
        temp['Glucose'] = request.POST.get('gluVal')
        temp['BloodPressure'] = request.POST.get('bpVal')
        temp['SkinThickness'] = request.POST.get('stVal')
        temp['Insulin'] = request.POST.get('insVal')
        temp['BMI_year'] = request.POST.get('bmiVal')
        temp['DiabetesPedigreeFunction'] = request.POST.get('predfunVal')
        temp['Age'] = request.POST.get('ageVal')

        # context={'temp':temp}

        temp2=temp.copy()
        temp2['BMI year']=temp['BMI_year']
        print(temp.keys(),temp2.keys())
        del temp2['BMI_year']
        # print(request.POST.dict())
        # print(request.POST.get('cylinderVal'))
    # we have a dictionary and the model is expecting a dataframe so we will make a dataframe
    testDtaa=pd.DataFrame({'x':temp2}).transpose()
    # for scoring data
    scoreval=reloadModel.predict(testDtaa)[0]
    context={'scoreval':scoreval,'temp':temp}
    return render(request,'index.html',context)
def viewDataBase(request):
    countOfrow=collectionD.find().count()
    context={'countOfrow':countOfrow}
    return render(request,'viewDB.html',context)

def updateDataBase(request):
    temp = {}
    temp['Pregnancies'] = request.POST.get('pregVal')
    temp['Glucose'] = request.POST.get('gluVal')
    temp['BloodPressure'] = request.POST.get('bpVal')
    temp['SkinThickness'] = request.POST.get('stVal')
    temp['Insulin'] = request.POST.get('insVal')
    temp['BMI year'] = request.POST.get('bmiVal')
    temp['DiabetesPedigreeFunction'] = request.POST.get('predfunVal')
    temp['Age'] = request.POST.get('ageVal')
    # store in database
    collectionD.insert_one(temp)
    countOfrow = collectionD.find().count()
    # show the updated count
    context = {'countOfrow': countOfrow}
    return render(request, 'viewDB.html', context)

# Create your views here.
