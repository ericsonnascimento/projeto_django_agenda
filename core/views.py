from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import Evento
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username') #capturando user e password do formulário
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password) #comparando user e password com o cadastrado no db utilizando a função authenticate
        if usuario is not None:
            login(request, usuario) #utilizando a função login para criar uma sessão e liberar acesso se os campos não estiverem vazios
        else:
            messages.error(request, 'Usuario ou senha inválido')
    return redirect('/')

@login_required(login_url='/login') #limitando acesso, apenas usuários logados, se não estiver é direcionado para a url /login
def lista_eventos(request):
    usuario = request.user #pegando a sessão do usuário logado
    data_atual = datetime.now() - timedelta(hours=1) #no "- timedelta(hours=1)" faz com que os eventos que venceram até 1h atrás ainda apareçam

    '''filtrando apenas os eventos do usuário capturado, django não tem > ou <, temos __gt para > e __lt para <, então,
    vamos usar na coluna do DB __gt para pegar evento acima da data atual'''
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual) 
    return render(request, 'agenda.html', {'eventos':evento})

#aqui além de criarmos uma nova agenda vamos reaproveitar a criação de um novo evento em evento.html para também editar
@login_required(login_url='/login')
def evento(request): #cadastrar evento page form

    #---> aqui começa o código para edição do evento reaproveitando o evento.html
    id_evento = request.GET.get('id') #pegando o id na url editar em agenda.html 
    dados = {} #inserindo nesta variável um dicionário com todos os dados capturados do id selecionado
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)

    #---> aqui termina o código de reaproveitamento
    return render(request, 'evento.html', dados)

@login_required(login_url='/login')
def submit_evento(request): #botão submit do evento page form
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user

        #---> aqui começa o código para edição do evento reaproveitando o evento.html
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario: #validando se o usuário que está editando é o mesmo que está logado
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
        #---> aqui termina o código de reaproveitamento
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario) #criando objeto no db
    return redirect('/')

@login_required(login_url='/login')
def delete_evento(request, id_evento):
    usuario = request.user

    #bloco que trata exceção para o Error server (500), que exibirá agora "Not Found"
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario: #validando para que o usuario possa deletar apenas os seus eventos
        evento.delete()
    else:
        raise Http404()
    #fim do bloco

    return redirect('/')

@login_required(login_url='/login')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo') 
    return JsonResponse(list(evento), safe=False) #safe=False significa que estamos passando lista e não um dicionário, isso habilita que seja possível fazer dessa forma


def json_lista_evento_api(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo') 
    return JsonResponse(list(evento), safe=False) #safe=False significa que estamos passando lista e não um dicionário, isso habilita que seja possível fazer dessa forma

