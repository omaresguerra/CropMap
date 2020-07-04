from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cropmapapp'

urlpatterns = [
	
	#/cropmapapp/
	url(r'^$', views.home, name='home'),
	#/cropmapapp/
	url(r'^about/$', views.about, name='about'),
	#/cropmapapp/
	url(r'^image/$', views.index, name='index'),
	#/cropmapapp/712/
	url(r'^image/(?P<image_id>[0-9]+)/$', views.detail, name='detail'),
	#/cropmapapp/image/add
	url(r'^image/add_image/$',views.image_add, name='image-add'),
	#/cropmapapp/image/2/
	# url(r'^image/(?P<image_id>[0-9]+)/$',views.ImageUpdate, name='image-update'),
	#/cropmapapp/image/2/delete
	url(r'^image/(?P<image_id>[0-9]+)/delete_image/$',views.image_delete, name='image-delete'),



	# test algorithm
	url(r'^image/test/(?P<image_id>[0-9]+)/$',views.test_algorithm, name='test-algorithm'), 
	# test algorithm - croppingdata
	url(r'^croppingdata/(?P<image_id>[0-9]+)/test/(?P<data_id>[0-9]+)/$',views.test_algorithm_data, name='test-algorithm-data'), 



	#/cropping/
	url(r'^cropping/$', views.cropping, name='cropping'),
	#/cropping/712/
	url(r'^cropping/(?P<image_id>[0-9]+)/$', views.croppingdetail, name='croppingdetail'),
	#/cropping/add
	url(r'^cropping/add-cropping/$',views.cropping_add, name='cropping-add'),
	#/cropping/2/delete
	url(r'^cropping/(?P<image_id>[0-9]+)/delete-data/$',views.croppingimage_delete, name='croppingimage-delete'),

	#/cropping/compare/712/
	url(r'^cropping/compare/(?P<image_id>[0-9]+)/$', views.compare, name='compare'),

	
	#/cropping/712/
	url(r'^croppingdata/(?P<data_id>[0-9]+)/$', views.croppingdatadetail, name='croppingdatadetail'),
	#/croppingdata/add
	url(r'^(?P<image_id>[0-9]+)/add-data/$',views.croppingdata_add, name='data-add'),
	#/cropping/2/delete
	url(r'^cropping/(?P<image_id>[0-9]+)/delete-croppingdata/(?P<data_id>[0-9]+)/$',views.croppingdata_delete, name='croppingdata-delete'),


	#Register
	url(r'^register/$', views.register, name='register'),
	#Login_User
	url(r'^login_user/$', views.login_user, name='login_user'),
	#Logout_User
	url(r'^logout_user/$', views.logout_user, name='logout_user'),


	# confirm password
	url(r'^password_reset/$',auth_views.password_reset,name='password_reset'),
	url(r'^password_reset/done/$',auth_views.password_reset_done,name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Z-a-z]{1,20})/$',auth_views.password_reset_confirm,name='password_reset_confirm'),
	url(r'^reset/done/$',auth_views.password_reset_complete,name='password_reset_complete'),
	# url(r'^password_reset/$',auth_views.password_reset,{'template_name':'password_reset_form.html'}),

	url(r'^accounts/login/$',views.login_user, name='login_user'),

	#/print
	url(r'^print/(?P<image_id>[0-9]+)/$', views.print_data, name='print-data'),

	#/print-comparison
	url(r'^printcomparison/(?P<image_id>[0-9]+)/$', views.print_comparison, name='print-comparison')

]	
