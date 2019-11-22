from PIL import Image, ImageFilter, ImageEnhance, ImageFile
import os,sys
import pytesseract
import argparse
import re 
import datefinder as df
ImageFile.LOAD_TRUNCATED_IMAGES = True

def split_check(lst,sym):
	x = []
	y = []
	if(len(lst)>0):
		for i in range(len(lst)):
			z = lst[i]
			slst = lst[i].split(sym)
			#print(slst)
			s1 = int(slst[0])
			s2 = int(slst[2])
			#print(s1,",",s2)
			#print(s2<=2019)
			#print(z)
			if(s1<=31 and s2<=2050 and s2>1900):
				x.append(z)
	if(len(x)>0):
		return x
	else:
		return y
		
def Arrange_Date(lst):
	date = ""
	if(len(lst)>0):
		z = str(lst[0])
		y = z.split("'")
		y1 = y[0]
		year = y[1]
		mon = ""
		for i in y1:
			if(i.isdigit()):
				date+=i
			else:
				mon+=i
				
		date = [date+mon+year]
	return date
	
def valid_Date(lst):
	xx = []
	xy = []
	if(len(lst)>0):
		for i in range(len(lst)):
			z = str(lst[i])
			xdf = df.find_dates(z)
			x = ""
			for j in xdf:
				xx.append(j)
			for k in xx:
				x = str(k)
				x = x.split(" ")
				x = x[0]
				xy.append(x)
	return xy
			
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

def listToString(li):
	s = ""
	for i in li:
		s = s + i +" "
	return s

#regular expressions for finding date pattern
def patternREGEX(line):
	patternsFound=[]
	xPattern_1 = re.findall("\d{4}\,\w+\s\d{2}",line)
	xPattern_2 = re.findall("\w{3}\d{1,2}\'\d{2}",line)
	xPattern_3 = re.findall("\w+\s\d{2}\,\d{4}",line)
	xPattern_4 = re.findall("\d{2}\.\w+\.\d{4}",line)
	xPattern_5 = re.findall("\d{2}-\w+-\d{4}",line)
	xPattern_6 = re.findall("\d+/\w+/\d+",line)
	xPattern_7 = re.findall("\d{2}\s\w{3}\s\d{4}",line)
	xPattern_8 = re.findall("\w{3}\s\d{2}\s\d{4}",line)
	xPattern_9 = re.findall("\d{2}-\w{3}\d{2}",line)
	xPattern_10 = re.findall("\d{2}\w{3}\s\d{4}",line)
	xPattern_11 = re.findall("\w+\s\d{2}\,\s\d{4}",line)

	Pattern_1 = listToString(Remove(xPattern_1))
	Pattern_2 = listToString(Remove(valid_Date(Arrange_Date(Remove(xPattern_2)))))
	Pattern_3 = listToString(Remove(valid_Date(Remove(xPattern_3))))
	#Pattern_4 = listToString(Remove(valid_Date(split_check(Remove(xPattern_4),"."))))
	Pattern_4 = listToString(Remove(valid_Date(Remove(xPattern_4))))
	#Pattern_5 = listToString(Remove(valid_Date(split_check(Remove(xPattern_5),"-"))))
	Pattern_5 = listToString(Remove(valid_Date(Remove(xPattern_5))))
	#Pattern_6 = listToString(Remove(valid_Date(split_check(Remove(xPattern_6),"/"))))
	Pattern_6 = listToString(Remove(valid_Date(Remove(xPattern_6))))
	Pattern_7 = listToString(Remove(valid_Date(Remove(xPattern_7))))
	Pattern_8 = listToString(Remove(valid_Date(Remove(xPattern_8))))
	Pattern_9 = listToString(Remove(valid_Date(Remove(xPattern_9))))
	Pattern_10 = listToString(Remove(valid_Date(Remove(xPattern_10))))
	Pattern_11 = listToString(Remove(valid_Date(Remove(xPattern_11))))

	if(len(Pattern_1)>0):
		patternsFound.append(Pattern_1)
	if(len(Pattern_2)>0):
		patternsFound.append(Pattern_2)
	if(len(Pattern_3)>0):
		patternsFound.append(Pattern_3)
	if(len(Pattern_4)>0):
		patternsFound.append(Pattern_4)
	if(len(Pattern_5)>0):
		patternsFound.append(Pattern_5)
	if(len(Pattern_6)>0):
		patternsFound.append(Pattern_6)
	if(len(Pattern_7)>0):
		patternsFound.append(Pattern_7)
	if(len(Pattern_8)>0):
		patternsFound.append(Pattern_8)
	if(len(Pattern_9)>0):
		patternsFound.append(Pattern_9)
	if(len(Pattern_10)>0):
		patternsFound.append(Pattern_10)
	if(len(Pattern_11)>0):
		patternsFound.append(Pattern_11)
	
	return patternsFound

def printFound(patternsFound,x):
	print("Recognized text from image :" , x)
	print("Dates found in image are:",patternsFound)
	
def reCheck(y):
	#y = ImageEnhance.Color(y)
	#y = y.enhance(0.0)
	#y = y.filter(ImageFilter.FIND_EDGES)
	#y.show()
	y = ImageEnhance.Sharpness(y) 
	y = y.enhance(2.0)
	#y.show()
	x = pytesseract.image_to_string(y)
	patternsFound = patternREGEX(x)	
	print("---Re-Checking---")
	if(len(patternsFound)>0):
		printFound(patternsFound,x)
	else:
		print("Extracted Text is :",x)
		print("No dates Found")

def image_Enhance(y1):
	black = (0,0,0)
	white = (255,255,255)
	threshold = (160,160,160)

	# Open input image in grayscale mode and get its pixels.
	img = y1.convert("LA")
	pixels = img.getdata()
	newPixels = []

	# Compare each pixel 
	for pixel in pixels:
		if pixel < threshold:
			newPixels.append(black)
		else:
			newPixels.append(white)
	
	# Create and save new image.
	newImg = Image.new("RGB",img.size)
	newImg.putdata(newPixels)
	return newImg
	#newImg.save("newImage.jpg")
def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,help="path to input image to be OCR'd")
	args = vars(ap.parse_args())
	y = Image.open(args["image"])
	y1 = Image.open(args["image"])
	y1 = image_Enhance(y1)
	#y2.show()
	#y = y.filter(ImageFilter.EDGE_ENHANCE)
	#y = y.filter(ImageFilter.CONTOUR) 
	#y = y.filter(ImageFilter.EMBOSS) 
	y = y.filter(ImageFilter.DETAIL)
	#y.show()
	x = pytesseract.image_to_string(y)
	patternsFound = patternREGEX(x)
	if(len(patternsFound)>0):
		printFound(patternsFound,x)
	else:
		reCheck(y)
if __name__== "__main__":
  main()
		