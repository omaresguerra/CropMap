from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ImageForm, CroppingForm, CroppingDataForm, UserForm, DataForm, CroppingDataDetailForm, ComparisonForm
from .models import Image, CroppingImage, CroppingData, Data, CroppingDataDetail, Comparison
from django.contrib import auth

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Image Add
def image_add(request):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.image_raw = request.FILES['image_raw']
            file_type = image.image_raw.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'image': image,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'cropmapapp/image_form.html', context)
            image.save()
            images = Image.objects.filter(user=request.user)
            return render(request, 'cropmapapp/index.html', {'images': images})
        context = {
            "form": form,
        }
        return render(request, 'cropmapapp/image_form.html', context)


# Image Delete
def image_delete(request, image_id):
    image = Image.objects.get(pk=image_id)
    image.delete()
    images = Image.objects.filter(user=request.user)
    return render(request, 'cropmapapp/index.html', {'images': images})


# Cropping Image
def cropping(request):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        images = CroppingImage.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            images = images.filter(
                Q(surveying_area__icontains=query) |
                Q(image_raw__icontains=query) |
                Q(address__icontains=query) |
                Q(land_description__icontains=query)
            ).distinct()
            return render(request, 'cropmapapp/cropping.html', {
                'images': images,
                'croppings': croppings,
            })
        else:
            return render(request, 'cropmapapp/cropping.html', {'images': images})


# Cropping Detail
def croppingdetail(request, image_id):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        user = request.user
        image = get_object_or_404(CroppingImage, pk=image_id)

        return render(request, 'cropmapapp/croppingdetail.html', {'image': image, 'user': user})



# Cropping Data Detail
def croppingdatadetail(request, data_id):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        user = request.user
        croppingdata = get_object_or_404(CroppingData, pk=data_id)
        return render(request, 'cropmapapp/croppingdatadetail.html', {'croppingdata': croppingdata, 'user': user})


# Compare
def compare(request, image_id):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        user = request.user
        image = get_object_or_404(CroppingImage, pk=image_id)

        compare = image.comparison_set.all()

        return render(request, 'cropmapapp/comparison.html', {'image': image, 'compare':compare, 'user': user})


# Print Compare
def print_comparison(request, image_id):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        user = request.user
        image = get_object_or_404(CroppingImage, pk=image_id)

        compare = image.comparison_set.all()

        return render(request, 'cropmapapp/print-comparison.html', {'image': image, 'compare':compare, 'user': user})


# Cropping Image Add
def cropping_add(request):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        form = CroppingForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.image_raw = request.FILES['image_raw']
            file_type = image.image_raw.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'image': image,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'cropmapapp/croppingimage_form.html', context)
            image.save()
            return render(request, 'cropmapapp/croppingdetail.html', {'image': image})
        context = {
            "form": form,
        }
        return render(request, 'cropmapapp/croppingimage_form.html', context)


# Cropping Image Add
def croppingdata_add(request, image_id):
    form = CroppingDataForm(request.POST or None, request.FILES or None)
    croppingimage = get_object_or_404(CroppingImage, pk=image_id)

    if form.is_valid():
        croppingdata = form.save(commit=False)
        croppingdata.image = croppingimage
        croppingdata.save()
        return render(request, 'cropmapapp/croppingdetail.html', {'image':croppingimage}) 
    context = {
        'image':croppingimage,
        'form':form,
    }
    return render(request, 'cropmapapp/croppingdata_form.html', context)


# Cropping Image Delete
def croppingimage_delete(request, image_id):
    cropping = CroppingImage.objects.get(pk=image_id)
    cropping.delete()
    cropping = CroppingImage.objects.filter(user=request.user)
    return render(request, 'cropmapapp/cropping.html', {'images': cropping})


# Cropping Data Delete
def croppingdata_delete(request, image_id, data_id):
    croppingimage = get_object_or_404(CroppingImage, pk=image_id)
    croppingdata = CroppingData.objects.get(pk=data_id)
    croppingdata.delete()

    compare = Comparison.objects.all()
    
    compare_data = ''
    
    for a in compare:
        if a.croppingdata == croppingdata.cropping:
            compare_data = a.croppingdata

    to_delete = Comparison.objects.filter(croppingdata=compare_data)
    to_delete.delete()

    return render(request, 'cropmapapp/croppingdetail.html', {'image': croppingimage})


# Index
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        images = Image.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            images = images.filter(
                Q(image_name__icontains=query) |
                Q(image_raw__icontains=query) |
                Q(image_description__icontains=query)
            ).distinct()
            return render(request, 'cropmapapp/index.html', {
                'images': images,
            })
        else:
            return render(request, 'cropmapapp/index.html', {'images': images})

# Home
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        return render(request, 'cropmapapp/home.html')


# About
def about(request):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        return render(request, 'cropmapapp/about.html')


# Image Data
def detail(request, image_id):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        user = request.user
        image = get_object_or_404(Image, pk=image_id)
        return render(request, 'cropmapapp/detail.html', {'image': image, 'user': user})

# Image Data
def print_data(request, image_id):
    if not request.user.is_authenticated:
        return render(request, 'cropmapapp/login.html')
    else:
        user = request.user
        image = get_object_or_404(Image, pk=image_id)
        return render(request, 'cropmapapp/print-data.html', {'image': image, 'user': user})


# Test_Algorithm
def test_algorithm(request, image_id):
    image = get_object_or_404(Image, pk=image_id)

    import cv2
    import numpy as np
    import tkinter as tk
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    import os
    import matplotlib.patches as mpathches

    np.seterr(divide = 'ignore', invalid = 'ignore')
    root = tk.Tk()
    # def retrieve_input():
    images = str(image.image_raw)
    print(images)
    # inputValue = textBox.get("1.0","end-1c")
    filename=os.path.basename('./media/' + images)
    img1 = cv2.imread('./media/' + filename)
    # legend = cv2.imread('./media/legend.jpg')

    #RESIZE
    resized_image = img1[0:512, 0:512]

    #CONVERT TO HSV
    hsvColor = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    hsvColor1 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    rgbColor = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    rgbColor1 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB) 
    rgbColor2 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB) 
    rgbColor3 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB) 


    #HOW BEAUTIFUL IS BEAUTIFUL
    #RED
    SOIL_MIN = np.array([160, 50, 200])
    SOIL_MAX = np.array([180, 145, 255])

    GRAY_MIN = np.array([0, 40, 25])
    GRAY_MAX = np.array([140, 280, 255])

    #NIR
    PINK_MIN = np.array([140, 100, 0])
    PINK_MAX = np.array([180, 255, 255])

    DARK_MIN = np.array([0, 85, 130])
    DARK_MAX = np.array([10, 255, 230])



    # Variables for Computing Percentage
    #NDVI
    ndvi_125 = 0
    ndvi_150 = 0
    ndvi_200 = 0
    ndvi_225 = 0
    ndvi_255 = 0
    ndvi_255_125 = 0
    ndvi_255_150 = 0
    ndvi_255_200 = 0
    ndvi_255_255 = 0
    ndvi_0_255 = 0

    #OSAVI
    osavi_125 = 0
    osavi_150 = 0
    osavi_200 = 0
    osavi_225 = 0
    osavi_255 = 0
    osavi_255_125 = 0
    osavi_255_150 = 0
    osavi_255_200 = 0
    osavi_255_255 = 0
    osavi_0_255 = 0



    #THE MATRIX GOES IN...
    for x in range(0, 512, 4):
        for y in range(0, 512, 4):

            fourbyfour = hsvColor[x:x + 4, y:y + 4]

            #BEAUTY RANGE
            dark = cv2.inRange(fourbyfour, DARK_MIN, DARK_MAX)
            pink = cv2.inRange(fourbyfour, PINK_MIN, PINK_MAX)
            gray = cv2.inRange(fourbyfour, GRAY_MIN, GRAY_MAX)
            soil = cv2.inRange(fourbyfour, SOIL_MIN, SOIL_MAX)

            #COUNT COLORS
            no_of_dark = cv2.countNonZero(dark)
            no_of_pink = cv2.countNonZero(pink)
            no_of_gray = cv2.countNonZero(gray)
            no_of_soil = cv2.countNonZero(soil)

            total_nir = no_of_dark + no_of_pink + no_of_soil
            total_vis = no_of_gray + no_of_soil

            try:
                ave_nir = float(total_nir / 16.0)
                ave_vis = float(total_vis / 16.0)
            except ZeroDivisionError:
                ave_nir = -1.0
                ave_vis = -1.0



            #THE NDVI FORMULA
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                ndvi = float(ave_nir - ave_vis) / float(ave_nir + ave_vis)   #Formula for NDVI                    
            except ZeroDivisionError:
                ndvi = 100
                        
            print("[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + "\t RED: " + str(ave_vis) + "\t\t" + str(ndvi))

            stat = ""
            stat = stat + "[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + " \t RED: " + str(ave_vis) + "\t\t" + str(ndvi) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_NDVI_statisticaldata.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()

                
            #CONDITIONS FOR NDVI
            if(ndvi == 1.0):
                rgbColor[x:x + 4, y:y + 4] = [0, 125, 0]
            elif (ndvi < 1.0 and ndvi >= 0.75):
                rgbColor[x:x + 4, y:y + 4] = [0, 150, 0]
            elif (ndvi < 0.75 and ndvi >= 0.50):
                rgbColor[x:x + 4, y:y + 4] = [0, 200, 0]
            elif (ndvi < 0.50 and ndvi >= 0.25):
                rgbColor[x:x + 4, y:y + 4] = [0, 225, 0]
            elif (ndvi < 0.25 and ndvi >= 0.00):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 0]
            elif (ndvi < 0.0 and ndvi >= -0.25):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 125]
            elif (ndvi < -0.25 and ndvi >= -0.50):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 150]
            elif (ndvi < -0.50 and ndvi >= -0.75):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 200]
            elif (ndvi < -0.75 and ndvi > -1.0):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 255]
            elif (ndvi == -1.0):
                rgbColor[x:x + 4, y:y + 4] = [0, 0, 255]
            elif (ndvi == 100):
                rgbColor[x:x + 4, y:y + 4] = [0, 0, 128]

               
            #THE OSAVI FORMULA
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                osavi = float(ave_nir - ave_vis) / float(ave_nir + ave_vis + 0.16)   #Formula for OSAVI
                osavi = float(("{0:.2f}".format(osavi)))
                if ave_nir == 0.0 and ave_vis == 0.0:
                    osavi = 100

            except ZeroDivisionError:
                osavi = 100
   
            print("[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + "\t RED: " + str(ave_vis) + "\t\t" + str(osavi))

            stat = ""
            stat = stat + "[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + " \t RED: " + str(ave_vis) + "\t\t" + str(osavi) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_OSAVI_statisticaldata.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()


            #CONDITIONS FOR OSAVI
            if (osavi == 1.0):
                rgbColor1[x:x + 4, y:y + 4] = [0, 125, 0]
            elif (osavi < 1.0 and osavi >= 0.75):
                rgbColor1[x:x + 4, y:y + 4] = [0, 150, 0]
            elif (osavi < 0.75 and osavi >= 0.50):
                rgbColor1[x:x + 4, y:y + 4] = [0, 200, 0]
            elif (osavi < 0.50 and osavi >= 0.25):
                rgbColor1[x:x + 4, y:y + 4] = [0, 225, 0]
            elif (osavi < 0.25 and osavi >= 0.00):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 0]
            elif (osavi < 0.0 and osavi >= -0.25):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 125]
            elif (osavi < -0.25 and osavi >= -0.50):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 150]
            elif (osavi < -0.50 and osavi >= -0.75):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 200]
            elif (osavi < -0.75 and osavi > -0.86):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 255]
            elif (osavi == -0.86):
                rgbColor1[x:x + 4, y:y + 4] = [0, 0, 255]
            elif (osavi == 100):
                rgbColor1[x:x + 4, y:y + 4] = [0, 0, 128]

        print("\n")


    #128 x 128 Matrix = 4 x 4 as a whole
    for x in range(0,512,128):
        for y in range(0,512,128):

            onetwoeight = hsvColor1[x:x + 128, y:y + 128]

            #BEAUTY RANGE
            dark1 = cv2.inRange(onetwoeight, DARK_MIN, DARK_MAX)
            pink1 = cv2.inRange(onetwoeight, PINK_MIN, PINK_MAX)
            gray1 = cv2.inRange(onetwoeight, GRAY_MIN, GRAY_MAX)
            soil1 = cv2.inRange(onetwoeight, SOIL_MIN, SOIL_MAX)

            #COUNT COLORS
            no_of_dark1 = cv2.countNonZero(dark1)
            no_of_pink1 = cv2.countNonZero(pink1)
            no_of_gray1 = cv2.countNonZero(gray1)
            no_of_soil1 = cv2.countNonZero(soil1)

            total_nir1 = no_of_dark1 + no_of_pink1 + no_of_soil1
            total_vis1 = no_of_gray1 + no_of_soil1

            try:
                ave_nir1 = float(total_nir1 / 16384.0) 
                ave_vis1 = float(total_vis1 / 16384.0) 
            except ZeroDivisionError:
                ave_nir1 = -1.0
                ave_vis1 = -1.0


            #THE NDVI FORMULA - 4 x 4
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                ndvi1 = float(ave_nir1 - ave_vis1) / float(ave_nir1 + ave_vis1)           #Formula for NDVI    
                ndvi1 = float(("{0:.2f}".format(ndvi1)))                
            except ZeroDivisionError:
                ndvi1 = 100
                        
            print("[" + str(x) + ":" + str(x + 128) + "," + str(y) + ":" + str(y + 128) + "] \t" + "NIR: " + str(ave_nir1) + "\t RED: " + str(ave_vis1) + "\t\t" + str(ndvi1))


            stat = ""
            stat = str(ndvi1) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_NDVI_4x4StatisticalData.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()

                
            #CONDITIONS FOR NDVI - 4 X 4 
            if(ndvi1 == 1.0):
                rgbColor2[x:x + 128, y:y + 128] = [0, 125, 0]
                ndvi_125 += 1
            elif (ndvi1 < 1.0 and ndvi1 >= 0.75):
                rgbColor2[x:x + 128, y:y + 128] = [0, 150, 0]
                ndvi_150 += 1
            elif (ndvi1 < 0.75 and ndvi1 >= 0.50):
                rgbColor2[x:x + 128, y:y + 128] = [0, 200, 0]
                ndvi_200 += 1
            elif (ndvi1 < 0.50 and ndvi1 >= 0.25):
                rgbColor2[x:x + 128, y:y + 128] = [0, 225, 0]
                ndvi_225 += 1
            elif (ndvi1 < 0.25 and ndvi1 >= 0.00):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 0]
                ndvi_255 += 1
            elif (ndvi1 < 0.0 and ndvi1 >= -0.25):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 125]
                ndvi_255_125 += 1
            elif (ndvi1 < -0.25 and ndvi1 >= -0.50):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 150]
                ndvi_255_150 += 1
            elif (ndvi1 < -0.50 and ndvi1 >= -0.75):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 200]
                ndvi_255_200 += 1
            elif (ndvi1 < -0.75 and ndvi1 > -1.0):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 255]
                ndvi_255_255 += 1
            elif (ndvi1 == -1.0):
                rgbColor2[x:x + 128, y:y + 128] = [0, 0, 255]
                ndvi_0_255 += 1
            elif (ndvi1 == 100):
                rgbColor2[x:x + 128, y:y + 128] = [0, 0, 128]



            #THE OSAVI FORMULA - 4 x 4
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                osavi1 = float(ave_nir1 - ave_vis1) / float(ave_nir1 + ave_vis1 + 0.16)           #Formula for NDVI    
                osavi1 = float(("{0:.2f}".format(osavi1))) 
                if ave_nir1 == 0.0 and ave_vis1 == 0.0:
                    osavi1 = 100               
            except ZeroDivisionError:
                osavi1 = 100
                        
            print("[" + str(x) + ":" + str(x + 128) + "," + str(y) + ":" + str(y + 128) + "] \t" + "NIR: " + str(ave_nir1) + "\t RED: " + str(ave_vis1) + "\t\t" + str(osavi1))

            stat = ""
            stat = str(osavi1) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_OSAVI_4x4StatisticalData.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()


            #CONDITIONS FOR OSAVI - 4 X 4
            if (osavi1 == 1.0):
                rgbColor3[x:x + 128, y:y + 128] = [0, 125, 0]
                osavi_125 += 1
            elif (osavi1 < 1.0 and osavi1 >= 0.75):
                rgbColor3[x:x + 128, y:y + 128] = [0, 150, 0]
                osavi_150 += 1
            elif (osavi1 < 0.75 and osavi1 >= 0.50):
                rgbColor3[x:x + 128, y:y + 128] = [0, 200, 0]
                osavi_200 += 1
            elif (osavi1 < 0.50 and osavi1 >= 0.25):
                rgbColor3[x:x + 128, y:y + 128] = [0, 225, 0]
                osavi_225 += 1
            elif (osavi1 < 0.25 and osavi1 >= 0.00):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 0]
                osavi_255 += 1
            elif (osavi1 < 0.0 and osavi1 >= -0.25):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 125]
                osavi_255_125 += 1
            elif (osavi1 < -0.25 and osavi1 >= -0.50):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 150]
                osavi_255_150 += 1
            elif (osavi1 < -0.50 and osavi1 >= -0.75):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 200]
                osavi_255_200 += 1
            elif (osavi1 < -0.75 and osavi1 > -0.86):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 255]
                osavi_255_255 += 1
            elif (osavi1 == -0.86):
                rgbColor3[x:x + 128, y:y + 128] = [0, 0, 255]
                osavi_0_255 += 1
            elif (osavi1 == 100):
                rgbColor3[x:x + 128, y:y + 128] = [0, 0, 128]


        print("\n")


    #BEAUTY RANGE
    dark2 = cv2.inRange(hsvColor, DARK_MIN, DARK_MAX)
    pink2 = cv2.inRange(hsvColor, PINK_MIN, PINK_MAX)
    gray2 = cv2.inRange(hsvColor, GRAY_MIN, GRAY_MAX)
    soil2 = cv2.inRange(hsvColor, SOIL_MIN, SOIL_MAX)

    #COUNT COLORS
    no_of_dark2 = cv2.countNonZero(dark2)
    no_of_pink2 = cv2.countNonZero(pink2)
    no_of_gray2 = cv2.countNonZero(gray2)
    no_of_soil2 = cv2.countNonZero(soil2)

    total_nir2 = no_of_dark2 + no_of_pink2 + 0.1
    total_vis2 = no_of_gray2 + no_of_soil2 + 0.1

    try:
        ave_nir2 = float(total_nir2 / 512.0)
        ave_vis2 = float(total_vis2 / 512.0)
    except ZeroDivisionError:
        ave_nir2 = -0.99
        ave_vis2 = -0.99

    np.seterr(divide = 'ignore', invalid = 'ignore')
    ndviV = 0.0
    
    try:
        ndviV = float(ave_nir2 - ave_vis2) / float(ave_nir2 + ave_vis2)
        osaviV = float(ave_nir2 - ave_vis2) / float(ave_nir2 + ave_vis2 + 0.16)
    except ZeroDivisionError:
        ndviV = -1.0
        osaviV = -1.0

    b, g, r = cv2.split(resized_image)
    resized2 = cv2.merge([r, g, b])

    b, g, r = cv2.split(rgbColor)
    ndvi2 = cv2.merge([r, g, b])
    blurred1 = cv2.medianBlur(ndvi2, 3)

    b, g, r = cv2.split(rgbColor1)
    osavi2 = cv2.merge([r, g, b])
    blurred2 = cv2.medianBlur(osavi2, 3)

    b, g, r = cv2.split(rgbColor2)
    ndvi3 = cv2.merge([r, g, b])

    b, g, r = cv2.split(rgbColor3)
    osavi3 = cv2.merge([r, g, b])

    # b, g, r = cv2.split(legend)
    # legend2 = cv2.merge([r, g, b])


    #PLOTTING THE RESULT
    ndvi_data = np.genfromtxt('./media/' + filename + '_NDVI_4x4StatisticalData.txt',delimiter=',')
    osavi_data = np.genfromtxt('./media/' + filename + '_OSAVI_4x4StatisticalData.txt',delimiter=',')

    ndvi_plt = ndvi_data[0:16]
    osavi_plt = osavi_data[0:16]


    # For Pie Graph
    #Pie Graph of NDVI
    colors = []
    sizes = []
    labels = []

    #Pie Graph of OSAVI
    colors1 = []
    sizes1 = []
    labels1 = []

    #Conditions for NDVI
    if ndvi_125 != 0:
        sizes += [ndvi_125]
        colors += ['#007d00']
        labels += ['Very Healthy']
    if ndvi_150 != 0:
        sizes += [ndvi_150]
        colors += ['#009600']
        labels += ['Very Healthy']
    if ndvi_200 != 0:
        sizes += [ndvi_200]
        colors += ['#00c800']
        labels += ['Moderate Healthy']
    if ndvi_225 != 0:
        sizes += [ndvi_225]
        colors += ['#00e100']
        labels += ['Moderate Healthy']
    if ndvi_255 != 0:
        sizes += [ndvi_255]
        colors += ['#00ff00']
        labels += ['Healthy']
    if ndvi_255_125 != 0:
        sizes += [ndvi_255_125]
        colors += ['#7dff00']
        labels += ['Unhealthy']
    if ndvi_255_150 != 0:
        sizes += [ndvi_255_150]
        colors += ['#96ff00']
        labels += ['Unhealthy']
    if ndvi_255_200 != 0:
        sizes += [ndvi_255_200]
        colors += ['#c8ff00']
        labels += ['Unhealthy']
    if ndvi_255_255 != 0:
        sizes += [ndvi_255_255]
        colors += ['#ffff00']
        labels += ['Dead']
    if ndvi_0_255 != 0:
        sizes += [ndvi_0_255]
        colors += ['#ff0000']
        labels += ['Dead']


    #Conditions for OSAVI
    if osavi_125 != 0:
        sizes1 += [osavi_125]
        colors1 += ['#007d00']
        labels1 += ['Very Healthy']
    if osavi_150 != 0:
        sizes1 += [osavi_150]
        colors1 += ['#009600']
        labels1 += ['Very Healthy']
    if osavi_200 != 0:
        sizes1 += [osavi_200]
        colors1 += ['#00c800']
        labels1 += ['Moderate Healthy']
    if osavi_225 != 0:
        sizes1 += [osavi_225]
        colors1 += ['#00e100']
        labels1 += ['Moderate Healthy']
    if osavi_255 != 0:
        sizes1 += [osavi_255]
        colors1 += ['#00ff00']
        labels1 += ['Healthy']
    if osavi_255_125 != 0:
        sizes1 += [osavi_255_125]
        colors1 += ['#7dff00']
        labels1 += ['Unhealthy']
    if osavi_255_150 != 0:
        sizes1 += [osavi_255_150]
        colors1 += ['#96ff00']
        labels1 += ['Unhealthy']
    if osavi_255_200 != 0:
        sizes1 += [osavi_255_200]
        colors1 += ['#c8ff00']
        labels1 += ['Unhealthy']
    if osavi_255_255 != 0:
        sizes1 += [osavi_255_255]
        colors1 += ['#ffff00']
        labels1 += ['Dead']
    if osavi_0_255 != 0:
        sizes1 += [osavi_0_255]
        colors1 += ['#ff0000']
        labels1 += ['Dead']


    # Plotting Pie Graph for NDVI
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',shadow=True,startangle=90)
    ax1.axis('equal')
    plt.savefig('./media/' + filename + '_NDVI PIEGRAPH.png', bbox_inches='tight')
    plt.close()

    # Plotting Pie Graph for NDVI
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes1, colors=colors1, labels=labels1, autopct='%1.1f%%',shadow=True,startangle=90)
    ax2.axis('equal')
    plt.savefig('./media/' + filename + '_OSAVI PIEGRAPH.png', bbox_inches='tight')
    plt.close()

    # Plotting all Images
    plt.subplot(241), plt.imshow(resized2), plt.title('RAW IMAGE')
    plt.subplot(242), plt.imshow(blurred1), plt.title('NDVI READING')
    plt.subplot(243), plt.imshow(blurred2), plt.title('OSAVI READING')
    # plt.subplot(244), plt.imshow(legend2), plt.title('LEGEND'), plt.xticks([]), plt.yticks([]), plt.title("LEGEND")
    plt.subplot(246), plt.imshow(ndvi3), plt.title('NDVI 4X4 READING')
    plt.subplot(247), plt.imshow(osavi3), plt.title('OSAVI 4X4 READING')
    plt.subplot(248), plt.xlabel('Number of Pixels'), plt.plot(ndvi_plt, color="green", label="NDVI"), plt.plot(osavi_plt, color="red", label="OSAVI"), plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.), plt.title("\n" + "Average NDVI: " + str(ndviV) + "\n" + "Average OSAVI: " + str(osaviV))
    plt.suptitle("PROCESSING AND AQUISITION OF NDVI AND OSAVI IMAGE")
    plt.close()
    
    #SAVE IMAGES AS PNG
    save_resized2 = plt.imshow(resized2)
    plt.savefig('./media/' + filename + '_RawImage.png', bbox_inches='tight')
    plt.close()        

    save_blurred1 = plt.imshow(blurred1)
    plt.savefig('./media/' + filename + '_NDVI READING.png', bbox_inches='tight')
    plt.close()

    save_blurred2 = plt.imshow(blurred2)
    plt.savefig('./media/' + filename + '_OSAVI READING.png', bbox_inches='tight')
    plt.close()

    save_ndvi3 = plt.imshow(ndvi3)
    plt.savefig('./media/' + filename + '_NDVI 4x4 READING.png', bbox_inches='tight')
    plt.close()

    save_osavi3 = plt.imshow(osavi3)
    plt.savefig('./media/' + filename + '_OSAVI 4x4 READING.png', bbox_inches='tight')
    plt.close()

    save_numpixel = plt.xlabel('Number of Pixels'), plt.plot(ndvi_plt, color="green", label="NDVI"), plt.plot(osavi_plt, color="red", label="OSAVI"), plt.legend(), plt.title("\n" + "Average NDVI: " + str(ndviV) + "\n" + "Average OSAVI: " + str(osaviV))
    plt.savefig('./media/' + filename + '_STATISTICAL GRAPH.png', bbox_inches='tight')
    plt.close()
    plt.close('all')

    imaging = str(image)
    raw = imaging + '_RawImage.png'
    ndvi = imaging + '_NDVI READING.png'
    osavi = imaging + '_OSAVI READING.png'
    ndvi_4x4 = imaging + '_NDVI 4x4 READING.png'
    osavi_4x4 = imaging + '_OSAVI 4x4 READING.png'
    graph = imaging + '_STATISTICAL GRAPH.png'
    ndvipiegraph = imaging + '_NDVI PIEGRAPH.png'
    osavipiegraph = imaging + '_OSAVI PIEGRAPH.png'


    # Add to Database
    image.processed = True
    image.save()

    form = Data()
    form.image = image
    form.raw = raw
    form.ndvi = ndvi
    form.osavi = osavi
    form.ndvi_4x4 = ndvi_4x4
    form.osavi_4x4 = osavi_4x4
    form.graph = graph
    form.ndvipiegraph = ndvipiegraph
    form.osavipiegraph = osavipiegraph
    image_data = image.data_set.all()
    form.save()

    return render(request, 'cropmapapp/detail.html', {'image':image}) 
    
    
# Test_Algorithm Cropping Data
def test_algorithm_data(request, image_id, data_id):

    croppingdata = get_object_or_404(CroppingData, pk=data_id)
    croppingimage = get_object_or_404(CroppingImage, pk=image_id)

    import cv2
    import numpy as np
    import tkinter as tk
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    import os
    import matplotlib.patches as mpathches

    np.seterr(divide = 'ignore', invalid = 'ignore')
    root = tk.Tk()

    croppingdatas = str(croppingdata.cropping)
    print(croppingdatas)

    filename=os.path.basename('./media/' + croppingdatas)
    img1 = cv2.imread('./media/' + filename)
    legend = cv2.imread('./media/legend.jpg')

    #RESIZE
    resized_image = img1[0:512, 0:512]

    #CONVERT TO HSV
    hsvColor = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    hsvColor1 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    rgbColor = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    rgbColor1 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB) 
    rgbColor2 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB) 
    rgbColor3 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB) 


    #HOW BEAUTIFUL IS BEAUTIFUL
    #RED
    SOIL_MIN = np.array([160, 50, 200])
    SOIL_MAX = np.array([180, 145, 255])

    GRAY_MIN = np.array([0, 40, 25])
    GRAY_MAX = np.array([140, 280, 255])

    #NIR
    PINK_MIN = np.array([140, 100, 0])
    PINK_MAX = np.array([180, 255, 255])

    DARK_MIN = np.array([0, 85, 130])
    DARK_MAX = np.array([10, 255, 230])



    # Variables for Computing Percentage
    #NDVI
    ndvi_125 = 0
    ndvi_150 = 0
    ndvi_200 = 0
    ndvi_225 = 0
    ndvi_255 = 0
    ndvi_255_125 = 0
    ndvi_255_150 = 0
    ndvi_255_200 = 0
    ndvi_255_255 = 0
    ndvi_0_255 = 0

    #OSAVI
    osavi_125 = 0
    osavi_150 = 0
    osavi_200 = 0
    osavi_225 = 0
    osavi_255 = 0
    osavi_255_125 = 0
    osavi_255_150 = 0
    osavi_255_200 = 0
    osavi_255_255 = 0
    osavi_0_255 = 0


    #THE MATRIX GOES IN...
    for x in range(0, 512, 4):
        for y in range(0, 512, 4):

            fourbyfour = hsvColor[x:x + 4, y:y + 4]

            #BEAUTY RANGE
            dark = cv2.inRange(fourbyfour, DARK_MIN, DARK_MAX)
            pink = cv2.inRange(fourbyfour, PINK_MIN, PINK_MAX)
            gray = cv2.inRange(fourbyfour, GRAY_MIN, GRAY_MAX)
            soil = cv2.inRange(fourbyfour, SOIL_MIN, SOIL_MAX)

            #COUNT COLORS
            no_of_dark = cv2.countNonZero(dark)
            no_of_pink = cv2.countNonZero(pink)
            no_of_gray = cv2.countNonZero(gray)
            no_of_soil = cv2.countNonZero(soil)

            total_nir = no_of_dark + no_of_pink + no_of_soil
            total_vis = no_of_gray + no_of_soil

            try:
                ave_nir = float(total_nir / 16.0)
                ave_vis = float(total_vis / 16.0)
            except ZeroDivisionError:
                ave_nir = -1.0
                ave_vis = -1.0



            #THE NDVI FORMULA
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                ndvi = float(ave_nir - ave_vis) / float(ave_nir + ave_vis)   #Formula for NDVI                    
            except ZeroDivisionError:
                ndvi = 100
                        
            print("[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + "\t RED: " + str(ave_vis) + "\t\t" + str(ndvi))

            stat = ""
            stat = stat + "[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + " \t RED: " + str(ave_vis) + "\t\t" + str(ndvi) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_NDVI_statisticaldata.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()

                
            #CONDITIONS FOR NDVI
            if(ndvi == 1.0):
                rgbColor[x:x + 4, y:y + 4] = [0, 125, 0]
            elif (ndvi < 1.0 and ndvi >= 0.75):
                rgbColor[x:x + 4, y:y + 4] = [0, 150, 0]
            elif (ndvi < 0.75 and ndvi >= 0.50):
                rgbColor[x:x + 4, y:y + 4] = [0, 200, 0]
            elif (ndvi < 0.50 and ndvi >= 0.25):
                rgbColor[x:x + 4, y:y + 4] = [0, 225, 0]
            elif (ndvi < 0.25 and ndvi >= 0.00):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 0]
            elif (ndvi < 0.0 and ndvi >= -0.25):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 125]
            elif (ndvi < -0.25 and ndvi >= -0.50):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 150]
            elif (ndvi < -0.50 and ndvi >= -0.75):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 200]
            elif (ndvi < -0.75 and ndvi > -1.0):
                rgbColor[x:x + 4, y:y + 4] = [0, 255, 255]
            elif (ndvi == -1.0):
                rgbColor[x:x + 4, y:y + 4] = [0, 0, 255]
            elif (ndvi == 100):
                rgbColor[x:x + 4, y:y + 4] = [0, 0, 128]

               
            #THE OSAVI FORMULA
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                osavi = float(ave_nir - ave_vis) / float(ave_nir + ave_vis + 0.16)   #Formula for OSAVI
                osavi = float(("{0:.2f}".format(osavi)))
                if ave_nir == 0.0 and ave_vis == 0.0:
                    osavi = 100

            except ZeroDivisionError:
                osavi = 100
   
            print("[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + "\t RED: " + str(ave_vis) + "\t\t" + str(osavi))

            stat = ""
            stat = stat + "[" + str(x) + ":" + str(x + 4) + "," + str(y) + ":" + str(y + 4) + "] \t" + "NIR: " + str(ave_nir) + " \t RED: " + str(ave_vis) + "\t\t" + str(osavi) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_OSAVI_statisticaldata.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()


            #CONDITIONS FOR OSAVI
            if (osavi == 1.0):
                rgbColor1[x:x + 4, y:y + 4] = [0, 125, 0]
            elif (osavi < 1.0 and osavi >= 0.75):
                rgbColor1[x:x + 4, y:y + 4] = [0, 150, 0]
            elif (osavi < 0.75 and osavi >= 0.50):
                rgbColor1[x:x + 4, y:y + 4] = [0, 200, 0]
            elif (osavi < 0.50 and osavi >= 0.25):
                rgbColor1[x:x + 4, y:y + 4] = [0, 225, 0]
            elif (osavi < 0.25 and osavi >= 0.00):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 0]
            elif (osavi < 0.0 and osavi >= -0.25):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 125]
            elif (osavi < -0.25 and osavi >= -0.50):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 150]
            elif (osavi < -0.50 and osavi >= -0.75):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 200]
            elif (osavi < -0.75 and osavi > -0.86):
                rgbColor1[x:x + 4, y:y + 4] = [0, 255, 255]
            elif (osavi == -0.86):
                rgbColor1[x:x + 4, y:y + 4] = [0, 0, 255]
            elif (osavi == 100):
                rgbColor1[x:x + 4, y:y + 4] = [0, 0, 128]

        print("\n")


    #128 x 128 Matrix = 4 x 4 as a whole
    for x in range(0,512,128):
        for y in range(0,512,128):

            onetwoeight = hsvColor1[x:x + 128, y:y + 128]

            #BEAUTY RANGE
            dark1 = cv2.inRange(onetwoeight, DARK_MIN, DARK_MAX)
            pink1 = cv2.inRange(onetwoeight, PINK_MIN, PINK_MAX)
            gray1 = cv2.inRange(onetwoeight, GRAY_MIN, GRAY_MAX)
            soil1 = cv2.inRange(onetwoeight, SOIL_MIN, SOIL_MAX)

            #COUNT COLORS
            no_of_dark1 = cv2.countNonZero(dark1)
            no_of_pink1 = cv2.countNonZero(pink1)
            no_of_gray1 = cv2.countNonZero(gray1)
            no_of_soil1 = cv2.countNonZero(soil1)

            total_nir1 = no_of_dark1 + no_of_pink1 + no_of_soil1
            total_vis1 = no_of_gray1 + no_of_soil1

            try:
                ave_nir1 = float(total_nir1 / 16384.0) 
                ave_vis1 = float(total_vis1 / 16384.0) 
            except ZeroDivisionError:
                ave_nir1 = -1.0
                ave_vis1 = -1.0


            #THE NDVI FORMULA - 4 x 4
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                ndvi1 = float(ave_nir1 - ave_vis1) / float(ave_nir1 + ave_vis1)           #Formula for NDVI    
                ndvi1 = float(("{0:.2f}".format(ndvi1)))                
            except ZeroDivisionError:
                ndvi1 = 100
                        
            print("[" + str(x) + ":" + str(x + 128) + "," + str(y) + ":" + str(y + 128) + "] \t" + "NIR: " + str(ave_nir1) + "\t RED: " + str(ave_vis1) + "\t\t" + str(ndvi1))


            stat = ""
            stat = str(ndvi1) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_NDVI_4x4StatisticalData.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()

                
            #CONDITIONS FOR NDVI - 4 X 4 
            if(ndvi1 == 1.0):
                rgbColor2[x:x + 128, y:y + 128] = [0, 125, 0]
                ndvi_125 += 1
            elif (ndvi1 < 1.0 and ndvi1 >= 0.75):
                rgbColor2[x:x + 128, y:y + 128] = [0, 150, 0]
                ndvi_150 += 1
            elif (ndvi1 < 0.75 and ndvi1 >= 0.50):
                rgbColor2[x:x + 128, y:y + 128] = [0, 200, 0]
                ndvi_200 += 1
            elif (ndvi1 < 0.50 and ndvi1 >= 0.25):
                rgbColor2[x:x + 128, y:y + 128] = [0, 225, 0]
                ndvi_225 += 1
            elif (ndvi1 < 0.25 and ndvi1 >= 0.00):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 0]
                ndvi_255 += 1
            elif (ndvi1 < 0.0 and ndvi1 >= -0.25):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 125]
                ndvi_255_125 += 1
            elif (ndvi1 < -0.25 and ndvi1 >= -0.50):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 150]
                ndvi_255_150 += 1
            elif (ndvi1 < -0.50 and ndvi1 >= -0.75):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 200]
                ndvi_255_200 += 1
            elif (ndvi1 < -0.75 and ndvi1 > -1.0):
                rgbColor2[x:x + 128, y:y + 128] = [0, 255, 255]
                ndvi_255_255 += 1
            elif (ndvi1 == -1.0):
                rgbColor2[x:x + 128, y:y + 128] = [0, 0, 255]
                ndvi_0_255 += 1
            elif (ndvi1 == 100):
                rgbColor2[x:x + 128, y:y + 128] = [0, 0, 128]



            #THE OSAVI FORMULA - 4 x 4
            np.seterr(divide = 'ignore', invalid = 'ignore')
            try:
                osavi1 = float(ave_nir1 - ave_vis1) / float(ave_nir1 + ave_vis1 + 0.16)           #Formula for NDVI    
                osavi1 = float(("{0:.2f}".format(osavi1))) 
                if ave_nir1 == 0.0 and ave_vis1 == 0.0:
                    osavi1 = 100               
            except ZeroDivisionError:
                osavi1 = 100
                        
            print("[" + str(x) + ":" + str(x + 128) + "," + str(y) + ":" + str(y + 128) + "] \t" + "NIR: " + str(ave_nir1) + "\t RED: " + str(ave_vis1) + "\t\t" + str(osavi1))

            stat = ""
            stat = str(osavi1) + "\n"

            def make_text_file():
                a = open('./media/' + filename + '_OSAVI_4x4StatisticalData.txt', "a")
                a.write(stat)
                a.close()
                
            make_text_file()


            #CONDITIONS FOR OSAVI - 4 X 4
            if (osavi1 == 1.0):
                rgbColor3[x:x + 128, y:y + 128] = [0, 125, 0]
                osavi_125 += 1
            elif (osavi1 < 1.0 and osavi1 >= 0.75):
                rgbColor3[x:x + 128, y:y + 128] = [0, 150, 0]
                osavi_150 += 1
            elif (osavi1 < 0.75 and osavi1 >= 0.50):
                rgbColor3[x:x + 128, y:y + 128] = [0, 200, 0]
                osavi_200 += 1
            elif (osavi1 < 0.50 and osavi1 >= 0.25):
                rgbColor3[x:x + 128, y:y + 128] = [0, 225, 0]
                osavi_225 += 1
            elif (osavi1 < 0.25 and osavi1 >= 0.00):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 0]
                osavi_255 += 1
            elif (osavi1 < 0.0 and osavi1 >= -0.25):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 125]
                osavi_255_125 += 1
            elif (osavi1 < -0.25 and osavi1 >= -0.50):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 150]
                osavi_255_150 += 1
            elif (osavi1 < -0.50 and osavi1 >= -0.75):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 200]
                osavi_255_200 += 1
            elif (osavi1 < -0.75 and osavi1 > -0.86):
                rgbColor3[x:x + 128, y:y + 128] = [0, 255, 255]
                osavi_255_255 += 1
            elif (osavi1 == -0.86):
                rgbColor3[x:x + 128, y:y + 128] = [0, 0, 255]
                osavi_0_255 += 1
            elif (osavi1 == 100):
                rgbColor3[x:x + 128, y:y + 128] = [0, 0, 128]


        print("\n")


    #BEAUTY RANGE
    dark2 = cv2.inRange(hsvColor, DARK_MIN, DARK_MAX)
    pink2 = cv2.inRange(hsvColor, PINK_MIN, PINK_MAX)
    gray2 = cv2.inRange(hsvColor, GRAY_MIN, GRAY_MAX)
    soil2 = cv2.inRange(hsvColor, SOIL_MIN, SOIL_MAX)

    #COUNT COLORS
    no_of_dark2 = cv2.countNonZero(dark2)
    no_of_pink2 = cv2.countNonZero(pink2)
    no_of_gray2 = cv2.countNonZero(gray2)
    no_of_soil2 = cv2.countNonZero(soil2)

    total_nir2 = no_of_dark2 + no_of_pink2 + 0.1
    total_vis2 = no_of_gray2 + no_of_soil2 + 0.1

    try:
        ave_nir2 = float(total_nir2 / 512.0)
        ave_vis2 = float(total_vis2 / 512.0)
    except ZeroDivisionError:
        ave_nir2 = -0.99
        ave_vis2 = -0.99

    np.seterr(divide = 'ignore', invalid = 'ignore')
    ndviV = 0.0
    
    try:
        ndviV = float(ave_nir2 - ave_vis2) / float(ave_nir2 + ave_vis2)
        osaviV = float(ave_nir2 - ave_vis2) / float(ave_nir2 + ave_vis2 + 0.16)
    except ZeroDivisionError:
        ndviV = -1.0
        osaviV = -1.0

    b, g, r = cv2.split(resized_image)
    resized2 = cv2.merge([r, g, b])

    b, g, r = cv2.split(rgbColor)
    ndvi2 = cv2.merge([r, g, b])
    blurred1 = cv2.medianBlur(ndvi2, 3)

    b, g, r = cv2.split(rgbColor1)
    osavi2 = cv2.merge([r, g, b])
    blurred2 = cv2.medianBlur(osavi2, 3)

    b, g, r = cv2.split(rgbColor2)
    ndvi3 = cv2.merge([r, g, b])

    b, g, r = cv2.split(rgbColor3)
    osavi3 = cv2.merge([r, g, b])

    # b, g, r = cv2.split(legend)
    # legend2 = cv2.merge([r, g, b])


    #PLOTTING THE RESULT
    ndvi_data = np.genfromtxt('./media/' + filename + '_NDVI_4x4StatisticalData.txt',delimiter=',')
    osavi_data = np.genfromtxt('./media/' + filename + '_OSAVI_4x4StatisticalData.txt',delimiter=',')

    ndvi_plt = ndvi_data[0:16]
    osavi_plt = osavi_data[0:16]



    #For Colors, Sizes, Explode, and Labels of Pie Chart
    colors = []
    sizes = []
    labels = []

    colors1 = []
    sizes1 = []
    labels1 = []

    #Conditions for NDVI
    if ndvi_125 != 0:
        sizes += [ndvi_125]
        colors += ['#007d00']
        labels += ['Very Healthy']
    if ndvi_150 != 0:
        sizes += [ndvi_150]
        colors += ['#009600']
        labels += ['Very Healthy']
    if ndvi_200 != 0:
        sizes += [ndvi_200]        
        colors += ['#00c800']
        labels += ['Moderate Healthy']
    if ndvi_225 != 0:
        sizes += [ndvi_225]
        colors += ['#00e100']
        labels += ['Moderate Healthy']
    if ndvi_255 != 0:
        sizes += [ndvi_255]
        colors += ['#00ff00']
        labels += ['Healthy']
    if ndvi_255_125 != 0:
        sizes += [ndvi_255_125]
        colors += ['#7dff00']
        labels += ['Unhealthy']
    if ndvi_255_150 != 0:
        sizes += [ndvi_255_150]
        colors += ['#96ff00']
        labels += ['Unhealthy']
    if ndvi_255_200 != 0:
        sizes += [ndvi_255_200]
        colors += ['#c8ff00']
        labels += ['Unhealthy']
    if ndvi_255_255 != 0:
        sizes += [ndvi_255_255]
        colors += ['#ffff00']
        labels += ['Dead']
    if ndvi_0_255 != 0:
        sizes += [ndvi_0_255]
        colors += ['#ff0000']
        labels += ['Dead']

    #Conditions for OSAVI
    if osavi_125 != 0:
        sizes1 += [osavi_125]
        colors1 += ['#007d00']
        labels1 += ['Very Healthy']
    if osavi_150 != 0:
        sizes1 += [osavi_150]
        colors1 += ['#009600']
        labels1 += ['Very Healthy']
    if osavi_200 != 0:
        sizes1 += [osavi_200]
        colors1 += ['#00c800']
        labels1 += ['Moderate Healthy']
    if osavi_225 != 0:
        sizes1 += [osavi_225]
        colors1 += ['#00e100']
        labels1 += ['Moderate Healthy']
    if osavi_255 != 0:
        sizes1 += [osavi_255]
        colors1 += ['#00ff00']
        labels1 += ['Average']
    if osavi_255_125 != 0:
        sizes1 += [osavi_255_125]
        colors1 += ['#7dff00']
        labels1 += ['Unhealthy']
    if osavi_255_150 != 0:
        sizes1 += [osavi_255_150]
        colors1 += ['#96ff00']
        labels1 += ['Unhealthy']
    if osavi_255_200 != 0:
        sizes1 += [osavi_255_200]
        colors1 += ['#c8ff00']
        labels1 += ['Unhealthy']
    if osavi_255_255 != 0:
        sizes1 += [osavi_255_255]
        colors1 += ['#ffff00']
        labels1 += ['Dead']
    if osavi_0_255 != 0:
        sizes1 += [osavi_0_255]
        colors1 += ['#ff0000']
        labels1 += ['Dead']


    #Pie Chart for NDVI
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',shadow=True,startangle=90)
    ax1.axis('equal')
    plt.savefig('./media/' + filename + '_NDVI PIEGRAPH.png', bbox_inches='tight')
    plt.close()

    #Pie Chart for OSAVI
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes1, colors=colors1, labels=labels1, autopct='%1.1f%%',shadow=True,startangle=90)
    ax2.axis('equal')
    plt.savefig('./media/' + filename + '_OSAVI PIEGRAPH.png', bbox_inches='tight')
    plt.close()


    plt.subplot(241), plt.imshow(resized2), plt.title('RAW IMAGE')
    plt.subplot(242), plt.imshow(blurred1), plt.title('NDVI READING')
    plt.subplot(243), plt.imshow(blurred2), plt.title('OSAVI READING')
    # plt.subplot(244), plt.imshow(legend2), plt.title('LEGEND'), plt.xticks([]), plt.yticks([]), plt.title("LEGEND")
    plt.subplot(246), plt.imshow(ndvi3), plt.title('NDVI 4X4 READING')
    plt.subplot(247), plt.imshow(osavi3), plt.title('OSAVI 4X4 READING')
    plt.subplot(248), plt.xlabel('Number of Pixels'), plt.plot(ndvi_plt, color="green", label="NDVI"), plt.plot(osavi_plt, color="red", label="OSAVI"), plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.), plt.title("\n" + "Average NDVI: " + str(ndviV) + "\n" + "Average OSAVI: " + str(osaviV))
    plt.suptitle("PROCESSING AND AQUISITION OF NDVI AND OSAVI IMAGE")
    plt.close()
    
    #SAVE IMAGE AS PNG
    save_resize2 = plt.imshow(resized2)
    plt.savefig('./media/' + filename + '_RawImage.png', bbox_inches='tight')
    plt.close()        

    save_blurred1 = plt.imshow(blurred1)
    plt.savefig('./media/' + filename + '_NDVI READING.png', bbox_inches='tight')
    plt.close()

    save_blurred2 = plt.imshow(blurred2)
    plt.savefig('./media/' + filename + '_OSAVI READING.png', bbox_inches='tight')
    plt.close()

    save_ndvi3 = plt.imshow(ndvi3)
    plt.savefig('./media/' + filename + '_NDVI 4x4 READING.png', bbox_inches='tight')
    plt.close()

    save_osavi3 = plt.imshow(osavi3)
    plt.savefig('./media/' + filename + '_OSAVI 4x4 READING.png', bbox_inches='tight')
    plt.close()

    save_numpixel = plt.xlabel('Number of Pixels'), plt.plot(ndvi_plt, color="green", label="NDVI"), plt.plot(osavi_plt, color="red", label="OSAVI"), plt.legend(), plt.title("\n" + "Average NDVI: " + str(ndviV) + "\n" + "Average OSAVI: " + str(osaviV))
    plt.savefig('./media/' + filename + '_STATISTICAL GRAPH.png', bbox_inches='tight')
    plt.close()
    plt.close('all')


    imaging = str(croppingdata)


    raw = imaging + '_RawImage.png'
    ndvi = imaging + '_NDVI READING.png'
    osavi = imaging + '_OSAVI READING.png'
    ndvi_4x4 = imaging + '_NDVI 4x4 READING.png'
    osavi_4x4 = imaging + '_OSAVI 4x4 READING.png'
    graph = imaging + '_STATISTICAL GRAPH.png'
    ndvipiegraph = imaging + '_NDVI PIEGRAPH.png'
    osavipiegraph = imaging + '_OSAVI PIEGRAPH.png'
    croppingdata.processed = True
    croppingdata.save()


    form = CroppingDataDetail()
    form.image = croppingdata
    form.raw = raw
    form.ndvi = ndvi
    form.osavi = osavi
    form.ndvi_4x4 = ndvi_4x4
    form.osavi_4x4 = osavi_4x4
    form.graph = graph
    form.ndvipiegraph = ndvipiegraph
    form.osavipiegraph = osavipiegraph
    # image_data = croppingdata.croppingdatadetail_set.all()
    form.save()


    date = croppingdata.croppingdate
    desc = croppingdata.description
    
    
    form1 = Comparison()
    form1.image = croppingimage
    form1.raw = raw
    form1.croppingdate = date
    form1.description = desc
    form1.graph = graph
    form1.ndvipiegraph = ndvipiegraph
    form1.osavipiegraph = osavipiegraph
    form1.croppingdata = croppingdata
    # image_data = croppingdata.Comparison_set.all()
    form1.save()

    return render(request, 'cropmapapp/croppingdatadetail.html', {'croppingdata':croppingdata}) 

# Logout User
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'cropmapapp/login.html', context)


# Login User
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'cropmapapp/home.html')
            else:
                return render(request, 'cropmapapp/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'cropmapapp/login.html', {'error_message': 'Invalid login'})
    return render(request, 'cropmapapp/login.html')


# Register user
def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'cropmapapp/home.html')

	context = {
		"form": form,
	}
	return render(request, 'cropmapapp/register.html', context)
    