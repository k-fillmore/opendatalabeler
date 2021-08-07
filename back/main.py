from fastapi import FastAPI, UploadFile, File, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import  json
from typing import List
import shutil
import zipfile



app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Dataset(BaseModel):
    name: str
    id: str
    kind: str
    problem: str
    count: dict = {"Original":0, "train":0, "test":0, "valid":0}


@app.get("/")
async def root():
    return {"message": "World"}

@app.post("/api/upload/images/")
async def upload_image( datasetName: str, images: List[UploadFile] = File(...)):
    print(images, datasetName)
    dirpath = "./datasets/"+datasetName+"/data/"
    for image in images:
        with open("./datasets/temp/"+datasetName+".zip", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        

@app.post("/api/dataset")
async def create_dataset(dataset: Dataset):
    print(dataset)
    root_path = "./datasets/" + dataset.name + "/"
    data_path = root_path + "data/"

    if not os.path.exists(root_path):
        os.makedirs(root_path)
        os.mkdir(data_path)
        os.mkdir(data_path+"train/")
        os.mkdir(data_path+"valid/")
        os.mkdir(data_path+"test/")
        os.mkdir(data_path+"original/")
        properties = {}
        properties["name"] = dataset.name
        properties["id"] = dataset.id
        properties["kind"] = dataset.kind
        properties["data_path"] = data_path
        properties["problem"] = dataset.problem  
        properties["count"] = dataset.count      
        with open(root_path + "properties.json", "w") as f:
            json.dump(properties, f)
    if os.path.exists("./datasets/temp/"+dataset.name+".zip"):
        with zipfile.ZipFile("./datasets/temp/"+dataset.name+".zip", 'r') as zip_ref:
            zip_ref.extractall(data_path+"/original/")
    #delte mac metadata -- not needed
    if os.path.exists(data_path+"/original/__MACOSX"):
        shutil.rmtree(data_path+"/original/__MACOSX")

@app.get("/api/allDatasets")
async def get_all_datasets():
    datasets = []
    for dataset in os.listdir("./datasets/"):
        if dataset == "temp":
            continue
        if os.path.isdir("./datasets/"+dataset):
            with open("./datasets/"+dataset+"/properties.json", "r") as f:
                properties = json.load(f)
                datasets.append(properties)
    return datasets

@app.get("/api/dataset/")
async def get_dataset(dataset_id: str):
    datasets = []
    for dataset in os.listdir("./datasets/"):
        if dataset == "temp":
            continue
        if os.path.isdir("./datasets/"+dataset):
            with open("./datasets/"+dataset+"/properties.json", "r") as f:
                properties = json.load(f)
                if properties["id"] == dataset_id:
                    datasets.append(properties)
    return datasets

@app.get("/api/dataset/fetchExample")
async def get_dataset_example(dataset_id: str):
    ds = get_dataset(dataset_id)
    if len(ds) == 0:
        return {"message": "No dataset found"}
    dataset = ds[0]
    data_path = dataset["data_path"]
    files = os.listdir(data_path+"original/")
    return FileResponse(files[0], filename=files[0])

@app.post("/api/dataset/moveExample")
async def get_dataset_example(dataset_id: str, file: str, type: str):
    ds = get_dataset(dataset_id)
    if len(ds) == 0:
        return {"message": "No dataset found"}
    dataset = ds[0]
    data_path = dataset["data_path"]
    if type == "train":
        shutil.move(data_path+"original/"+file, data_path+"train/"+file)
        return {"message": "Moved to train"}
    elif type == "valid":
        shutil.move(data_path+"original/"+file, data_path+"valid/"+file)
        return {"message": "Moved to valid"}
    elif type == "test":
        shutil.move(data_path+"original/"+file, data_path+"test/"+file)
        return {"message": "Moved to test"}
    else:
        return {"message": "Invalid type"}

@app.post("/api/dataset/moveIncorrectExample")
async def get_dataset_example(dataset_id: str, file: str, src: str, dest: str):
    ds = get_dataset(dataset_id)
    if len(ds) == 0:
        return {"message": "No dataset found"}
    dataset = ds[0]
    data_path = dataset["data_path"]
    if src == "train":
        shutil.move(data_path+"train/"+file, data_path+dest+"/"+file)
        return {"message": "Moved to {dest}"}
    elif src == "valid":
        shutil.move(data_path+"valid/"+file, data_path+dest+"/"+file)
        return {"message": "Moved to {dest}"}
    elif src == "test":
        shutil.move(data_path+"test/"+file, data_path+dest+"/"+file)
        return {"message": "Moved to {dest}"}
    else:
        return {"message": "Invalid type"}

@app.post("/api/dataset/label/add")
async def add_dataset_labels(dataset_id: str, label:str):
    ds = get_dataset(dataset_id)
    if len(ds) == 0:
        return {"message": "No dataset found"}
    dataset = ds[0]
    if "label" in ds.keys():
        ds["label"].append(label)
    else:
        ds["label"] = [label]
    with open("./datasets/"+dataset["name"]+"/properties.json", "w") as f:
        json.dump(ds, f)
    return {"message": "Label added"}

@app.post("/api/dataset/label/delete")
async def delete_dataset_labels(dataset_id: str, label:str):
    ds = get_dataset(dataset_id)
    if len(ds) == 0:
        return {"message": "No dataset found"}
    dataset = ds[0]
    if "label" in ds.keys():
        ds["label"].remove(label)
    else:
        return {"message": "No labels found"}
    with open("./datasets/"+dataset["name"]+"/properties.json", "w") as f:
        json.dump(ds, f)
    return {"message": "Label deleted"}

@app.post("/api/dataset/label/rename")
async def rename_dataset_labels(dataset_id: str, old_label:str, new_label:str):
    ds = get_dataset(dataset_id)
    if len(ds) == 0:
        return {"message": "No dataset found"}
    dataset = ds[0]
    if "label" in ds.keys():
        for i, label in enumerate(ds["label"]):
            if label == old_label:
                ds["label"][i] = new_label
    else:
        return {"message": "No labels found"}
    with open("./datasets/"+dataset["name"]+"/properties.json", "w") as f:
        json.dump(ds, f)
    return {"message": "Label renamed"}
@app.get("/api/dataset/export")
async def export_dataset(dataset_id: str):
    ds = get_dataset(dataset_id)
    if len(ds) == 0:
        return {"message": "No dataset found"}
    dataset = ds[0]
    data_path = dataset["data_path"]
    dir_list = ["./datasets/"+dataset["name"]+"/train/", "./datasets/"+dataset["name"]+"/valid/", "./datasets/"+dataset["name"]+"/test/"]
    zipf = zipfile.ZipFile(data_path+"export.zip", 'w', zipfile.ZIP_DEFLATED)
    for dir in dir_list:
        zipdir(dir, zipf)
    zipf.close()

#helper function for export
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
