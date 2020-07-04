# from django.views import generic
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.core.urlresolvers import reverse_lazy



# -----------------------------------------------------------------------------------------





# def create_image(request):
# 	form = ImageForm(request.POST or None, request.FIlES or None)
# 	if form.is_valid():

# class IndexView(generic.ListView):
# 	template_name = 'thesis/index.html'

# 	def get_queryset(self):
# 		return Image.objects.all()

# class ImageDetail(generic.DetailView):
# 	model = Image
# 	template_name = 'thesis/detail.html'

# class ImageCreate(CreateView):
# 	model = Image
# 	fields = ['image_name', 'image_raw', 'image_description']
# 	success_url = reverse_lazy('thesis:index')

# class ImageUpdate(UpdateView):
# 	model = Image




# 	fields = ['image_name', 'image_raw', 'image_description']

# class ImageDelete(DeleteView):
# 	model = Image
# 	success_url = reverse_lazy('thesis:index')



# class TestAlgorithm(generic.DetailView):
# 	model = Image
# 	# raw_image = ['image_raw']
# 	template_name = 'thesis/test-algorithm.html'



# class Cropping(generic.ListView):
# 	template_name = 'thesis/cropping.html'

# 	def get_queryset(self):
# 		return CroppingImage.objects.all()

# class CroppingDetail(generic.DetailView):
# 	model = CroppingImage
# 	template_name = 'thesis/croppingdetail.html'
		
# # Add Cropping Image
# class CroppingCreate(CreateView):
# 	model = CroppingImage
# 	fields = ['image_name', 'image_raw', 'image_description']
# 	success_url = reverse_lazy('thesis:cropping')

# #Delete Cropping Image
# class CroppingImageDelete(DeleteView):
# 	model = CroppingImage
# 	success_url = reverse_lazy('thesis:cropping')


# # Add Cropping Image
# class CroppingDataCreate(CreateView):
# 	model = CroppingData
# 	fields = ['image', 'cropping', 'croppingdate', 'description']
# 	success_url = reverse_lazy('thesis:cropping')


# # def CroppingDataCreate(request, image_id):
# # 	form 
# # 	if form.is_valid():