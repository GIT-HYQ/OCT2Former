from torch.utils.data import Dataset
import csv
from .transform import *
from utils.loss import  class2one_hot, one_hot2dist
import pandas as pd


class myDataset(Dataset): 
    def __init__(self, data_root, target_root, crop_size, data_mode, k_fold=None, imagefile_csv=None, num_fold=None, data_root_aux=None, img_aug=False):
        self.crop_size = crop_size  # h, w
        self.data_root = data_root
        self.target_root = target_root
        self.data_mode = data_mode
        self.img_aug = img_aug

        if data_mode=='train':
            self.transforms = get_transforms_train_OCTA_SS()
        else:
            self.transforms = get_transforms_valid()

        data_path = data_root
        if data_mode=="train":
            self.name_list = sorted(os.listdir(data_path + '/images/training/'))
            self.label_list = sorted(os.listdir(data_path + '/annotations/training/'))
            self.data = []
            for i in range(len(self.name_list)):
                img_path = data_path + '/images/training/' + self.name_list[i]
                mask_path = data_path + '/annotations/training/' + self.label_list[i]
                self.data.append([img_path, mask_path])
        elif data_mode=="val":
            self.name_list = sorted(os.listdir(data_path + '/images/validation/'))
            self.label_list = sorted(os.listdir(data_path + '/annotations/validation/'))
            self.data = []
            for i in range(len(self.name_list)):
                img_path = data_path + '/images/validation/' + self.name_list[i]
                mask_path = data_path + '/annotations/validation/' + self.label_list[i]
                self.data.append([img_path, mask_path])
        elif data_mode=="test":
            self.name_list = sorted(os.listdir(data_path + '/images/test/'))
            self.label_list = sorted(os.listdir(data_path + '/annotations/test/'))
            self.data = []
            for i in range(len(self.name_list)):
                img_path = data_path + '/images/test/' + self.name_list[i]
                mask_path = data_path + '/annotations/test/' + self.label_list[i]
                self.data.append([img_path, mask_path])
        else:
            print("Error, invalid split type")

        print(f"{data_mode} dataset: {len(self.name_list)}")

    def __len__(self):  
        return len(self.name_list)

    def __getitem__(self, index): 

        index = index % len(self.name_list)
        name = self.name_list[index]
        image_path, label_path = self.data[index]

        image, label = fetch(image_path, label_path)  

        if self.data_mode == "train" and self.img_aug == True:
            image_aug = self.transforms(image=image.astype(np.uint8), mask=label.astype(np.uint8))
            image = image_aug['image']
            label = image_aug['mask']#.unsqueeze(0)

        image, label = convert_to_tensor(image, label)
        
        # label = (label == 255).float()

        #image, label = resize(self.crop_size, image, label)

        label = label.squeeze()
        # print(name)
        return {
            "image": image,
            "label": label,
            "file": name}

# class myDataset(Dataset): 
#     def __init__(self, data_root, target_root, crop_size, data_mode, k_fold=None, imagefile_csv=None, num_fold=None, data_root_aux=None, img_aug=False):
#         self.crop_size = crop_size  # h, w
#         self.data_root = data_root
#         self.target_root = target_root
#         self.data_mode = data_mode
#         self.img_aug = img_aug

#         if data_mode=='train':
#             self.transforms = get_transforms_train_OCTA_SS()
#         else:
#             self.transforms = get_transforms_valid()

#         image_files = pd.read_csv(imagefile_csv, header=None).squeeze().tolist()

#         if data_mode == "train":
#             self.image_files = image_files[0: 27]
#         elif data_mode == "val" :
#             self.image_files = image_files[27: 30]
#         else:
#             self.image_files = image_files[30: 55]

#         print(f"{data_mode} dataset: {len(self.image_files)}")

#     def __len__(self):  
#         return len(self.image_files)

#     def __getitem__(self, idx): 
#         file = self.image_files[idx]
#         file_name = os.path.splitext(file)[0]

#         image_path = os.path.join(self.data_root, str(file))
#         label_path = os.path.join(self.target_root, file_name) + '.png'

#         image, label = fetch(image_path, label_path)  

#         if self.data_mode == "train" and self.img_aug == True:
#             image_aug = self.transforms(image=image.astype(np.uint8), mask=label.astype(np.uint8))
#             image = image_aug['image']
#             label = image_aug['mask']#.unsqueeze(0)

#         image, label = convert_to_tensor(image, label)
        
#         label = (label == 255).float()

#         #image, label = resize(self.crop_size, image, label)

#         label = label.squeeze()

#         return {
#             "image": image,
#             "label": label,
#             "file": file}