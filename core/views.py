from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import Evento

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
    evento = Evento.objects.filter(usuario=usuario) #filtrando apenas os eventos do usuário capturado
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
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario: #validando para que o usuario possa deletar apenas os seus eventos
        evento.delete()
    return redirect('/')