"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from epicevent.views import contract_list, sales_contact_list
from api.views import LoginUser, UsersViewSet, ClientViewSet, ContractViewSet, EventViewSet, \
    MissingClientSales, MissingEventSupport, PotentialClients, ComingEventViewSet, SupportEvents
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', UsersViewSet)
router.register('client', ClientViewSet)
router.register('contract', ContractViewSet)
router.register('event', EventViewSet)
router.register('comingevent', ComingEventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginUser.as_view()),
    path('get/contracts/<client_id>/', contract_list),
    path('get/sales/<client_id>/', sales_contact_list),
    path('api/client/nosales/', MissingClientSales.as_view()),
    path('api/client/potential/', PotentialClients.as_view()),
    path('api/event/nosupport/', MissingEventSupport.as_view()),
    path('api/event/supportevent/', SupportEvents.as_view()),
    path('api/', include(router.urls)),
]
