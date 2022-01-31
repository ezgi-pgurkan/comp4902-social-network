from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account, Profile


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('email', 'username', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account.email)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Email {username} is already in use.')


    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('profile', 'about', 'tech_stack', 'learning', 'hobbies', 'music', 'tvshows', 'movies', 'books')
        widgets = {
                    'profile': forms.TextInput(attrs={'class': 'form-conrol', 'value':'', 'id': 'elder2', 'type':'hidden'}),
                    'about': forms.Textarea(attrs={ 'cols':50, 'rows':2, 'placeholder': 'Your self-summary...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    'tech_stack': forms.Textarea(attrs={'cols':50, 'rows':2,  'placeholder': 'The programming languages, frameworks, and tools that you currently know/use...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    'learning': forms.Textarea(attrs={'cols':50, 'rows':2,  'placeholder': 'The programming languages, frameworks, and tools that you are learning at the moment...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    'hobbies': forms.Textarea(attrs={ 'cols':50, 'rows':2, 'placeholder': 'Your interests/hobbies...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    'music': forms.Textarea(attrs={ 'cols':50, 'rows':2, 'placeholder': 'Your favorite music...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    'tvshows': forms.Textarea(attrs={ 'cols':50, 'rows':2, 'placeholder': 'Your favorite movies...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    'movies': forms.Textarea(attrs={ 'cols':50, 'rows':2,'placeholder': 'Your favorite movies...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    'books': forms.Textarea(attrs={'cols':50, 'rows':2, 'placeholder': 'Your favorite books...', 'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                  }