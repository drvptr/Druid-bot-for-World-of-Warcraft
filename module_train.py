import torch
from torch.utils.data import DataLoader
from torchvision import models, transforms
from module_data import WoWDataset
import torch.optim as optim

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def collate_fn(batch):
    images, boxes = zip(*batch)
    
    max_boxes = max(len(box) for box in boxes) 
    

    padded_boxes = []
    for box in boxes:
        if len(box) < max_boxes:
            padding = torch.zeros((max_boxes - len(box), 4))
            padded_boxes.append(torch.cat([box, padding], dim=0))
        else:
            padded_boxes.append(box)
    
    return torch.stack(images, 0), torch.stack(padded_boxes, 0)

dataset = WoWDataset('dataset/images', 'dataset/labels', transform=transform)
data_loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=collate_fn)

model = models.detection.fasterrcnn_resnet50_fpn(weights="FasterRCNN_ResNet50_FPN_Weights.COCO_V1")

optimizer = optim.Adam(model.parameters(), lr=0.0001)

for epoch in range(10):
    model.train() 
    for images, boxes in data_loader:
        optimizer.zero_grad()

        targets = []
        for box in boxes:
            if box.numel() == 0 or box.dim() != 2 or box.shape[1] != 4:
                targets.append({"boxes": torch.zeros((0, 4)), "labels": torch.zeros((0,), dtype=torch.int64)})
                continue  

            valid_boxes = box[(box[:, 2] > box[:, 0]) & (box[:, 3] > box[:, 1])]

            if valid_boxes.numel() == 0:
                targets.append({"boxes": torch.zeros((0, 4)), "labels": torch.zeros((0,), dtype=torch.int64)})
            else:
                targets.append({"boxes": valid_boxes, "labels": torch.ones((valid_boxes.shape[0],), dtype=torch.int64)}) 

        loss_dict = model(images, targets)
        
        losses = sum(loss for loss in loss_dict.values())
        
        losses.backward()
        optimizer.step()
    
    print(f"Epoch {epoch}, Loss: {losses.item()}")

torch.save(model.state_dict(), 'fasterrcnn.pth')
