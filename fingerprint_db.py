import os
path = "/home/nacho/Documents/fingerprint/proyecto_fingerprint"
os.chdir(path)
print(os.getcwd())
#%%
from db import DBCLIENT
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image
import io
import urllib.request
import cv2
import numpy as np
from numpy import savez_compressed
from imgaug import augmenters as iaa
#%%
def my_ip():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print(external_ip)
    return external_ip
my_ip()

#me conecto al objeto mysql con el arhivo db.py
con = DBCLIENT()
#creo un objeto pymysqldb
db = con.db_connection()
#cur = db.cursor()
#cur.execute("set global max_allowed_packet = 67108864;")

#querys
query = "SELECT id FROM DMA_CESP_PRD"
no_data = pd.read_sql_query(query, db)
print(len(no_data))
imgs = np.zeros((len(range(1, 1002)), 90, 90),dtype=np.uint8)
labels = np.zeros((len(range(1, 1002)), 2),dtype=np.uint16)

for i in range(1, 1002):
    query = 'select * from DMA_CESP_PRD where id = '+str(i)+';'
    data = pd.read_sql_query(query, db)
    #extraer huella
    data_fingerprint = data.iloc[0]['HUELLA']
    img = Image.open(io.BytesIO(data_fingerprint))
    img.save('huella.png')
    imgcv2 = cv2.imread('huella.png', cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(imgcv2, (90, 90))
    imgs[[i-1]] = img
    #extraer label
    gender = data['SEX'].values[0] = 0 if data['SEX'].values[0] == 'M' else 1
    label = np.array([int(data['PERSONID']), gender],dtype=np.uint16)
    labels[[i-1]] = label
    
savez_compressed('dataset/X_imgs.npz', imgs)
np.save('dataset/y_labels.npy', labels)

plt.title(labels[-1])
plt.imshow(imgs[-1], cmap='gray')

#cerrar conexion
con.close()
#%%
x_data = np.load('dataset/X_imgs.npz')['arr_0']
#%% Preview Augmentation
seq = iaa.Sequential([
    # blur images with a sigma of 0 to 0.5
    #iaa.GaussianBlur(sigma=(0, 0.5)),
    iaa.Affine(
        # scale images to 90-110% of their size, individually per axis
        #scale={"x": (0.9, 1.1), "y": (0.9, 1.1)},
        # translate by -10 to +10 percent (per axis)
        #translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)},
        # rotate by -30 to +30 degrees
        rotate=(-30, 30),
        # use nearest neighbour or bilinear interpolation (fast)
        order=[0, 1],
        # if mode is constant, use a cval between 0 and 255
        cval=255
    )
], random_order=True)

augs = [x_data] * 3   
augs1 = seq.augment_images(augs[0])   
augs2 = seq.augment_images(augs[1])  
augs3 = seq.augment_images(augs[2])
savez_compressed('dataset/X_augs1.npz', augs1)  
savez_compressed('dataset/X_augs2.npz', augs2)  
savez_compressed('dataset/X_augs3.npz', augs3)  

i = 10
plt.figure(figsize=(16, 6))
plt.subplot(2, 5, 1)
plt.title('original')
plt.imshow(x_data[i].squeeze(), cmap='gray')
plt.subplot(2, 5, 2)
plt.title('aug1')
plt.imshow(augs1[i].squeeze(), cmap='gray')
plt.subplot(2, 5, 3)
plt.title('aug2')
plt.imshow(augs2[i].squeeze(), cmap='gray')
plt.subplot(2, 5, 4)
plt.title('aug3')
plt.imshow(augs3[i].squeeze(), cmap='gray')
