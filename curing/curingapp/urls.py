from django.urls import path
from . import views
# from . import exeriment

urlpatterns = [
    #user
    path('', views.home),
    path('home/',views.home,name='home'), 
    path('loginuser/', views.login_user, name='loginuser'),
    path('logoutuser/',views.logout_user,name='logoutuser'),
    path('registeruser/',views.register_user,name='register_user'),
    path('change_password/',views.change_password,name='change_password'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    #Administrator Part
        #Project
    path('create_project/', views.create_project, name='create_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
        #Site
    path('create_site/', views.create_site, name='create_site'),
    path('get_sites_for_project/<int:project_id>/', views.get_sites_for_project, name='get_sites_for_project'),
    path('edit_site/<int:site_id>/', views.edit_site, name='edit_site'),
    path('delete_site/<int:site_id>/', views.delete_site, name='delete_site'),
        #Structural_element
    path('create_structural_element/', views.create_structural_element, name='create_structural_element'),
    path('edit_structural_element/<int:element_id>/', views.edit_structural_element, name='edit_structural_element'),
    path('delete_structural_element/<int:element_id>/', views.delete_structural_element, name='delete_structural_element'),

    #Scheduling Part 
    path('create_schedule_curing/<int:user_id>/', views.create_schedule_curing, name='create_schedule_curing'),
    path('schedule_curing_table/<int:transaction_concreting_id>/', views.schedule_curing_table, name='schedule_curing_table'),
    path('transaction_concreting/', views.transaction_concreting_list, name='transaction_concreting_list'),
    path('upload_image/', views.upload_image_view, name='upload_image'),
    path('get_image_list/', views.get_image_list, name='get_image_list'),

    #Experiment
    #path('camera/',exeriment.camera_view,name='camera_view' ),
    #path('exschedule_curing_table/<int:transaction_concreting_id>/', exeriment.schedule_curing_table, name='exschedule_curing_table'),

]