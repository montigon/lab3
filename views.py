import requests
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import AuthForm, RegisterForm, TasklistDetailForm, PostToDoListForm, PostTaskForm, TagForm
from django.shortcuts import render
from types import *
from django import forms
from django.core.mail import send_mail


query = "http://127.0.0.1:8000"
token = ""


def auth(request):
    #global query
    global token
    token = ""
    valid = ""
    #query += request.get_full_path()
    #esp = requests.post('http://127.0.0.1:8000/newauth/', {'username': "AAAAA", 'password': "AAAAA11111"})
    #response = requests.get('http://127.0.0.1:8000/todolists/', 'Authorization: Token ' + str(esp))
    if request.method == 'POST':
        form = AuthForm(request.POST)
        postD = {'username': str(form.data['username']), 'password': str(form.data['password'])}
        token = requests.post('http://127.0.0.1:8000/newauth/', postD).json()#{'username': "AAAAA", 'password': "AAAAA11111"}# )
        if "token" in token:
            token = token["token"]
            return HttpResponseRedirect("/todolists/")
        else:
            form = AuthForm()
            valid = "Введите корректные данные"
            return render(request, 'template_auth.html', {'form': form, 'valid': valid})
    else:
        form = AuthForm()
    return render(request, 'template_auth.html', {'form': form, 'valid': valid})


def register(request):
    global token, log
    if token != "":
        return render(request, 'template_alreadyauth.html')
    valid = ""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        postD = {'username': str(form.data['username']),
                 'email': str(form.data['email']),
                 'email2': str(form.data['confirm_email']),
                'password': str(form.data['password'])}
        resp = requests.post('http://127.0.0.1:8000/register/', postD)
        resp = resp.json()
        postD22222 = {'username': str(postD['username']), 'password': str(postD['password'])}
        postD.pop('password')
        if postD == resp:

            token = requests.post('http://127.0.0.1:8000/newauth/', postD22222).json()  # {'username': "AAAAA", 'password': "AAAAA11111"}# )
            token = token["token"]
            print(token)

            send_mail("registration", "Вы зарегистрировались, молодцы, всего вам хорошего", 'mister.0025@yandex.ru', [postD["email"],], fail_silently=False)

            return HttpResponseRedirect("/todolists/")
        else:
            form = RegisterForm()
            valid = set(a[0] for a in resp.values())

            return render(request, 'template_register.html', {'form': form, 'valid': valid})
    else:
        form = RegisterForm()
    return render(request, 'template_register.html', {'form': form, 'valid': valid})



def getToDoList(request):
    #global query
    global token
    form = ""
    #query += request.get_full_path()
    response = requests.get("http://127.0.0.1:8000/todolists/", headers={'Authorization' : 'Token ' + token})
    responseJSON = response.json()
    if request.method == "POST":
        form = PostToDoListForm(request.POST)
        named = str(form.data["name"])
        try:
            shared = form.data["share"]
        except:
            shared = None
        postTasklist(named, shared)
        return HttpResponseRedirect("/todolists/")
    elif responseJSON == []:
        form = PostToDoListForm()
        templ = "No tasklists"
        return render(request, 'template_todolists.html', {'todolist': templ, "form": form})
    elif "detail" in responseJSON:
        return HttpResponseRedirect("/newauth/")
    else:
        form = PostToDoListForm
        templ = []
        for tasklist in responseJSON:
            templ.append((tasklist['id'], tasklist['name'], tasklist['tasks']))

        return render(request, 'template_todolists.html', {'todolist': templ, "form": form})

    #return HttpResponse(responseJSON)#return render(request, 'template_todolists.html', {'todolist': responseJSON})


def DetailTasklist(request, pk = 1):
    global token
    response = requests.get("http://127.0.0.1:8000/todolists/" + str(pk) + '/', headers={'Authorization': 'Token ' + token})
    responseJSON = response.json()
    id = responseJSON["id"]
    name = responseJSON["name"]
    tasks = responseJSON["tasks"]
    sharedWith = responseJSON["sharedName"]
    form = TasklistDetailForm({"name": name})
    if request.method == "POST":
        if "DDD" in request.POST:
            deleteTasklist(pk)
            return HttpResponseRedirect("/todolists/")

        else:
            form = TasklistDetailForm(request.POST)
            if form.is_valid():
                name = str(form.data["name"])
                try:
                    shared = form.cleaned_data["share"]
                except:
                    shared = None
                #print(name)
                putData = {"name": name, "shared": shared}#, "tasks": tasks}
                requests.put("http://127.0.0.1:8000/todolists/" + str(pk) + '/', putData, headers={'Authorization' : 'Token ' + token})

            response = requests.get("http://127.0.0.1:8000/todolists/" + str(pk) + '/', headers={'Authorization': 'Token ' + token})
            responseJSON = response.json()
            id = responseJSON["id"]
            name = responseJSON["name"]
            tasks = responseJSON["tasks"]
            sharedWith = responseJSON["sharedName"]

            form = TasklistDetailForm({"name": name})
            return render(request, 'template_detailtasklist.html', {"tasklist": name, "tasks": tasks, "shared": sharedWith, "form": form, "pk": id})

    return render(request, 'template_detailtasklist.html', {"tasklist": name, "tasks": tasks, "shared": sharedWith, "form": form, "pk": id})


    #return render(request, 'template_detailtasklist.html', {"resp": responseJSON, "form": form})


def getTasks(request, list_id = 1):
    global token, tagsCh
    response = requests.get("http://127.0.0.1:8000/todolists/" + str(list_id) + "/tasks/", headers={'Authorization': 'Token ' + token})
    responseJSON = response.json()
    if request.method == "POST":

        form = PostTaskForm(request.POST)
        if form.is_valid():
            name = form.data["name"]
            desc = form.data["description"]
            try:
                compl = form.data["completed"]
            except:
                compl = False
            dd = form.data["due_date"]
            pr = form.data["priority"]
            t = form.cleaned_data["tags"]
            print(t)
            postTask(list_id, name, desc, compl, dd, pr, t)
            return HttpResponseRedirect("/todolists/" + str(list_id) + "/tasks/")

    else:
        #КАК ДОБАВИТЬ ТЭГИ БЛ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """resp = requests.get("http://127.0.0.1:8000/tags/", headers={'Authorization': 'Token ' + token})
        resp = resp.json()
        tagsCh = [(t["name"], t["name"]) for t in resp]"""

        form = PostTaskForm()
        templ = []
        for task in responseJSON:
            templ.append((list_id, task["id"], task["name"], task["description"], task["completed"], task["date_created"], task["due_date"], task["priority"], task["tags"]))
        return render(request, 'template_tasks.html', {"tasks": templ, "form": form})



def postTasklist(name, shared):
    requests.post("http://127.0.0.1:8000/todolists/", {"name": name, "shared": shared}, headers={'Authorization' : 'Token ' + token})
    #return HttpResponseRedirect("/todolists/")


def postTask(list_id, name, desc, compl = False, dued = None, pr = "h", tags = []):
    print(tags, "erweewffdsf")
    postData = {"name": name,
        "description": desc,
        "completed": compl,
        "due_date": dued,
        "priority": pr,
        "tag": tags }
    print(postData["tag"])
    requests.post("http://127.0.0.1:8000/todolists/" + str(list_id) + "/tasks/", postData, headers={'Authorization': 'Token ' + token})


def Shared(request):
    global token
    response = requests.get("http://127.0.0.1:8000/todolists/", headers={'Authorization': 'Token ' + token})
    responseJSON = response.json()[0]
    print(responseJSON)
    tasklists = responseJSON["sharedTasklists"]
    return render(request, 'template_sharedtl.html', {"tasklists": tasklists})


def TaskDetail(request, list_id, pk):
    global token
    response = requests.get("http://127.0.0.1:8000/todolists/{list_id}/tasks/{pk}/".format(list_id=list_id, pk=pk),
                            headers={'Authorization': 'Token ' + token})
    responseJSON = response.json()
    id = responseJSON["id"]
    name = responseJSON["name"]
    desc = responseJSON["description"]
    compl = responseJSON["completed"]
    dd = responseJSON["due_date"]
    pr = responseJSON["priority"]
    t = responseJSON["tags"]
    if request.method == "POST":
        if "Delete" in request.POST:
            deleteTask(list_id, pk)
            return HttpResponseRedirect("/todolists/{list_id}/tasks/".format(list_id=list_id))
        form = PostTaskForm(request.POST)
        if form.is_valid():
            name = form.data["name"]
            desc = form.data["description"]
            try:
                compl = form.data["completed"]
            except:
                compl = False
            dd = form.data["due_date"]
            pr = form.data["priority"]
            t = form.cleaned_data["tags"]
            putData = {"name": name,
                        "description": desc,
                        "completed": compl,
                        "due_date": dd,
                        "priority": pr,
                        "tag": t}
            requests.put("http://127.0.0.1:8000/todolists/{list_id}/tasks/{pk}/".format(list_id=list_id, pk=pk), putData,
                         headers={'Authorization': 'Token ' + token})

            response = requests.get("http://127.0.0.1:8000/todolists/{list_id}/tasks/{pk}/".format(list_id=list_id, pk=pk),
                                    headers={'Authorization': 'Token ' + token})
            responseJSON = response.json()
            id = responseJSON["id"]
            name = responseJSON["name"]
            desc = responseJSON["description"]
            compl = responseJSON["completed"]
            dd = responseJSON["due_date"]
            pr = responseJSON["priority"]
            t = responseJSON["tags"]

            form = PostTaskForm({"name": name, "description": desc, "completed": compl, "due_date": dd, "priority": pr})
            return render(request, 'template_detailtask.html', {"name": name, "desc": desc, "compl": compl, "dd": dd, "pr": pr, "tags": t, "form": form, "list_id": list_id})
    form = PostTaskForm(
        {"name": name, "description": desc, "completed": compl, "due_date": dd, "priority": pr})
    return render(request, 'template_detailtask.html',
                      {"name": name, "desc": desc, "compl": compl, "dd": dd, "pr": pr, "tags": t, "form": form, "list_id": list_id})


def deleteTasklist(pk):
    requests.delete("http://127.0.0.1:8000/todolists/{pk}/".format(pk=pk), headers={'Authorization': 'Token ' + token})


def Main(request):
    global token
    if token == "":
        v = ""
    else:
        v = "qwerty"
    return render(request, 'template_main.html', {"value": v})


def deleteTask(list_id, pk):
    requests.delete("http://127.0.0.1:8000/todolists/{list_id}/tasks/{pk}/".format(list_id=list_id, pk=pk),
                            headers={'Authorization': 'Token ' + token})


def getTags(request):
    response = requests.get("http://127.0.0.1:8000/tags/")
    tags_id_name = [(t["id"], t["name"]) for t in response.json()]
    path = "/todolists/"
    print(path)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            requests.post("http://127.0.0.1:8000/tags/", {"name": name})
            return HttpResponseRedirect("/tags/")

    form = TagForm()
    return render(request, 'template_tags.html', {"tags": tags_id_name, "path": path, "form": form})


def DetailTag(request, pk):
    global token

    if request.method == "POST":
        print(111111111)
        form = TagForm(request.POST)
        name = form.data["name"]
        requests.put("http://127.0.0.1:8000/tags/{pk}/".format(pk=pk), {"name": name}, headers={'Authorization': 'Token ' + token})

    response = requests.get("http://127.0.0.1:8000/tags/{pk}/".format(pk=pk),
                            headers={'Authorization': 'Token ' + token})
    name = response.json()["name"]
    form = TagForm({"name": name})
    return render(request, 'tamplate_detailtag.html', {"form": form, "name": name})
