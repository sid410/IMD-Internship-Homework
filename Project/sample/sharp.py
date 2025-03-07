#from numba import jit
import cv2
from matplotlib import pyplot as plt
import numpy as np

def getStdThrsh(img, Blocksize):
    stds = []
    for y in range( 0, img.shape[0], Blocksize ):
        for x in range( 0, img.shape[1], Blocksize ):
            pimg = img[y:y+Blocksize, x:x+Blocksize]
            std = np.std( pimg )
            minv = np.min( pimg )
            maxv = np.max( pimg )
            stds.append(std)

    hist = np.histogram( stds, bins=64 )
    peaki = np.argmax(hist[0])   

    #plt.hist( stds, bins=64 )
    #plt.show()

    slim = 6.0
    for n in range(peaki,len(hist[0])-1):
        if hist[0][n] < hist[0][n+1]:
            slim = hist[1][n+1]
            break

    #if slim > 6.0:
    #    slim = 6.0
    
    return slim

def getBWThrsh(img):
    med = np.median(img)
    fild = img[img < med]
    return np.median(fild)

# def getWbias( img, bwthr ):
#     wimg = img[ img > bwthr ]
#     hist = np.histogram( wimg, bins=16 )
#     agm = np.argmax(hist[0])
#     return hist[1][agm]


def sharpenImg(imgfile):
    Blocksize = 8
    Testimagefile = imgfile

    with open(Testimagefile, mode='rb') as f:
        fdata =f.read()
        inp = np.frombuffer(fdata, dtype = 'uint8')
        bookimg = cv2.imdecode(inp, cv2.IMREAD_UNCHANGED)

    img_gray = cv2.cvtColor(bookimg, cv2.COLOR_BGR2GRAY)

    print( "width", img_gray.shape[1], "height", img_gray.shape[0] )

    slim = getStdThrsh(img_gray, Blocksize)*0.8
    outimage32 = sharpenMem( img_gray, slim, Blocksize, 8 )
    #cv2.imwrite("outimage32g.png", outimage32)
    
    img_gray = cv2.cvtColor(bookimg, cv2.COLOR_BGR2GRAY)
    outimage00 = sharpenMem( img_gray, slim, Blocksize, 0 )
    #cv2.imwrite("outimage00g.png", outimage00)

    outimage = cv2.addWeighted(outimage00, 0.5, outimage32, 0.5, 0)

    cv2.imshow("results",outimage)
    cv2.waitKey(0)

    return 

def neardevi(imgbl):
    d = 0.0
    for y in range(imgbl.shape[0]):
        for x in range(1, imgbl.shape[1] ):
            d = d + (imgbl[y][x-1]-imgbl[y][x])*(imgbl[y][x-1]-imgbl[y][x])
    d = d / (imgbl.shape[0]*imgbl.shape[1])
    return d        

#@jit
def sharpenMem(img_gray, slim, Blocksize, bias):

    bimgl = np.zeros([Blocksize,int(bias)]) + 255

    h = int((img_gray.shape[0] - bias) / Blocksize )*Blocksize
    d = img_gray.shape[0] - h -bias

    bimgle = np.zeros([d,int(bias)]) + 255
    bimgu = np.zeros([int(bias),img_gray.shape[1]]) + 255

    yimgs=[]
    yimgs.append(bimgu)

    for y in range( bias, img_gray.shape[0], Blocksize ):
        s = ""

        ximgs=[]
        if y+Blocksize > img_gray.shape[0]:
            ximgs.append(bimgle)
        else:
            ximgs.append(bimgl)

        for x in range( bias, img_gray.shape[1]-Blocksize, Blocksize ):
            pimg = img_gray[y:y+Blocksize, x:x+Blocksize]
            std = np.std( pimg )
            if std < slim:
                s = s + "_"
                ximg=np.zeros(pimg.shape) + 255
            else:
                s = s + "#"
                lut = np.zeros(256)
                white = int(np.median(pimg))
                black = int(white * 2 / 3)
                cnt = int(white - black)
                for n in range(cnt):
                    lut[black+n]=( int(256 * n / cnt) )
                for n in range(white,256):
                    lut[n]=(255)
                ximg=cv2.LUT(pimg,lut)

            ximgs.append(ximg)

        if img_gray.shape[1] > x+Blocksize:
            bimgr = np.zeros([ximg.shape[0],int(img_gray.shape[1] - x-Blocksize)]) + 255
            ximgs.append(bimgr)

        yimgs.append( cv2.hconcat( ximgs ) )
        print( "{:4d} {:s}".format( y, s ) )

    if img_gray.shape[0] > y+Blocksize:
        bimgd = np.zeros([int(img_gray.shape[0] - y - Blocksize),img_gray.shape[1]]) + 255
        yimgs.append(bimgd)

    outimage = cv2.vconcat(yimgs)

    return outimage

if __name__ =='__main__':
    sharpenImg("Project/Resources/sample.png")