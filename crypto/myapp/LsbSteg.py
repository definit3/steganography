from PIL import Image
import os
import numpy

bitsPerChar = 8
bitsPerPixel = 3
maxBitStuffing = 2
extension = "png"
row=0
column=0
script_dir = os.path.dirname(os.path.abspath(__file__))
def getsize(imageFilename):
       script_dir = os.path.dirname(os.path.abspath(__file__))
       img= Image.open(os.path.join(script_dir, imageFilename))
       return img.size

def new_image(s,imageFilename):
       vector=[]
       j=0
       binary=getBinary(imageFilename)
       # print(binary)
       global row 
       row= len(binary)
       global column
       column =len(binary[0])
       size=getsize(imageFilename)
       print("str len: " + str(len(s)))
       for i in range (0,row):
              temp=[1,2,3]
              temp[0]=s[j:j+8]
              j=j+8
              temp[1]=s[j:j+8]
              j=j+8
              temp[2]=s[j:j+8]
              j=j+8
              vector.append(temp)
       print (vector)
       newPixels = [tuple(int(p,2) for p in pixel) for pixel in vector]
       newImg = Image.new("RGB", size)
       newImg.putdata(newPixels)
       newImageFilename="temp"
       extension="jpeg"
       finalFilename = ".".join([newImageFilename,extension])
       script_dirr=os.path.join(script_dir,"images")
       newImg.save(os.path.join(script_dirr, finalFilename))
       return finalFilename

def getBinary(imageFilename):
       
       img= Image.open(os.path.join(script_dir, imageFilename))
       size = img.size
       pixels = list(img.getdata())
       binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
       return binaryPixels

def canEncode(message, image):
       width, height = image.size
       imageCapacity = width * height * bitsPerPixel
       messageCapacity = (len(message) * bitsPerChar) - (bitsPerChar + maxBitStuffing)
       return imageCapacity >= messageCapacity

def createBinaryTriplePairs(message):
       binaries = list("".join([bin(ord(i))[2:].rjust(bitsPerChar,'0') for i in message]) + "".join(['0'] * bitsPerChar))
       binaries = binaries + ['0'] * (len(binaries) % bitsPerPixel)
       binaries = [binaries[i*bitsPerPixel:i*bitsPerPixel+bitsPerPixel] for i in range(0,int(len(binaries) / bitsPerPixel))]
       return binaries

def embedBitsToPixels(binaryTriplePairs, pixels):
       binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
       # print(binaryPixels)
       count=0
       for i in range(len(binaryTriplePairs)):
              for j in range(len(binaryTriplePairs[i])):
                     binaryPixels[i][j] = list(binaryPixels[i][j])
                     binaryPixels[i][j][-1] = binaryTriplePairs[i][j]
                     binaryPixels[i][j] = "".join(binaryPixels[i][j])

       newPixels = [tuple(int(p,2) for p in pixel) for pixel in binaryPixels]
       return newPixels

def encodeLSB(message, imageFilename, newImageFilename):
       script_dir = os.path.dirname(os.path.abspath(__file__))
       img= Image.open(os.path.join(script_dir, imageFilename))
       # img = Image.open(imageFilename)
       size = img.size

       if not canEncode(message, img):
              return None

       binaryTriplePairs = createBinaryTriplePairs(message)

       # print("binaryTriplePairs: ")
       # print(binaryTriplePairs)


       pixels = list(img.getdata())
       # print(numpy.asarray(img))
       # print(pixels)
       newPixels = embedBitsToPixels(binaryTriplePairs, pixels)

       newImg = Image.new("RGB", size)
       newImg.putdata(newPixels)

       finalFilename = ".".join([newImageFilename,extension])
       newImg.save(os.path.join(script_dir, finalFilename))

       return newImg

def getLSBsFromPixels(binaryPixels):
       totalZeros = 0
       binList = []
       for binaryPixel in binaryPixels:
              for p in binaryPixel:
                     if p[-1] == '0':
                            totalZeros = totalZeros + 1
                     else:
                            totalZeros = 0
                     binList.append(p[-1])
                     if totalZeros == bitsPerChar:
                            return  binList

def decodeLSB(imageFilename):
       img = Image.open(imageFilename)
       pixels = list(img.getdata())
       binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
       binList = getLSBsFromPixels(binaryPixels)
       message = "".join([chr(int("".join(binList[i:i+bitsPerChar]),2)) for i in range(0,len(binList)-bitsPerChar,bitsPerChar)])
       return message