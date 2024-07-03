import logging
import os
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.http import FileResponse, HttpResponseForbidden

from .models import RotaryYear, RotaryYearFile, ClubReport, Club, Country, District, ClubBudget
from .forms import RotaryYearFileForm, ClubReportForm, ClubForm, CountryForm, DistrictForm, RotaryYearForm, ClubBudgetForm
from django.contrib.auth import logout
from django.urls import reverse


logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_superuser

def is_club_user(user):
    return user.clubs.exists()

def landing_page(request):
    return render(request, 'FDRADMIN/landing_page.html')

@login_required
def download_file(request, file_id):
    file = get_object_or_404(RotaryYearFile, id=file_id)
    response = FileResponse(file.file.open(), as_attachment=True)
    return response



@login_required
def upload_club_report(request, year_id, club_id):
    rotary_year = get_object_or_404(RotaryYear, id=year_id)
    club = get_object_or_404(Club, id=club_id)
    if request.method == 'POST':
        form = ClubReportForm(request.POST, request.FILES)
        if form.is_valid():
            club_report = form.save(commit=False)
            club_report.rotary_year = rotary_year
            club_report.club = club
            club_report.save()
            return redirect('club-dashboard')
    else:
        form = ClubReportForm()
    return render(request, 'FDRADMIN/upload_club_report.html', {'form': form, 'rotary_year': rotary_year, 'club': club})

@login_required
@user_passes_test(is_admin)
def authorize_club_report(request, report_id):
    club_report = get_object_or_404(ClubReport, id=report_id)
    if request.method == 'POST':
        club_report.is_authorized = True
        club_report.save()
        return redirect('rotaryyear-detail', pk=club_report.rotary_year_id)
    return render(request, 'FDRADMIN/authorize_club_report.html', {'club_report': club_report})

@login_required
def club_dashboard(request):
    club = get_object_or_404(Club, users=request.user)
    reports = ClubReport.objects.filter(club=club)
    active_years = RotaryYear.objects.filter(is_closed=False)
    past_years = RotaryYear.objects.filter(is_closed=True)
    budgets = ClubBudget.objects.filter(club=club)  # Assuming budgets are implemented

    # Fetching files published by superadmin
    superadmin_files = RotaryYearFile.objects.all()

    if request.method == 'POST':
        rotary_year = get_object_or_404(RotaryYear, id=request.POST.get('year_id'))
        form = ClubReportForm(request.POST, request.FILES)
        if form.is_valid():
            club_report = form.save(commit=False)
            club_report.rotary_year = rotary_year
            club_report.club = club
            club_report.save()
            return redirect('club-dashboard')
    else:
        form = ClubReportForm()

    return render(request, 'FDRADMIN/club_dashboard.html', {
        'club': club,
        'reports': reports,
        'active_years': active_years,
        'past_years': past_years,
        'budgets': budgets,
        'superadmin_files': superadmin_files,
        'form': form,
    })



#@login_required
#@user_passes_test(is_club_user)
##def club_dashboard(request):
 #   club = request.user.clubs.first()
 #   active_years = RotaryYear.objects.filter(is_closed=False)
 #   past_years = RotaryYear.objects.filter(is_closed=True)
 #   budgets = ClubBudget.objects.filter(club=club)

  #  if request.method == 'POST':
   #     year_id = request.POST.get('year_id')
    #    form = ClubReportForm(request.POST, request.FILES)
     #   if form.is_valid():
      #      rotary_year = get_object_or_404(RotaryYear, id=year_id)
       #     club_report = form.save(commit=False)
        #    club_report.club = club
         #   club_report.rotary_year = rotary_year
          #  club_report.save()
           # return redirect('club-dashboard')
    #else:
    #    form = ClubReportForm()

    #return render(request, 'FDRADMIN/club_dashboard.html', {
    #    'club': club,
    #    'active_years': active_years,
    #    'past_years': past_years,
    #    'budgets': budgets,
    #    'form': form
    #})

@login_required
def rotaryyear_detail(request, pk):
    try:
        rotary_year = get_object_or_404(RotaryYear, pk=pk)
        files = RotaryYearFile.objects.filter(rotary_year=rotary_year)
        reports = ClubReport.objects.filter(rotary_year=rotary_year).select_related('club')
        clubs = Club.objects.all()  # Fetch all clubs or filter as needed
        budgets = ClubBudget.objects.filter(rotary_year=rotary_year)  # Assuming budgets are implemented

        form = RotaryYearFileForm()

        return render(request, 'FDRADMIN/rotaryyear_detail.html', {
            'rotary_year': rotary_year,
            'files': files,
            'reports': reports,
            'clubs': clubs,
            'budgets': budgets,
            'form': form
        })
    except Exception as e:
        logger.error(f"Error in rotaryyear_detail: {e}")
        return HttpResponseServerError("Internal Server Error")

@method_decorator([login_required], name='dispatch')
class ClubListView(ListView):
    model = Club
    template_name = 'FDRADMIN/club_list.html'

@method_decorator([login_required], name='dispatch')
class ClubDetailView(DetailView):
    model = Club
    template_name = 'FDRADMIN/club_detail.html'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ClubCreateView(CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'FDRADMIN/club_form.html'
    success_url = '/clubs/'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ClubUpdateView(UpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'FDRADMIN/club_form.html'
    success_url = '/clubs/'

@method_decorator([login_required], name='dispatch')
class CountryListView(ListView):
    model = Country
    template_name = 'FDRADMIN/country_list.html'

@method_decorator([login_required], name='dispatch')
class CountryDetailView(DetailView):
    model = Country
    template_name = 'FDRADMIN/country_detail.html'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm
    template_name = 'FDRADMIN/country_form.html'
    success_url = '/countries/'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm
    template_name = 'FDRADMIN/country_form.html'
    success_url = '/countries/'

@method_decorator([login_required], name='dispatch')
class DistrictListView(ListView):
    model = District
    template_name = 'FDRADMIN/district_list.html'

@method_decorator([login_required], name='dispatch')
class DistrictDetailView(DetailView):
    model = District
    template_name = 'FDRADMIN/district_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        district = self.object
        context['countries'] = district.countries.all()
        context['clubs'] = Club.objects.filter(district=district)
        return context

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class DistrictCreateView(CreateView):
    model = District
    form_class = DistrictForm
    template_name = 'FDRADMIN/district_form.html'
    success_url = '/districts/'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class DistrictUpdateView(UpdateView):
    model = District
    form_class = DistrictForm
    template_name = 'FDRADMIN/district_form.html'
    success_url = '/districts/'

@method_decorator([login_required], name='dispatch')
class RotaryYearListView(ListView):
    model = RotaryYear
    template_name = 'FDRADMIN/rotaryyear_list.html'
    context_object_name = 'rotary_years'

@method_decorator([login_required], name='dispatch')
class RotaryYearDetailView(DetailView):
    model = RotaryYear
    template_name = 'FDRADMIN/rotaryyear_detail.html'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class RotaryYearCreateView(CreateView):
    model = RotaryYear
    form_class = RotaryYearForm
    template_name = 'FDRADMIN/rotaryyear_form.html'
    success_url = '/rotaryyears/'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class RotaryYearUpdateView(UpdateView):
    model = RotaryYear
    form_class = RotaryYearForm
    template_name = 'FDRADMIN/rotaryyear_form.html'
    success_url = '/rotaryyear/'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ClubBudgetCreateView(CreateView):
    model = ClubBudget
    form_class = ClubBudgetForm
    template_name = 'FDRADMIN/clubbudget_form.html'
    success_url = '/clubbudgets/'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ClubBudgetUpdateView(UpdateView):
    model = ClubBudget
    form_class = ClubBudgetForm
    template_name = 'FDRADMIN/clubbudget_form.html'
    success_url = '/clubbudgets/'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ClubBudgetListView(ListView):
    model = ClubBudget
    template_name = 'FDRADMIN/clubbudget_list.html'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ClubBudgetDetailView(DetailView):
    model = ClubBudget
    template_name = 'FDRADMIN/clubbudget_detail.html'

@login_required
@user_passes_test(is_admin)
def superadmin_dashboard(request):
    clubs = Club.objects.all()
    rotary_years = RotaryYear.objects.all()
    return render(request, 'FDRADMIN/superadmin_dashboard.html', {'clubs': clubs, 'rotary_years': rotary_years})

# API to get countries for a district
def get_countries_for_district(request, district_id):
    try:
        district = District.objects.get(pk=district_id)
        countries = district.countries.all()
        countries_list = list(countries.values('id', 'name'))
        return JsonResponse(countries_list, safe=False)
    except District.DoesNotExist:
        return JsonResponse([], safe=False)
    
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def upload_admin_file(request, year_id):
    rotary_year = get_object_or_404(RotaryYear, id=year_id)
    if request.method == 'POST':
        form = RotaryYearFileForm(request.POST, request.FILES)
        if form.is_valid():
            rotary_year_file = form.save(commit=False)
            rotary_year_file.rotary_year = rotary_year
            rotary_year_file.save()
            return redirect('rotaryyear-detail', pk=year_id)
    else:
        form = RotaryYearFileForm()
    return render(request, 'FDRADMIN/upload_admin_file.html', {'form': form, 'rotary_year': rotary_year})


@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class RotaryYearFileListView(ListView):
    model = RotaryYearFile
    template_name = 'FDRADMIN/rotaryyearfile_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        return RotaryYearFile.objects.filter(rotary_year_id=self.kwargs['year_id'])

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class RotaryYearFileCreateView(CreateView):
    model = RotaryYearFile
    form_class = RotaryYearFileForm
    template_name = 'FDRADMIN/rotaryyearfile_form.html'

    def form_valid(self, form):
        form.instance.rotary_year_id = self.kwargs['year_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rotaryyear-detail', kwargs={'pk': self.kwargs['year_id']})


@login_required
def view_pdf(request, file_id):
    file = get_object_or_404(ClubReport, id=file_id)
    if request.method == 'POST' and request.user.is_superuser:
        if 'authorize' in request.POST:
            file.approve()
        elif 'decline' in request.POST:
            file.decline()
        return redirect('rotaryyear-detail', pk=file.rotary_year.id)

    return render(request, 'FDRADMIN/view_pdf.html', {'file': file})

@login_required
@user_passes_test(is_admin)
def serve_pdf(request, file_id):
    file = get_object_or_404(RotaryYearFile, id=file_id)
    response = FileResponse(file.file.open(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}"'.format(file.file.name)
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response