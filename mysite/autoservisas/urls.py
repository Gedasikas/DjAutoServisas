from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymaiListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymai_detail'),
    path('paslaugos/', views.paslaugos, name='paslaugos'),
    path('paslaugos/<int:paslauga_id>', views.paslauga, name='paslauga'),
    path('search/', views.search, name='search'),
    path('search/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('manouzsakymai/', views.UzsakymasByUserListView.as_view(), name='manouzsakymai'),
    path('register/', views.register, name='register'),
]