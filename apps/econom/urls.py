from django.urls import path
from apps.econom.views import SectionView, WalletListView, WalletView, SectionListView, CostCategoryListView, CostCategoryView, IncomeCategoryListView

urlpatterns = [
    path('section/', SectionListView.as_view()),
    path('section/<int:pk>/', SectionView.as_view()),
    path('section/<int:id_section>/wallet/', WalletListView.as_view()),
    path('section/<int:id_section>/wallet/<int:pk>/', WalletView.as_view()),
    path('section/<int:id_section>/cost/category/', CostCategoryListView.as_view()),
    path('section/<int:id_section>/cost/category/<int:pk>/', CostCategoryView.as_view()),
    path('section/<int:id_section>/income/category/', IncomeCategoryListView.as_view()),
]