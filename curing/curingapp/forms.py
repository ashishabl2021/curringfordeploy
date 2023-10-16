from django import forms
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm
from .models import CustomUser, Transaction_Concreting,Project_Master,Site_Master,Structural_Element,Schedule_Curing # Updated model name
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import datetime

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'Contact_no', 'Project', 'Site','is_user','is_Administrator', 'password1', 'password2']

        # Make the password fields hidden
class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email',  'Contact_no', 'Project', 'Site','is_user','is_Administrator']
    

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Repeat New Password', widget=forms.PasswordInput())

class TransactionConcretingForm(forms.ModelForm):
    # Project = forms.CharField(max_length=100)
    # Site = forms.CharField(max_length=100)
    # Structural_Element = forms.CharField(max_length=100)

    class Meta:
        model = Transaction_Concreting  # Updated model name
        fields = ['Project', 'Site', 'Structural_Element', 'Schedule_Date_and_Time']
        labels = {
                'Structural_Element': '',
                'Schedule_Date_and_Time':'',
            }
    widgets = {
            'Project': forms.Select(attrs={'id': 'project-select'}),
            'Site': forms.Select(attrs={'id': 'site-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the initial value of Schedule_Date_and_Time to the current date and time
        self.fields['Schedule_Date_and_Time'].initial = datetime.now()
        self.fields['Schedule_Date_and_Time'].disabled = True
        self.fields['Project'].required = True
        self.fields['Site'].required = True

class ProjectForm(forms.ModelForm): 
    class Meta:
        model = Project_Master
        fields = ['Project_Name']

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site_Master
        fields = ['Site_Name', 'Project']

class StructuralElementForm(forms.ModelForm):
    class Meta:
        model = Structural_Element
        fields = ['Structural_Element', 'No_Of_Days', 'Frequency', 'Time_Bet_TwoCuring']

        labels = {
            'Time_Bet_TwoCuring': 'Time between Two Curing',
        }
    
class ScheduleCuringUpdateForm(forms.ModelForm):
    class Meta:
        model = Schedule_Curing
        fields = ['Image_Of_Curing', 'Status']

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

    # def clean_schedule_entry_id(self):
    #     schedule_entry_id = self.cleaned_data['schedule_entry_id']
    #     # You can add validation here to ensure the schedule entry exists and belongs to the user.
    #     return schedule_entry_id
