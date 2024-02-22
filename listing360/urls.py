from django.urls import path

from listing360.views.property_views import CreatePropertyView, CategoryListCreateView, \
    CategoryRetrieveUpdateDestroyView, DistrictListCreateView, DistrictRetrieveUpdateDestroyView, \
    PropertyListCreateView, PropertyRetrieveUpdateDestroyView, CityListCreateView, CityRetrieveUpdateDestroyView, \
    CategoriesByPropertyTypeView, CityDistrictsListView, PropertyUpdateView, \
    PropertyCategoryFieldsView, ShortTextFieldRetrieveUpdateDestroyAPIView, ShortTextFieldListCreateAPIView, \
    LongTextFieldRetrieveUpdateDestroyAPIView, LongTextFieldListCreateAPIView, SelectFieldListCreateAPIView, \
    SelectFieldRetrieveUpdateDestroyAPIView, DateFieldListCreateAPIView, DateFieldRetrieveUpdateDestroyAPIView, \
    IntegerFieldListCreateAPIView, IntegerFieldRetrieveUpdateDestroyAPIView, FieldListView
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

    path('categories-by-property-type/', CategoriesByPropertyTypeView.as_view(), name='categories-by-property-type'),
    path('cities-with-districts/', CityDistrictsListView.as_view(), name='cities-with-districts'),
    path('properties/update/<int:property_id>/', PropertyUpdateView.as_view(), name='property-update'),
    path('properties/<int:property_id>/fields/', PropertyCategoryFieldsView.as_view(), name='property-category-fields'),
    path('districts/', DistrictListCreateView.as_view()),
    path('districts/<int:pk>/', DistrictRetrieveUpdateDestroyView.as_view()),
    path('properties/', PropertyListCreateView.as_view()),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view()),
    path('cities/', CityListCreateView.as_view(), name='city-list-create'),
    path('cities/<int:pk>/', CityRetrieveUpdateDestroyView.as_view(), name='city-retrieve-update-destroy'),

    path('shorttextfields/', ShortTextFieldListCreateAPIView.as_view(), name='shorttextfields-list-create'),
    path('shorttextfields/<int:pk>/', ShortTextFieldRetrieveUpdateDestroyAPIView.as_view(), name='shorttextfields-detail'),
    path('longtextfields/', LongTextFieldListCreateAPIView.as_view(), name='longtextfields-list-create'),
    path('longtextfields/<int:pk>/', LongTextFieldRetrieveUpdateDestroyAPIView.as_view(), name='longtextfields-detail'),
    path('selectfields/', SelectFieldListCreateAPIView.as_view(), name='selectfield-list-create'),
    path('selectfields/<int:pk>/', SelectFieldRetrieveUpdateDestroyAPIView.as_view(), name='selectfield-detail'),
    path('datefields/', DateFieldListCreateAPIView.as_view(), name='datefield-list-create'),
    path('datefields/<int:pk>/', DateFieldRetrieveUpdateDestroyAPIView.as_view(), name='datefield-detail'),
    path('integerfields/', IntegerFieldListCreateAPIView.as_view(), name='integerfield-list-create'),
    path('integerfields/<int:pk>/', IntegerFieldRetrieveUpdateDestroyAPIView.as_view(), name='integerfield-detail'),
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),
    path('fields/', FieldListView.as_view(), name='field-list'),

]