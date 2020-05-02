
from django.urls import path, include
from . import views

urlpatterns = [
	path('add_image', views.home, name='home'),
	path('', views.home, name='home'),
	path('apply_lsb', views.apply_lsb, name='apply_lsb'),
	path('convert_to_binary',views.convert_to_binary,name='convert_to_binary'),
	path('apply_partitioning',views.apply_partitioning,name='apply_partitioning'),
	path('perform_zigzag',views.perform_zigzag,name='perform_zigzag'),
	path('perform_swapping',views.perform_swapping,name='perform_swapping'),
	path('final_encrypted_image',views.final_encrypted_image,name='final_encrypted_image'),
	path('decrypt',views.decrypt,name='decrypt'),
]


