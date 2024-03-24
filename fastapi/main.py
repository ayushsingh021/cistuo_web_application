# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import FileResponse
# import os
# from random import randint
# import uuid
# from fastapi.middleware.cors import CORSMiddleware
 
# IMAGEDIR = "images/"
 
# app = FastAPI()
 

# # Set up CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # Update this with your frontend's origin
#     allow_credentials=True,
#     allow_methods=["GET", "POST"],
#     allow_headers=["*"],
# )

 
# @app.post("/api/upload/")
# async def create_upload_file(file: UploadFile = File(...)):
    
#     file.filename = f"{uuid.uuid4()}.jpg"
#     contents = await file.read()
 
#     #save the file
#     with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
#         f.write(contents)
 
#     return {"filename": file.filename}
 
 
# @app.get("/api/show/")
# async def read_random_file():
 
#     # get random file from the image directory
#     files = os.listdir(IMAGEDIR)
#     random_index = randint(0, len(files) - 1)
 
#     path = f"{IMAGEDIR}{files[random_index]}"
     
#     return FileResponse(path)


from fastapi import FastAPI,HTTPException, File, UploadFile
from typing import List
import os
import uuid
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from cloudinary.uploader import upload

import cv2
import glob
import os
from vehicle_detector import VehicleDetector

app = FastAPI()

load_dotenv()

IMAGEDIR = "./images/"

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],  # Update this with your frontend's origin
    allow_origins=["*"],  # Allow all origins, you may want to restrict this in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

# print(cloud_name)

IMAGEDIRECT = "images" 

@app.post("/api/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
        with open(os.path.join(IMAGEDIR, filename), "wb") as f:
            f.write(contents)
        filenames.append(filename)
    return {"filenames": filenames}


# Load Vehicle Detector
vd = VehicleDetector()

def process_images():
    # Load images from a folder
    images_folder = glob.glob("images/*.jpg")

    vehicles_folder_count = 0

    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all the images
    for img_path in images_folder:
        print("Img path", img_path)
        img = cv2.imread(img_path)

        vehicle_boxes = vd.detect_vehicles(img)
        vehicle_count = len(vehicle_boxes)

        # Update total count
        vehicles_folder_count += vehicle_count

        for box in vehicle_boxes:
            x, y, w, h = box

            cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 3)
            cv2.putText(img, "Vehicles: " + str(vehicle_count), (20, 50), 0, 2, (100, 200, 0), 3)

        filename = os.path.basename(img_path)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, img)

    print("Total current count", vehicles_folder_count)
    return vehicles_folder_count

@app.get("/api/process_images")
async def process_images_endpoint():
    vehicles_count = process_images()
    return {"vehicles_count": vehicles_count}


# Route for uploading images to Cloudinary
@app.get("/api/upload-images/")
async def upload_images_to_cloudinary():
    try:
        cloudinary_urls = []
        # Iterate over the files in the local directory
        for filename in os.listdir(IMAGEDIRECT):
            # Upload file to Cloudinary
            file_path = os.path.join(IMAGEDIRECT, filename)
            response = upload(file_path, cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
            # Append the URL of the uploaded image to the list
            cloudinary_urls.append(response["secure_url"])

        return {"cloudinary_urls": cloudinary_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


IMAGEDIRECTSHOW = "output_images" 
# Route for uploading images to Cloudinary
@app.get("/api/download-images/")
async def download_images_to_cloudinary():
    try:
        cloudinary_urls = []
        # Iterate over the files in the local directory
        for filename in os.listdir(IMAGEDIRECTSHOW ):
            # Upload file to Cloudinary
            file_path = os.path.join(IMAGEDIRECTSHOW , filename)
            response = upload(file_path, cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
            # Append the URL of the uploaded image to the list
            cloudinary_urls.append(response["secure_url"])

        return {"cloudinary_urls": cloudinary_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
