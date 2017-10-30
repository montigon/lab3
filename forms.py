from django import forms
import requests


class AuthForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label="Password")


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label="Email Adress")
    confirm_email = forms.EmailField(label="Confirm Email")
    password = forms.CharField(label="Password")


users = requests.get("http://127.0.0.1:8000/users/")
usersch = [(u["id"], u["username"]) for u in users.json()]


class PostToDoListForm(forms.Form):
    name = forms.CharField(label="Name")
    share = forms.MultipleChoiceField(label="Share with", choices=usersch, required=False)


class TasklistDetailForm(forms.Form):
    name = forms.CharField(label="Name")
    share = forms.MultipleChoiceField(label="Share with", choices=usersch, required=False)


tags = requests.get("http://127.0.0.1:8000/tags/")
tagsch = [(t["id"], t["name"]) for t in tags.json()]



class PostTaskForm(forms.Form):
    name = forms.CharField(label="Name")
    description = forms.CharField(label="Description")
    completed = forms.BooleanField(label="Completed", required=False)
    due_date = forms.DateField(label="Due date")
    priority = forms.ChoiceField(label="Priotity", choices=[("h", "heigh"), ("m", "medium"), ("l", "low")], required=False)
    tags = forms.MultipleChoiceField(label="Tags", choices=tagsch, required=False)


class TagForm(forms.Form):
    name = forms.CharField(label="Name")
