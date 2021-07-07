from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('Customers/', views.customers, name="customers"),
    path('ViewCustomers/<str:id>', views.viewcustomers, name="viewcustomers"),
    path('EditCustomers/<str:id>', views.editcustomers, name="editcustomers"),
    path('DeleteCustomers/<str:id>', views.deletecustomers, name="deletecustomers"),
    path('DownloadPDF/<str:id>', views.downloadPDF, name="downloadPDF"),
    
    path('Payment/<str:id>', views.copylink, name="copylink"),
	path('charge', views.charge, name="charge"),
	path('success/<str:args>', views.successMesg, name="success"),

    path('Search/',views.search,name='search'),
    # path('DownloadPDF/<str:id>', views.downloadPDF, name="downloadPDF"),
    path('Projects/', views.projects, name="projects"),
    path('Tasks/', views.tasks, name="tasks"),

    path('SalesReport/', views.salesReport, name="salesReport"),
    path('SalesAPI/', views.salesAPI, name="salesAPI"),
    path('SalesSlab/', views.salesSlab, name="salesSlab"),

    path('Catalog/', views.catalog, name="catalog"),

    path('signin/',views.signin,name="signin"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.handlelogout,name='handlelogout'),
]