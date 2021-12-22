import utils
import pandas as pd
import numpy as np
from PIL import Image
from plyfile import PlyData, PlyElement


def pfm2ply(immagine, molt):
    ottico = Image.open(immagine + '.jpg')
    ottico = ottico.convert('RGB')
    (data, scale) = utils.read_pfm(immagine + '.pfm')
    df = pd.DataFrame(data)

    x = np.zeros(ottico.width * ottico.height)
    y = np.zeros(ottico.width * ottico.height)
    z = np.zeros(ottico.width * ottico.height)
    red = np.zeros(ottico.width * ottico.height)
    green = np.zeros(ottico.width * ottico.height)
    blue = np.zeros(ottico.width * ottico.height)
    posizione = 0

    # with open(immagine+'_elaborata.txt', 'w') as f:
    for j in range(1, ottico.width):
        for k in range(1, ottico.height):
            RGB = ottico.getpixel((ottico.width - j, ottico.height - k))
            # stringa = str(k)+';'+str(j)+';'+str(df.values[k,j]*molt)
            # stringa = stringa + ';'+str(RGB[0])+';'+str(RGB[1])+';'+str(RGB[2])+'\n'
            x[posizione] = k
            y[posizione] = j
            z[posizione] = df.values[k, j] * molt
            red[posizione] = RGB[0]
            green[posizione] = RGB[1]
            blue[posizione] = RGB[2]
            posizione = posizione + 1
            # print(str(j)+'-'+str(k))
            # f.write(stringa)
    # f.close()
    # df.to_csv("quota.csv",sep=';',header=False,index=False)

    vertices = np.empty(ottico.width * ottico.height,
                        dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])
    vertices['x'] = x.astype('f4')
    vertices['y'] = y.astype('f4')
    vertices['z'] = z.astype('f4')
    vertices['red'] = red.astype('u1')
    vertices['green'] = green.astype('u1')
    vertices['blue'] = blue.astype('u1')

    # save as ply
    ply = PlyData([PlyElement.describe(vertices, 'vertex')], text=False)
    ply.write(immagine + ".ply")


if __name__ == '__main__':
    pfm2ply('/Users/lucainnocenti/drone/IMG_0928', 20)
