from django import forms
from .models import User, Review, Task, Team, TeamMember, MyTask

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['LastName', 'FirstName', 'Email', 'password']

class AuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'text']

class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        (1, 'P1'),
        (2, 'P2'),
        (3, 'P3'),
    ]
    Priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
    )
    class Meta:
        model = Task
        fields = ['Title', 'Description', 'Priority', 'Start', 'End', 'AssignedUser']

        widgets = {
            'Start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'End': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }




class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['TeamName']

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['user']

class AddTaskuser(forms.ModelForm):
    PRIORITY_CHOICES = [
        (1, 'P1'),
        (2, 'P2'),
        (3, 'P3'),
    ]
    Priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
    )
    class Meta:
        model = MyTask
        fields = ['Title', 'Description','Priority','Start','End']

        widgets = {
            'Start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'End': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }