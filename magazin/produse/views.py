from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse('<p>Index view</p>')



def entry_detail(request, produs_id):
    return HttpResponse('<p>entry_detail cu id ' + str(produs_id) + ' </p>')

def contact(request):
    return_string = '''<h3>Contact</h3>
    <p>Contact: Numele Tau</p>
    <p>Email:office@site.com</p>
    <p>Tel:070.111.111</p>'''
    return HttpResponse(return_string)

###################################################3

from django.http import Http404
from produse.models import Produse


def index(request):
    produse = Produse.objects.all()
    return render(request, 'index.html', {'produse': produse})


def entry_detail(request,produs_id):
    try:
        produs=Produse.objects.get(id=produs_id)
    except:
        raise Http404("Produsul nu mai exista in momentul de fata spre vanzare.")
    else:
        return render(request,'entry_detail.html',{'produs':produs})

def contact(request):
    return render(request, 'contact.html', {})


# formular de contact

from produse.forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail

def contact(request):
  if request.method == 'POST':
     form = ContactForm(request.POST)
     if form.is_valid():
         mesaj="Mesaj de la:"+form.cleaned_data['contact_name']+",email:"+\
                 form.cleaned_data['contact_email']+"\n\n"+\
                 form.cleaned_data['content']
         send_mail('Contact prin django', mesaj,  settings.EMAIL_HOST_USER,
                 ['popescu.catalin.ionut@gmail.com'], fail_silently=False)
     return render(request, 'contact_sent.html', {})
  else:
     return render(request, 'contact.html', {'form': ContactForm})

############### formular de contact ##########
# Create your views here.
from django.views import View


class Contact(View):
  def get(self, request):
    return render(request, 'contact.html', {'form': ContactForm})

  def post(self, request):
     form = ContactForm(request.POST)
     if form.is_valid():
       mesaj = "Mesaj de la:" + form.cleaned_data['contact_name'] + ",email:" + \
               form.cleaned_data['contact_email'] + "\n\n" + \
               form.cleaned_data['content']
       send_mail('Contact prin django', mesaj, settings.EMAIL_HOST_USER,
                 ['popescu.catalin.ionut@gmail.com'], fail_silently=False)
     return render(request, 'contact_sent.html', {})


def index(request):
  produse = Produse.objects.all()
  return render(request, 'index.html', {'produse': produse, 'username':request.user.username})


def entry_detail(request,produs_id):
    try:
        produs=Produse.objects.get(id=produs_id)
    except:
        raise Http404("Produsul nu mai exista in momentul de fata spre vanzare.")
    else:
        return render(request, 'entry_detail.html', {'produs': produs, 'username': request.user.username})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mesaj="Mesaj de la:"+form.cleaned_data['contact_name']+",email:"+\
                 form.cleaned_data['contact_email']+"\n\n"+\
                 form.cleaned_data['content']
            send_mail('Contact prin django', mesaj,  settings.EMAIL_HOST_USER,
                 ['popescu.catalin.ionut@gmail.com'], fail_silently=False)
            return render(request, 'contact_sent.html', {'username':request.user.username})
    else:
        return render(request, 'contact.html', {'form': ContactForm, 'username':request.user.username})


# profil

from produse.forms import UserForm
from produse.models import Useri
from django.contrib.auth.models import User
from django.shortcuts import redirect

def profil(request):
    user_is_valid = True
    try:
        user_oficial = User.objects.get(username=request.user.username)
        user = Useri.objects.get(user=user_oficial.id)
    except:
        user_is_valid = False
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if not user_is_valid :
            return redirect('login')
        elif form.is_valid():
            form.save()
            return redirect('index')
    else:
        if not user_is_valid:
            return redirect('login')
    form = UserForm(instance=user)
    return render(request, 'profil.html', {'form': form, 'username':request.user.username})


# cos cumparaturi
from produse.models import Comanda
from django.contrib.auth.decorators import login_required
from produse import views

@login_required
def comanda(request):
  cart = _extragere_cos(request)
  user_oficial = User.objects.get(id=request.user.id)
  for produs,numar in cart.items():
    produs_q = Produse.objects.get(id=produs)
    Comanda.objects.create(
      pret_achizitie=produs_q.pret,
      produs = produs_q,
      user = Useri.objects.get(user=user_oficial.id),
      finalizat = False)
  request.session['cart'] = {}
  return render(request, 'cart_comandat.html', {'produse': [], 'cos': len(_extragere_cos(request)),
                                                'username': request.user.username,
                                            'titlu': 'cos'})

def _extragere_cos(request):
  if not request.session.has_key('cart'):
    return {}
  else:
    return request.session['cart']


@login_required(login_url="login")
def cos(request):
  cart = _extragere_cos(request)
  produse = []
  for produs,numar in cart.items():
    produs_q = Produse.objects.get(id=produs)
    produs_q.numar = numar
    produse.append(produs_q)
  return render(request, 'cart.html', {'produse': produse,
                                       'cos': len(cart),
                                       'username': request.user.username,
                                            'titlu': 'cos'})


@login_required(login_url="login")
def istoric(request):
  produse = []
  cart = _extragere_cos(request)
  produse_query = Comanda.objects.filter(user_id=Useri.objects.get(user=request.user.id).id).reverse()
  for produs in produse_query:
    produs_q = Produse.objects.get(id=produs.produs_id)
    produs_q.pret_achizitie=produs.pret_achizitie
    produs_q.numar = produs.numar
    produs_q.data = produs.data
    produs_q.finalizat = produs.finalizat
    produse.append(produs_q)
  return render(request, 'istoric.html', {'produse': produse, 'cos': len(cart),
                                          'username': request.user.username, 'titlu': 'cos'})


def adauga_in_cos(request, produs_id):
  produs_id = str(produs_id)
  if not request.session.has_key('cart'):
    request.session['cart']={produs_id: 1}
  else:
    all_cart = request.session['cart']
    if all_cart.get(produs_id):
      all_cart[produs_id]+=1
    else:
      all_cart[produs_id] = 1

    request.session['cart']=all_cart
  request.session.modified = True
  return getattr(views,'entry_detail')(request,produs_id)


def index(request):
  produse=Produse.objects.all()
  cos = _extragere_cos(request)
  return render(request,'index.html',{'produse':produse, 'cos':len(cos),
                                      'username':request.user.username})

def entry_detail(request,produs_id):
  try:
    produs=Produse.objects.get(id=produs_id)
  except:
    raise Http404("Produsul nu mai exista in momentul de fata spre vanzare.")
  else:
    cart = _extragere_cos(request)
    return render(request,'entry_detail.html',{'produs':produs,'cos':sum(cart.values()),
                                               'username':request.user.username})


def contact(request):
  if request.method == 'POST':
     form = ContactForm(request.POST)
     if form.is_valid():
         mesaj="Mesaj de la:"+form.cleaned_data['contact_name']+",email:"+\
                 form.cleaned_data['contact_email']+"\n\n"+\
                 form.cleaned_data['content']
         send_mail('Contact prin django', mesaj,  settings.EMAIL_HOST_USER,
                 ['popescu.catalin.ionut@gmail.com'], fail_silently=False)
         return render(request, 'contact_sent.html', {'username':request.user.username,
                                                      'cos': len(_extragere_cos(request))})
  else:
     return render(request, 'contact.html', {'form': ContactForm,
                                             'cos': len(_extragere_cos(request)),
                                             'username':request.user.username})

def profil(request):
  user_is_valid = True
  try:
    user_oficial = User.objects.get(username=request.user.username)
    user = Useri.objects.get(user=user_oficial.id)
  except:
    user_is_valid = False
  if request.method == 'POST':
      form = UserForm(request.POST, instance=user)
      if not user_is_valid :
        return redirect('login')
      elif form.is_valid():
        form.save()
        return redirect('index')
  else:
    if not user_is_valid:
      return redirect('login')
    form = UserForm(instance=user)
  return render(request, 'profil.html', {'form': form, 'username':request.user.username,
                                         'cos': len(_extragere_cos(request))})