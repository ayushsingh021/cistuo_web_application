import cv2
import glob
import os
from vehicle_detector import VehicleDetector



# Load Veichle Detector
vd = VehicleDetector()

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

        cv2.putText(img, "Vehicles: " + str(vehicle_count), (20, 50), 0, 2, (10, 10, 10), 3)

    filename = os.path.basename(img_path)
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, img)
    
    # cv2.imshow("Cars", img)
    # cv2.waitKey(1)

print("Total current count", vehicles_folder_count)