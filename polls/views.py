from django.shortcuts import render,redirect
import polinomio as pn
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from .models import Question, User
from django.utils import timezone
import datetime
from hashlib import sha256
from .usuarios import logout, huser
from django.http import HttpResponse
matplotlib.use('agg')




def index(request):
    return render(request,'polls/index.html')

    
def telaInicial(request):
    logout = False
    permisson = False
    if huser(request) and request.method == 'POST' and not 'IR' in request.POST:
        logout = True
        if 'sair' in request.POST:
            user = User.objects.get(user = request.session['usuario'])
            user.login = False
            user.save()
            request.session.pop('usuario')
            return redirect('index')
        elif 'cancelar' in request.POST:
            logout = False
            return redirect('telaInicial')
    context = {'logout':logout,
               'permission':permisson}
    return render(request, 'polls/telainicial.html', context)

def register(request):
    if request.method == 'GET':
        return render(request, 'polls/user.html')
    else:
        usuario  = request.POST.get('usuario')
        senha = str(request.POST.get('senha'))
        if usuario == '' or senha == '':
            verificacao = True
            context = {'verificacao':verificacao}
            return render(request, 'polls/user.html', context)
        try:
            user1 = User.objects.get(user = usuario, password = sha256(senha.encode()).hexdigest())
        except:
            verificacao = True
            context = {'verificacao':verificacao}
            return render(request, 'polls/user.html', context)
        else: 
            request.session['usuario'] = usuario
            request.session.save()
            user1.login_date = timezone.now()
            user1.login = True
            user1.save()
            return redirect('index')

def polinomio2(request, verificacao = False, value = str()):
    mensagem = 'Use apenas coeficientes inteiros'
    if request.method == 'GET' or verificacao:
        logout(request)
        context = {'verificacao':verificacao,
                   'valor':value,
                   'mensagem':mensagem}
        return render(request, 'polls/raizes.html',context)
    else:
        verificacao = False
        polinomio3 = request.POST.get('polinomio2')
        if polinomio3=='' or 'x' not in polinomio3:
            s = 'Digite um valor válido'
            context = {'s':s}
            return render(request, 'polls/raizes.html', context)
        diretorio = 'static/imagens/Pol1.png'
        polinomio1 = pn.Polinomio(polinomio3)
        po = polinomio1.poly()
        r = np.roots(po)
        r2 = r.tolist()
        x = np.linspace(-10000, 10000)
        y = po(x)
        fig = plt.figure(clear=True)
        plt.plot(x,y)
        fig.savefig(diretorio)
        verificacaop = True
        if huser(request):
            session = request.session['usuario']
            u = User.objects.get(user = str(session))
            if u.login:
                q = Question(user12 = u, url = 'raizes')
                q.value = polinomio3
                q.save()
        context = {'r':r2,
                   'p':polinomio3,
                   'verificacaop':verificacaop,
                   'mensagem':mensagem}
        return render(request,'polls/raizes.html', context)

def equadio(request,verificacao = False, value = str()):
    if request.method == 'GET' or verificacao:
        logout(request)
        context = {'verificacao':verificacao,
                   'valor':value}
        return render(request, 'polls/equadio.html', context)
    else:
        equadiof = request.POST.get('equadio')
        error=True
        for i,v in enumerate(equadiof):
            if v.isdigit():
                error = False
                break
            
        if equadiof=='' or error:
            s = 'Digite um valor válido'
            context = {'s':s}
            return render(request, 'polls/equadio.html', context)
        eq = str()
        lista = []
        verificacao2 = True
        for i,v in enumerate(equadiof):
            if v == '=':
                a = i
                break
            eq = eq+v
        eq2 = equadiof[a+1:]
        p = pn.Polinomio(eq)
        p.poly()
        a = p.coeficientes[0]
        b = p.coeficientes[1]
        c = int(eq2)
        resul = pn.dioequa(int(a),int(b),int(c))
        if isinstance(resul,str):
            verificacao2=False
        for k in equadiof:
            if k.isalpha():
                lista.append(k)
        if huser(request):
            session = request.session['usuario']
            u = User.objects.get(user = str(session))
            if u.login:
                q = Question(user12 = u, url = 'equacaodio')
                q.value = equadiof
                q.save()
        context = {'verificacao2':verificacao2,
                'resul':resul,
                'equadiof':equadiof,
                'lista':lista}
        return render(request,'polls/equadio.html', context)    

def number(request,verificacao = False, value = str()):
    if request.method == 'GET' or verificacao:
        logout(request)
        context = {'verificacao':verificacao,
                   'valor':value}
        return render(request, 'polls/number.html', context)
    else:
        Nu = request.POST.get('numero')
        error = not Nu.isdigit()
        if Nu=='' or error:
            s = 'Digite um valor válido'
            context = {'s':s}
            return render(request, 'polls/number.html', context)
        numero = pn.Numero(int(Nu))
        fat = numero.fat()
        if len(numero.prime)>1:
            isprimebool = False
        else:
            isprimebool=True
        verificacao2 = True
        context = {'verificacao2':verificacao2,
                   'isprimebool':isprimebool,
                   'fat':fat,
                   'N':Nu}
        if huser(request):
            session = request.session['usuario']
            u = User.objects.get(user = str(session))
            if u.login:
                q = Question(user12 = u, url = 'number')
                q.value = Nu
                q.save()
        return render(request, 'polls/number.html', context)

listamais = [0]
listamenos = [0]
def teoch(request,verificacao = False, value = str()):
    m = 0
    n = 0
    if request.method == 'GET' or verificacao:
        logout(request)
        k9 = str()
        i = 0
        listamais.clear()
        listamenos.clear()
        if verificacao:
            l2 = []
            l3 = []
            while True:
                if value[i].isdigit():
                    k9 = k9+value[i]
                else:
                    if k9!='':
                        l2.append(int(k9))
                    k9 =str()
                
                i+=1
                if i>=len(value):
                    break
            listamais.append(int((len(l2)-1)/6))
            m = sum(listamais)
            for i in range(0,int(len(l2)/3)):
                l3.append(l2[3*i:3*(i+1)])
            context = {'m':range(0,m+1),
                        'verificacao':verificacao,
                        'l3':l3}
            return render(request,'polls/teoch.html',context)
        return render(request,'polls/teoch.html',{'m':range(0,m+1),
                                                  'verificacao':verificacao})
    
    if '+' in request.POST or '-' in request.POST and not 'Enviar' in request.POST:
       
        if '+' in request.POST:
            m+=1
            listamais.append(m)
        if '-' in request.POST :
            n += 1
            listamenos.append(n)
        if sum(listamais)-sum(listamenos)>=1:
            verificacao2 = True
        else:
            verificacao2 = False
        q = sum(listamenos)
        p = sum(listamais)
        j = p-q
        context = {'m':range(0,j+1),
                   'v':verificacao2}
        return render(request,'polls/teoch.html', context)
    else:
        l = []
        l3 = []
        for i in request.POST:
            if i.isdigit():
                for k in request.POST.getlist(f'{i}'):
                    error = not k.isdigit()
                    if k=='' or error:
                        s = 'Digite um valor válido'
                        context = {'s':s,
                                   'verificacao':verificacao,
                                   'm':range(0,1)}
                        return render(request, 'polls/teoch.html', context)
                    l.append(int(k))  
          
        k = pn.teoch(l)
        if isinstance(k,list):
            a = k[0]
            b = k[1]
            q = sum(listamenos)
            p = sum(listamais)
            j = p-q
            if huser(request):
                session = request.session['usuario']
                u = User.objects.get(user = str(session))
                if u.login:
                    k = str()
                    for i in l:
                        k = k+' '+str(i)+' '
                    q = Question(user12 = u, url = 'teoch')
                    q.value = k
                    q.save()  
            for h in range(0,int(len(l)/3)):
                l3.append(l[3*h:3*(h+1)])
            context = {'m':range(0,(j+1)),
                    'l':f'{b}k+{a}',
                    'lista':l3,
                    'verificacao':verificacao}
            return render(request,'polls/techResult.html', context)
        else:
            return render(request, 'polls/techResult.html', {'k':k,
                                                             'ver':True})


def historic(request):
    logout(request)
    if huser(request):
        usuario = request.session['usuario']
        u = User.objects.get(user = usuario)
        verificacao2 = False
        verificacao = True
        verificacao3 = False
        if u.login:
            lista_question = list(Question.objects.filter(user12 = u))
            lista = lista_question
            for i in lista_question:
                        if i.value=='':
                            lista.remove(i)
            if len(lista) == 0:
                verificacao2 = True
            pesquisa = request.POST.get('input')
            if pesquisa != None:
                try:
                    questao = Question.objects.get(value=pesquisa)
                except:
                    verificacao3 = True 
                else:
                    verificacao3_1 = True
                    for i,v in enumerate(lista):
                        if v.value == questao.value:
                            item = i
                    return render(request, 'polls/historic.html', {'verificacao3_1':verificacao3_1,
                                                                       'p':pesquisa,
                                                                       'item':item})
            if request.method == 'POST' and not 'enviar' in request.POST:
                lista_request = list(request.POST)
                if lista_request[1][1].isdigit():
                    p = int(lista_request[1][1:])
                    u = lista_question[p]   
                    u.delete()
                    u.save()
                    for i in lista_question:
                        if i.value=='':
                            lista.remove(i)
                else:
                    value2 = request.POST.getlist('question')
                    u2 = Question.objects.get(value = value2[0], user12 = str(request.session['usuario']))
                    match u2.url:
                        case 'raizes':
                            return polinomio2(request, verificacao, value2[0])
                        case 'equacaodio':
                            return equadio(request, verificacao, value2[0])
                        case 'number':
                            return number(request, verificacao, value2[0])
                        case 'teoch':
                            return teoch(request, verificacao, value2[0]) 
            return render(request, 'polls/historic.html',
                                {'lista_question':lista,
                                'verificacao2':verificacao2,
                                'verificacao3':verificacao3})
        else:
            return render(request, 'polls/historic.html',{'verificacao':True})
    else:
        return render(request, 'polls/historic.html',{'verificacao':True})

def cadastro(request):
    if request.method == 'GET':
        return render(request,'polls/cadastro.html')
    else:
        usuario = request.POST.get('usuario')
        senha = str(request.POST.get('senha'))
        user_exist = False
        if usuario == '' or senha == '':
            return render(request, 'polls/cadastro.html', {'vazio':True})
        try:
            user = User.objects.get(user=usuario)
        except:
            user = User(user = usuario, password = sha256(senha.encode()).hexdigest(), login_date = (timezone.now()-datetime.timedelta(minutes=60)))
            user.save()
            return redirect('register')
        else:
            user_exist = True
            return render(request, 'polls/cadastro.html',{'user_exist':user_exist})
def mudarsenha(request):
    if request.method == 'GET':
        return render(request, 'polls/mudarsenha.html')
    else:
        usuario = request.POST.get('usuario')
        try:
            u = User.objects.get(user = usuario)
        except:
            verificaco3=True
            return render(request,'polls/mudarsenha.html', {'verificacao3':verificaco3})
        else:
            senha2 = request.POST.get('password')
            senha=str(request.POST.get('password2'))
            if senha != senha2:
                return render(request, 'polls/mudarsenha.html',{'v':True})
            u.password=sha256(senha.encode()).hexdigest()
            u.save()
            return redirect('register')