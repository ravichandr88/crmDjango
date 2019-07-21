from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


from .models import Lead_List



class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100,help_text = 'Required')
    first_name = forms.CharField(max_length=100, help_text='Required')
    last_name = forms.CharField(max_length=100, help_text='Optional')
    email = forms.EmailField()
    designation = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','designation', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,help_text='Required<br>')
    password = forms.CharField(max_length=100,help_text='Required<br>')

    class Meta:
        fields = ('username','password')

class Lead_List_form(forms.ModelForm):
    # name 
    # phone_number
    # email 
    # address 
    # nxt_flw_dt 
    # dob 
    # user_fllwng  
    # status 
    # created_dt 
    # campaign 
    # enquired_for 
    # degree 
    # yop 
    # marks 
    # brnch_loc 
    # tchngly_lk_fr 
    class Meta:
        model =  Lead_List
        exclude = ('user_fllwng',)
    
    def validate(self):
        phn_nmbr = self.cleaned_data.get('phone_number')
        if len(phn_nmbr) is not 10:
            return 'Enter valid phone number'
        elif Lead_List.objects.filter(phone_number = phn_nmbr).count()  != 0:
            return "Lead already exits with this phone number"
        else :
            return True





