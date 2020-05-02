from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import cv2
import numpy as np
from PIL import Image
import os
import base64
import math


from .forms import *
from .models import *
from . import LsbSteg
script_dir = os.path.dirname(os.path.abspath(__file__))
imageFilename = "new.jpeg"
row=0
column=0
key="abcdefghijkl"
partition=1000


# Create your views here.
def home(request): 
    if request.method == 'POST': 
        form = HotelForm(request.POST, request.FILES) 
  
        if form.is_valid():
        	request.POST
        	img=form.save()
        	basewidth = 400
        	imgg = Image.open(os.path.join(script_dir,img.image.name))
        	wpercent = (basewidth/float(imgg.size[0]))
        	hsize = int((float(imgg.size[1])*float(wpercent)))
        	imgg = imgg.resize((basewidth,hsize), Image.ANTIALIAS)
        	imgg.save(os.path.join(script_dir,img.image.name))
        	global key
        	key=img.key
        	return render(request, 'myapp/add_image.html', {'img' : img}) 
        else:
        	return HttpResponse('Uploading Faied') 
    else: 
        form = HotelForm()
        return render(request, 'myapp/home.html', {'form' : form}) 


def apply_lsb(request):
	obj=Hotel.objects.latest('pk')
	global imageFilename
	imageFilename=obj.image.name
	LsbSteg.encodeLSB(obj.message,imageFilename,"lsb_encoded")
	return render(request, 'myapp/apply_lsb.html',{'img' : obj}) 

def convert_to_binary(request):
	obj=Hotel.objects.latest('pk')
	global imageFilename
	imageFilename=obj.image.name
	s=getBinary(imageFilename)
	vector=[]
	temp=""
	for i in range (0,min(2500,len(s))):
		if i%100==0 and i!=0:
			vector.append(temp)
			temp=""
		temp+=s[i]
	print (vector)
	return render(request, 'myapp/convert_to_binary.html',{'s' : vector}) 

def apply_partitioning(request):

	binary_key=''.join(format(ord(i), 'b') for i in key)
	global partition
	partition=binaryToDecimal(binary_key[:11])
	print (partition)

	obj=Hotel.objects.latest('pk')
	global imageFilename
	imageFilename=obj.image.name
	s=getBinary(imageFilename)
	vector=partitioning(partition,imageFilename,s)
	dic={}
	dic["part"]=vector[0]
	dic["no"]=vector[1]
	return render(request, 'myapp/apply_partitioning.html',{'dic':dic})

def perform_zigzag(request):
	obj=Hotel.objects.latest('pk')
	global imageFilename
	imageFilename=obj.image.name
	print(imageFilename)
	s=getBinary(imageFilename)
	s=zigzag(partition,s)
	vector=[]
	temp=""
	for i in range (0,min(2500,len(s))):
		if i%100==0 and i!=0:
			vector.append(temp)
			temp=""
		temp+=s[i]
	print (vector)
	return render(request, 'myapp/perform_zigzag.html',{'s' : vector})

def perform_swapping(request):
    binary_key=''.join(format(ord(i), 'b') for i in key) 
    dicti=swaps(binary_key)
    print(dicti)
    return render(request, 'myapp/perform_swapping.html',{'s' : dicti})
  
  
def final_encrypted_image(request):
    obj=Hotel.objects.latest('pk')
    key=obj.key
    global imageFilename
    imageFilename=obj.image.name
    s=getBinary(imageFilename)
    s=zigzag(1000,s)
    finalFilename=LsbSteg.new_image(s,imageFilename)
    script_dirr="images"
    finalFilename=os.path.join(script_dirr,finalFilename)
    final=Final()
    final.image=finalFilename
    final.save()
    print(final)
    print(final.image.url)
    return render(request, 'myapp/final_encrypted_image.html',{'img':final, 'key':key})

def decrypt(request):
    obj=Hotel.objects.latest('pk')
    return render(request, 'myapp/decrypt.html',{'img':obj})

def binaryToDecimal(n): 
    return int(n,2) 


def encode():
	message = "This is a hidden text in an image"
	imageFilename = "new.jpeg"
	newImageFilename = "stego_stars_background"

	newImg = LsbSteg.encodeLSB(message, imageFilename, newImageFilename)
	if not newImg is None:
	        print("Stego image created.")

def getBinary(imageFilename):
	binary=LsbSteg.getBinary(imageFilename)
	s=""
	global row 
	row= len(binary)
	global column
	column =len(binary[0])
	print ("row: "+ str(row))
	print ("column: "+ str(column))

	for i in range(len(binary)):
		for j in range(len(binary[i])):
			s+=binary[i][j]
	return s

def partitioning(no_of_partition,imageFilename,s):
	print (len(s))
	print ("Number of partitions: ")
	print(no_of_partition)
	print("Size of each parition: ")
	print((int)(len(s)/no_of_partition))
	vector=[]
	vector.append(no_of_partition)
	vector.append((int)(len(s)/no_of_partition))
	return vector

def zigzag(no_of_partition,s):
	i=1
	temp=""
	cnt=True
	vector=[]
	size=math.ceil(len(s)/no_of_partition)
	for j in range(0,len(s)):
		if j%size==0 and j!=0:
			print("Partition "+ str(i) +": "+temp)
			vector.append(temp)
			temp=""
			i=i+1
		
		if cnt==True:
			cnt=False
			temp=temp+s[j]
			
		else:
			cnt=True
			temp = s[j]+temp
	vector.append(temp)
	s=""
	for i in range(0,len(vector)):
		for j in range(0,len(vector[i])):
			s+=vector[i][j]
	return s


def swaps(key):
	vector=[]
	temp=""
	print(len(key))
	for i in range(12,len(key)):
		if i%12==0 and i!=12:
			vector.append(binaryToDecimal(temp))
			temp=""
		temp+=key[i]

	j=1
	dicti={}
	for i in range(len(vector)):
		print("Partition "+str(j)+ " is swapped with Partition: " + str(vector[i]) + "\n")
		dicti[str(j)]=str(vector[i])
		j=j+1
	return dicti


