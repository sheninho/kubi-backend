from django.urls import path

from listing360.views.property_views import CreatePropertyView, CategoryListCreateView, \
    CategoryRetrieveUpdateDestroyView, DistrictListCreateView, DistrictRetrieveUpdateDestroyView, \
    PropertyListCreateView, PropertyRetrieveUpdateDestroyView, CityListCreateView, CityRetrieveUpdateDestroyView, \
    CategoryFieldsView
from listing360.views.user_views import (
    UserRegistrationView,
    UserLogoutView,
    ResendCodeView,
    ActivateAccountView,
    TimeRemainingView,
    VerifyCodeView,
    ChangePasswordView, LoginView, TokenRefreshView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('activate-account/', ActivateAccountView.as_view(), name='activate-account'),
    path('time-remaining/', TimeRemainingView.as_view(), name='time-remaining'),
    path('resend-code/', ResendCodeView.as_view(), name='resend-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('properties/create/', CreatePropertyView.as_view(), name='create_property'),

    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),
    path('districts/', DistrictListCreateView.as_view()),
    path('districts/<int:pk>/', DistrictRetrieveUpdateDestroyView.as_view()),
    path('properties/', PropertyListCreateView.as_view()),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view()),
    path('cities/', CityListCreateView.as_view(), name='city-list-create'),
    path('cities/<int:pk>/', CityRetrieveUpdateDestroyView.as_view(), name='city-retrieve-update-destroy'),
    path('category/<int:category_id>/fields/', CategoryFieldsView.as_view(), name='category-fields'),
]