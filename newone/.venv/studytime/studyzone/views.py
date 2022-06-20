from multiprocessing import context
from django.shortcuts import render,HttpResponse
from jmespath import search
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
import requests
import wikipedia
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'index.html') 
def about(request):
    return render(request,'about.html') 
def blog(request):
    return render(request,'blog.html') 

@login_required
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from{request.user.username} Successfully")
    else:
        form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    # notes= Notes.objects.filter().first()
    context={'notes':notes,'form':form}
    return render(request,'notes.html',context)  
@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")    
class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'notesview.html'
    
@login_required
def homework(request):
    if request.method =="POST":
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished =='on':
                    finished= True
                else:
                     finished= False
            except:
                finished=False
            homeworks= Homework(
            user =request.user,
            subject=request.POST['subject'],
            title=request.POST['title'],
            description=request.POST['description'],
            due=request.POST['due'],
            is_finished=finished,
            )
            homeworks.save()
            messages.success(request,f"Homework added form {request.user.username}!!")
    else:
          form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)== 0:
        homework_done=True
    else:
        homework_done=False
    context={
        'homeworks':homework,
        'homeworks_done':homework_done,
        'form':form,
        "True": True
        }
    return render(request,'homework.html',context)  
    
@login_required
def updatehomework(request,pk=None):
    homework= Homework.objects.get(id=pk)
    if homework.is_finished ==True:
        homework.is_finished= False
    else:
        homework.is_finished =True
    homework.save()
    return redirect('homework')

@login_required
def deletehomework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

@login_required
def todo(request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST["is_finished"]
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            todos=Todo(
                user= request.user,
                title= request.POST['title'],
                is_finished= finished
            )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username}!!")
    else:
        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,'todo.html',context) 

@login_required
def updatetodo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')
@login_required
def deletetodo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

def youtube(request):
     if request.method== "POST":
        form=DashboardFom(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={

                'form':form,
                'results':result_list
            }     
        return render(request,'youtube.html',context)
     else:    
         form=DashboardFom()    
     context={'form':form}
     return render(request,'youtube.html',context)

@login_required
def books(request):
     if request.method== "POST":
        form=DashboardFom(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer= r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                # 'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pagecount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }     
        return render(request,'books.html',context)
     else:    
         form=DashboardFom()
     context={'form':form}
     return render(request,'books.html',context) 

def dictionary(request):
    if request.method== "POST":
        form=DashboardFom(request.POST)
        text=request.POST['text']        
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer= r.json()
        try:
            phonetics= answer[0]['phonetics'][0]['text']
            audio= answer[0]['phonetics'][0]['audio']
            definition= answer[0]['meanings'][0]['definitions'][0]['definition']
            example= answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms= answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                'form':form,
                'input':'',
            }
        return render(request,"dictionary.html",context)
    else:
        form=DashboardFom()
        context={'form':form}
        return render(request,'dictionary.html',context) 

# def wikipedia(request):
#     import wikipedia
#     if request.method == "POST":
#         search = request.POST.get('search',False)
#         try:
#             result = wikipedia.summary(search,sentences = 3) #No of sentences that you want as output
#         except:
#             return HttpResponse("Wrong Input")
#         return render(request,"wikipedia.html",{"result":result})
#     return render(request,"wikipedia.html")

# wi = wikipedia.page("sachin tendulkar",sentences=2)
# print(wi)

def wikipedia(request):
    import wikipedia
    if request.method=='POST':
        text = request.POST['text']
        form= DashboardFom(request.POST)
        Search= wikipedia.page(text)
        # result = wikipedia.summary(search,sentences = 3)
        context={
            'form':form,
            'title':Search.title,
            'link': Search.url,
            'details':Search.summary
        }
        return render(request,"wikipedia.html",context)
    else:
        form=DashboardFom()
        context={'form':form}
    return render(request,'wikipedia.html',context) 

def conversion(request):
    if request.method=="POST":
        form=ConversionForm(request.POST)
        if request.POST['measurement']=='length':
            measurement_form=ConversionLengthForm()
            context={
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input= request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first =='yard' and second =='foot':
                        answer=f'{input}yard ={int(input)*3} foot'
                    if first =='foot' and second =='yard':
                        answer=f'{input}foot ={int(input)*3} yard'
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement']=='mass':
            measurement_form=ConversionMassForm()
            context={
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input= request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first =='pound' and second =='kilogram':
                        answer=f'{input}pound ={int(input)*0.453592} kilogram'
                    if first =='kilogram' and second =='pound':
                        answer=f'{input}kilogram ={int(input)*2.20462} pound'
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:    
        form=ConversionForm()
        context={
        'form':form,
        'input':False
        }
    return render(request,'conversion.html',context) 

def registration(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            # email=form.cleaned_data.get('email')
            messages.success(request,f"Account Created for {username}!!")
            return redirect('login')
    else:
        form=UserRegistrationForm()
    context={
        'form':form
    }
    return render(request,'registration.html',context)

@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todos)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done,
    }
    return render(request,'profile.html',context) 

@login_required
def newsletter(request):
    if request.method=="POST":
        # data=Registration()
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        Newsletter(name=name, email=email, phone=phone).save()
        return render(request,'index.html')
    else:
      return HttpResponse("error")  
    
# import wikipedia
 
# wikipedia page object is created
# page_object = wikipedia.page("Ms. Dhoni")
 
# printing html of page_object
# print(page_object)
 
# printing title
# print(page_object.original_title)
 
# printing links on that page object
# print(page_object.links[0:10])