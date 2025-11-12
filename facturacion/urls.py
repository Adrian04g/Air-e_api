from django.urls import path

from . import views

urlpatterns = [
    path('', views.FacturaListCreateView.as_view(), name='factura-list-create'),
    path('<int:pk>/', views.FacturaDetailView.as_view(), name='factura-detail'),
    #path('facturas/por-cableoperador/', views.FacturaByCableoperadorView.as_view(), name='factura-by-cableoperador'),
    
    # Registros de Pago
    path('pagos/', views.RegistroPagoListCreateView.as_view(), name='pago-list-create'),
    path('pagos/<int:pk>/', views.RegistroPagoDetailView.as_view(), name='pago-detail'),
    #path('pagos/por-factura/', views.RegistroPagoByFacturaView.as_view(), name='pago-by-factura'),
]