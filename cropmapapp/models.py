from django.contrib.auth.models import Permission, User
from django.db import models

class Image(models.Model):
	user = models.ForeignKey(User, default=1, on_delete = models.CASCADE)
	image_name = models.CharField(max_length = 1000)
	image_description = models.CharField(max_length = 2000)
	image_raw = models.FileField()
	processed = models.BooleanField(default=False)

	# def get_absolute_url(self):
	# 	return reverse('cropmapapp:detail', kwargs={'pk':self.pk})

	def __str__(self):
		return str(self.image_raw)

class Data(models.Model):
	image = models.ForeignKey(Image, on_delete = models.CASCADE)
	raw = models.CharField(max_length = 1000)
	ndvi = models.CharField(max_length = 1000)
	osavi = models.CharField(max_length = 1000)
	ndvi_4x4 = models.CharField(max_length = 1000)
	osavi_4x4 = models.CharField(max_length = 1000)
	graph = models.CharField(max_length = 1000)
	ndvipiegraph = models.CharField(max_length = 1000)
	osavipiegraph = models.CharField(max_length = 1000)

	def __str__(self):
		return self.raw

class CroppingImage(models.Model):
	user = models.ForeignKey(User, default=1, on_delete = models.CASCADE)
	surveying_area = models.CharField(max_length = 1000)
	address = models.CharField(max_length = 1000)
	land_description = models.CharField(max_length = 2000)
	image_raw = models.FileField()

	# def get_absolute_url(self):
	# 	return reverse('cropmapapp:detail', kwargs={'pk':self.pk})

	def __str__(self):
		return self.surveying_area
	
		
class CroppingData(models.Model):
	image = models.ForeignKey(CroppingImage, on_delete = models.CASCADE)
	cropping = models.FileField()
	croppingdate = models.DateField()
	description = models.CharField(max_length = 2000)
	processed = models.BooleanField(default=False)

	def __str__(self):
		return str(self.cropping)


class CroppingDataDetail(models.Model):
	image = models.ForeignKey(CroppingData, on_delete = models.CASCADE)
	raw = models.CharField(max_length = 1000)
	ndvi = models.CharField(max_length = 1000)
	osavi = models.CharField(max_length = 1000)
	ndvi_4x4 = models.CharField(max_length = 1000)
	osavi_4x4 = models.CharField(max_length = 1000)
	graph = models.CharField(max_length = 1000)
	ndvipiegraph = models.CharField(max_length = 1000)
	osavipiegraph = models.CharField(max_length = 1000)

	def __str__(self):
		return self.raw

class Comparison(models.Model):
	image = models.ForeignKey(CroppingImage, on_delete = models.CASCADE)
	raw = models.CharField(max_length = 1000)
	croppingdate =models.DateField()
	description = models.CharField(max_length = 2000)
	graph = models.CharField(max_length = 1000)
	ndvipiegraph = models.CharField(max_length = 1000)
	osavipiegraph = models.CharField(max_length = 1000)
	croppingdata = models.CharField(max_length = 1000)

	def __str__(self):
		return str(self.image)
	
		