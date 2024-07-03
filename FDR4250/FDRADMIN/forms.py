from django import forms
from .models import Club, District, Country, RotaryYearFile, ClubReport,RotaryYear, ClubBudget

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'district', 'country', 'enabled']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['country'].queryset = Country.objects.filter(district__id=district_id).distinct()
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['country'].queryset = self.instance.district.countries.distinct()

class RotaryYearFileForm(forms.ModelForm):
    class Meta:
        model = RotaryYearFile
        fields = ['file']

class ClubReportForm(forms.ModelForm):
    class Meta:
        model = ClubReport
        fields = ['file']

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'country', 'district', 'enabled', 'users']

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['zone', 'district_name', 'countries']

class RotaryYearForm(forms.ModelForm):
    class Meta:
        model = RotaryYear
        fields = ['year', 'rotary_full_year', 'is_closed', 'notice']

class ClubBudgetForm(forms.ModelForm):
    class Meta:
        model = ClubBudget
        fields = ['club', 'rotary_year', 'amount', 'description']