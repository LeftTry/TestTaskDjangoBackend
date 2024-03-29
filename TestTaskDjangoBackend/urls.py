from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from SystemForStudy.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products', ProductsAPIView.as_view(), name='get_products'),
    path('api/products/lessons', GetLessonsAPIView.as_view(), name='get_lessons'),
    path('api/products/quantity_of_students', GetQuantityOfStudentsAPIView.as_view(),
         name='get_quantity_of_students'),
    path('api/products/percent_of_fullness', GetPercentOfFullnessPerGroupAPIView.as_view(),
         name='percent_of_fullness'),
    path('api/products/buying_rating', GetProductBuyingRatingAPIView.as_view(),
         name='product_buying_rating'),
    path('api/student', StudentAPIView.as_view(),
         name='register_student_for_product'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
