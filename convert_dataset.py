# %%
import json
import os

import cv2

# Load the JSON file
dataset_dir = "/hpctmp/zwj/datasets/IDID/Train/"
image_dir = os.path.join(dataset_dir, "Images")

with open(os.path.join(dataset_dir,'labels_v1.2.json')) as f:
    data = json.load(f)

# %%
from copy import deepcopy
def save_images(stage, data, image_dir, save_dir):
    for idx, image in enumerate(data):
        # Add the image to the "images" list in the output data
        file_name = image['filename']
        data[idx]['filename'] = file_name.replace('.JPEG', '.jpg').replace('.JPG','.jpg').replace('.jpeg','.jpg') # change the file name to unify them
        img = cv2.imread(os.path.join(image_dir, file_name))
        # copy the image to the output directory
        cv2.imwrite(os.path.join(save_dir, 'images', stage, data[idx]['filename']), img)
        # os.system("cp {} {}".format(os.path.join(image_dir, file_name), os.path.join(save_dir, 'images', stage, file_name)))
        # print(file_name, "copied")
        print(file_name,idx, "converted")
    return data

# %%

def convert_to_coco(stage, data, image_dir, save_dir):
    # Initialize the output COCO JSON data
    output_data = {
        "categories": [{'id': 0, 'name': 'insu', 'supercategory': 'none'}
                       , {'id': 1, 'name': "insu{'shell': 'Broken'}"
                        , 'supercategory': 'none'}
                       , {'id': 2, 'name': 'insu-str-', 'supercategory': 'none'}
                       , {'id': 3, 'name': "insu{'glaze': 'Flashover damage'}", 'supercategory': 'none'}]
        , "images": []
        , "annotations": []
    }

    # Loop through each image
    for image in data:
        # Add the image to the "images" list in the output data
        file_name = image['filename']
        img = cv2.imread(os.path.join(image_dir, file_name))
        print(file_name)
        output_data["images"].append({
            "id": len(output_data["images"]) + 1,
            "file_name": file_name, #.replace('.JPEG', '.jpg').replace('.JPG','.jpg').replace('.jpeg','.jpg'), # change the file name to unify them
            # set width by reading from the file_name using cv2 and get the width
            "width": img.shape[1],
            "height": img.shape[0],
        })

        # Loop through each object in the image
        for obj in image["Labels"]["objects"]:
            # Add the object to the "annotations" list in the output data
            if int(obj.get('string', 0)) == 0:
                string_re = ''
            else:
                string_re = f"-str-"
            conditions = str(obj.get('conditions', 'None'))
            if "no issue" in conditions.lower() \
                    or "none" in conditions.lower() \
                    or "notbroken" in conditions.lower() \
                    or "notflash" in conditions.lower():
                conditions = ""
            label = obj['name'][0:4] + string_re + conditions
            # check if the label is in the categories list
            if label not in [cat['name'] for cat in output_data['categories']]:
                output_data['categories'].append({'id': len(output_data['categories']) + 1, 'name': label, 'supercategory': 'none'})
            # get the index of the label in the categories list
            cat_id = [cat['id'] for cat in output_data['categories'] if cat['name'] == label][0]
            output_data["annotations"].append({
                "id": len(output_data["annotations"]),
                "image_id": output_data["images"][-1]["id"],
                "category_id": cat_id,
                "bbox": obj["bbox"],
                "iscrowd": 0
            })
    with open(os.path.join(save_dir,f'{stage}-labels-coco.json'), 'w') as outfile:
        # write the dictionary to the file in a pretty format
        json.dump(output_data, outfile, indent=4)
    print("output categories: ", output_data['categories'])

# %%
def convert_to_yolo(stage, data,image_dir, save_dir):
    import cv2, numpy as np
    labels = ['insu', "insu{'shell': 'Broken'}", 'insu-str-', "insu{'glaze': 'Flashover damage'}"]
    for file_info in data:
        filename = file_info['filename']
        random_number = np.random.uniform(0, 1)
        # if random_number < 0.7:
        #     stage = "train"
        # elif random_number < 0.8:
        #     stage = "val"    
        # else:
        #     stage = "test"   
        # read the image named as filename
        img = cv2.imread(os.path.join(image_dir, f"{filename}"))
        img_height, img_width, _ = img.shape
        # filename = filename.replace('.JPEG', '.jpg').replace('.JPG','.jpg').replace('.jpeg','.jpg')
        #use append mode to write the output to the file
        with open(os.path.join(save_dir, f"{stage}-samples.txt"), 'a') as f:
                f.write(filename + '\n')
        # cv2.imwrite(os.path.join(yolo_dataset_path, f"images/{stage}/{filename}"), img)
        for obj in file_info['Labels']['objects']:
            # Extract the class label, bounding box coordinates, and image size
            if int(obj.get('string', 0)) == 0: 
                string_re = ''
            else:
                string_re = f"-str-"
            conditions = str(obj.get('conditions', 'None'))
            if "no issue" in conditions.lower()\
                or "none" in conditions.lower()\
                or "notbroken" in conditions.lower()\
                or "notflash" in conditions.lower():
                conditions = ""
            label = obj['name'][0:4]+string_re+conditions
            x = obj['bbox'][0]
            y = obj['bbox'][1]
            width = obj['bbox'][2]
            height = obj['bbox'][3]
            # Calculate the center coordinates and the normalized width and height
            # relative to the image size
            x_center = (x + width / 2) / img_width
            y_center = (y + height/ 2) / img_height
            width_norm = width / img_width
            height_norm = height / img_height
            # Generate the YOLO format output
            if label not in labels:
                labels.append(label)
            # get the index of the label in the labels
            label_index = labels.index(label)
            output = ' '.join([str(label_index), str(x_center), str(y_center),
                            str(width_norm), str(height_norm)])
            #use append mode to write the output to the file
            with open(os.path.join(save_dir, f"labels/{stage}/{filename.split('.')[0]}.txt"), 'a') as f:
                    f.write(output + '\n')
    print(labels)
    # save labels to yolo-classes.txt
    with open(os.path.join(save_dir, f"yolo-classes.txt"), 'w') as f:
        f.write(str(labels))
    len(labels)


# %%
def clean_dir(save_dir):
    import os, glob
    yolo_dataset_path = save_dir
    os.system("rm -r " + yolo_dataset_path)
    # mkdir the path
    os.makedirs(yolo_dataset_path, exist_ok=True)
    # this part for yolo
    for img_type in ['images', 'labels']:
        os.system("rm -r " + os.path.join(yolo_dataset_path, img_type))
        os.system("mkdir " + os.path.join(yolo_dataset_path, img_type))
        for stage in ['train', 'val', 'test']:
            os.makedirs(os.path.join(yolo_dataset_path, img_type, stage), exist_ok=True)

# %%
# do train val test split for data
from sklearn.model_selection import train_test_split
train_data,test_data, _, _  = train_test_split(data,[0]*len(data), test_size=0.2, random_state=42)
train_data,val_data, _, _  = train_test_split(train_data,[0]*len(train_data), test_size=0.2, random_state=42)
data_dict = {"test":test_data, "val":val_data, "train":train_data}

# %%
test_data

# %%
save_dir = os.path.join(dataset_dir, "combined_dataset")
clean_dir(save_dir)
for stage, data in data_dict.items():   
    data = save_images(stage, data, image_dir, save_dir)
    new_image_dir = os.path.join(save_dir, "images",stage)
    convert_to_yolo(stage, data, image_dir=new_image_dir, save_dir=save_dir)
    convert_to_coco(stage, data, image_dir=new_image_dir, save_dir=save_dir)

# %%
image_dir

# %%
tmp = [{'id': 1, 'name': 'insu', 'supercategory': 'none'}, {'id': 2, 'name': "insu{'shell': 'Broken'}", 'supercategory': 'none'}, {'id': 3, 'name': 'insu-str-', 'supercategory': 'none'}, {'id': 4, 'name': "insu{'glaze': 'Flashover damage'}", 'supercategory': 'none'}]

# %%
tmp


# %%
[value['name'] for value in tmp]

# %%



