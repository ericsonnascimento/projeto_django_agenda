from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo
    
    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M hrs')
    
    #criando uma função para data e hora que o navegador entende, isso é para o auto preenchimento da data e hora do editar em evento.html
    def get_data_input_evento(self): 
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')
    
    #função para mudar a cor do evento no agenda.html caso a data do evento seja inferior a data atual
    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False