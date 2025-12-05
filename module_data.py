# module_data.py
import os
import xml.etree.ElementTree as ET
from torch.utils.data import Dataset
from PIL import Image
import torch

class WoWDataset(Dataset):
    def __init__(self, images_dir, labels_dir, transform=None):
        self.images_dir = images_dir
        self.labels_dir = labels_dir
        self.transform = transform
        self.image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
        
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.images_dir, img_name)
        label_path = os.path.join(self.labels_dir, img_name.replace('.jpg', '.xml'))
        
        image = Image.open(img_path).convert("RGB")
        
        # Parse
        tree = ET.parse(label_path)
        root = tree.getroot()
        
        boxes = []
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            boxes.append([xmin, ymin, xmax, ymax])
        
        boxes = torch.tensor(boxes, dtype=torch.float32)
        
        if self.transform:
            image = self.transform(image)
        
        return image, boxes
