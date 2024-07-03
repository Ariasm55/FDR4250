from django.urls import path
from .views import (
    landing_page,
    upload_admin_file,
    upload_club_report,
    authorize_club_report,
    club_dashboard,
    rotaryyear_detail,
    ClubListView,
    ClubDetailView,
    ClubCreateView,
    ClubUpdateView,
    CountryListView,
    CountryDetailView,
    CountryCreateView,
    CountryUpdateView,
    DistrictListView,
    DistrictDetailView,
    DistrictCreateView,
    DistrictUpdateView,
    RotaryYearListView,
    RotaryYearDetailView,
    RotaryYearCreateView,
    RotaryYearUpdateView,
    ClubBudgetListView,
    ClubBudgetDetailView,
    ClubBudgetCreateView,
    ClubBudgetUpdateView,
    RotaryYearFileListView,
    RotaryYearFileCreateView,
    upload_admin_file,
    rotaryyear_detail,
    RotaryYearUpdateView,
    download_file,
    view_pdf,
    serve_pdf,
    superadmin_dashboard,  # SuperAdmin Dashboard
    get_countries_for_district,  # API for countries
)

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('dashboard/', club_dashboard, name='club-dashboard'),
    path('superadmin-dashboard/', superadmin_dashboard, name='superadmin-dashboard'),  # SuperAdmin Dashboard
    #path('rotaryyear/<int:year_id>/upload_admin_file/', upload_admin_file, name='upload-admin-file'),
    #path('rotaryyear/<int:year_id>/club/<int:club_id>/upload_report/', upload_club_report, name='upload-club-report'),
    path('authorize_report/<int:report_id>/', authorize_club_report, name='authorize-club-report'),


    #path('rotaryyear/<int:pk>/', rotaryyear_detail, name='rotaryyear-detail'),
    #path('rotaryyear/<int:pk>/update/', RotaryYearUpdateView.as_view(), name='rotaryyear-update'),
    #path('rotaryyear/<int:year_id>/files/', RotaryYearFileListView.as_view(), name='rotaryyearfile-list'),
    #path('rotaryyear/<int:year_id>/files/upload/', RotaryYearFileCreateView.as_view(), name='rotaryyearfile-upload'),
    #path('rotaryyear/<int:year_id>/upload_admin_file/', upload_admin_file, name='upload-admin-file'),
    path('rotaryyears/', RotaryYearListView.as_view(), name='rotaryyear-list'),  # Added this line
    
    path('clubs/', ClubListView.as_view(), name='club-list'),
    path('clubs/<int:pk>/', ClubDetailView.as_view(), name='club-detail'),
    path('clubs/create/', ClubCreateView.as_view(), name='club-create'),
    path('clubs/<int:pk>/update/', ClubUpdateView.as_view(), name='club-update'),
    
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
    path('countries/create/', CountryCreateView.as_view(), name='country-create'),
    path('countries/<int:pk>/update/', CountryUpdateView.as_view(), name='country-update'),
    
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('districts/<int:pk>/', DistrictDetailView.as_view(), name='district-detail'),
    path('districts/create/', DistrictCreateView.as_view(), name='district-create'),
    path('districts/<int:pk>/update/', DistrictUpdateView.as_view(), name='district-update'),
    

    path('clubbudgets/', ClubBudgetListView.as_view(), name='clubbudget-list'),
    path('clubbudgets/<int:pk>/', ClubBudgetDetailView.as_view(), name='clubbudget-detail'),
    path('clubbudgets/create/', ClubBudgetCreateView.as_view(), name='clubbudget-create'),
    path('clubbudgets/<int:pk>/update/', ClubBudgetUpdateView.as_view(), name='clubbudget-update'),


    path('rotaryyear/<int:pk>/', rotaryyear_detail, name='rotaryyear-detail'),
    path('rotaryyear/<int:pk>/update/', RotaryYearUpdateView.as_view(), name='rotaryyear-update'),
    path('rotaryyear/<int:year_id>/files/', RotaryYearFileListView.as_view(), name='rotaryyearfile-list'),
    path('rotaryyear/<int:year_id>/files/upload/', RotaryYearFileCreateView.as_view(), name='rotaryyearfile-upload'),
    path('rotaryyear/<int:year_id>/upload_admin_file/', upload_admin_file, name='upload-admin-file'),
    path('rotaryyear/<int:year_id>/club/<int:club_id>/upload_report/', upload_club_report, name='upload-club-report'),
    

    # API endpoints
    path('api/countries/<int:district_id>/', get_countries_for_district, name='get-countries-for-district'),


   path('file/<int:file_id>/view/', view_pdf, name='file-view'),
    path('file/<int:file_id>/download/', download_file, name='file-download'),
    path('file/<int:file_id>/serve/', serve_pdf, name='file-serve'),
]
