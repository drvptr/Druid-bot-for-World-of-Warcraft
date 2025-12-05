import Xlib
import Xlib.display
import torch
import numpy as np
from torchvision import models, transforms
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

model = models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
model.load_state_dict(torch.load('fasterrcnn.pth'))
model.eval()


disp = Xlib.display.Display()
root = disp.screen().root

# Ищем окно WoW
wow_window = None
for window in root.query_tree().children:
    wm_name = window.get_wm_name()
    if wm_name and "World of Warcraft" in wm_name:
        wow_window = window
        break

if not wow_window:
    print("win does not found")
    exit(1)


geom = wow_window.get_geometry()
x, y, width, height = geom.x, geom.y, geom.width, geom.height


transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])

while True:
    raw = wow_window.get_image(0, 0, width, height, Xlib.X.ZPixmap, 0xffffffff)
    img = np.frombuffer(raw.data, dtype=np.uint8).reshape((height, width, 4))

    img_tensor = transform(img[:, :, :3])
    img_tensor = img_tensor.unsqueeze(0)


    with torch.no_grad():  
        predictions = model(img_tensor)

    print(predictions)

    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)

    if len(predictions[0]['boxes']) > 0:
        for element in range(len(predictions[0]['boxes'])):
            box = predictions[0]['boxes'][element].cpu().numpy()
            score = predictions[0]['scores'][element].cpu().numpy()
            if score > 0.5: 
                draw.rectangle([tuple(box[:2]), tuple(box[2:])], outline="red", width=3)

    plt.imshow(pil_img)
    plt.axis('off') 
    plt.show()

    plt.pause(0.1)
