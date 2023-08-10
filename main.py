from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


import requests
from datetime import datetime
import _json
import pytz
import pycountry_convert as pc


######## cores ##########

cor0 = "#444466"  # preta
cor1 = "#feffff"  # branca
cor2 = "#6f9fbd"  # azul

fundo_dia = "#6cc4cc"
fundo_tarde = "#bfb86d"
fundo_noite = "#484f60"
fundo = fundo_dia


janela = Tk()
janela.title('')
janela.geometry('320x350')
janela.configure(bg=fundo)
ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)


# criando frames
frame_top = Frame(janela, width=320, height=50, bg=cor1, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=320, height=300, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=NW)

estilo = ttk.Style(janela)
estilo.theme_use('clam')


global imagem
# ----Criação da função que retorna as informações----
def informacao():
    # Conectando a chave API com o link
    chave = 'e350c65f151924f4d637e5a6fd281c59'
    cidade = input_local.get()
    api_link = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave}&lang=pt_br&units=metric' 
    
    # Fazendo a chamada da API usando request
    r = requests.get(api_link)

    # Convertendo os dados da variável r em dicionário
    dados = r.json()


    # ----Obtendo Zona----
    pais_codigo = dados['sys']['country']
    zona_fuso = pytz.country_timezones[pais_codigo]
    #print(zona_fuso)


    # ----Obtendo país----
    pais = pytz.country_names[pais_codigo]


    # ----Obtendo a data----
    zona = pytz.timezone(zona_fuso[0])


    # ----Obtendo a Hora local da cidade----
    zona_horas = datetime.now(zona)
    zona_horas = zona_horas.strftime("%d %m %y | %H:%M:%S %p")


    # ----tempo----

    tempo = dados['main']['temp'] 
    pressao = dados['main']['pressure']
    humidade = dados['main']['humidity']
    velocidade = dados['wind']['speed']
    descricao = dados['weather'][0]['description']
    

    # ----Mudando informações----


    def pais_para_continente(i):
        pais_alfa = pc.country_name_to_country_alpha2(i)
        pais_continente_cod = pc.country_alpha2_to_continent_code(pais_alfa)
        pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continente_cod)

        return pais_continente_nome

    continente = pais_para_continente(pais)
    # ----Fim função informação----

    # ----Passando informações da labels----
    l_cidade['text'] = cidade + " - " + pais + " / " + continente
    l_data['text'] = zona_horas
    l_temperatura['text'] = f"{tempo:.1f}"
    l_t_simbolo['text'] = "C°"
    l_velocidade_vento['text'] = f"Velocidade de vento: {velocidade}"
    l_pressao['text'] = f"pressao atmosférica: {pressao}"
    l_descricao['text'] = descricao


    # ----Lógica de troca de fundo----
    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime("%H")

    global imagem

    zona_periodo = int(zona_periodo)

    if zona_periodo <= 5:
        # Adicionando imagens
        imagem = Image.open('consulta-clima\images\lua_noite.png')
        fundo = fundo_noite
    elif zona_periodo <= 11:
        imagem = Image.open('consulta-clima\images\sol_dia.png')
        fundo = fundo_dia
    elif zona_periodo <= 17:
        imagem = Image.open('consulta-clima\images\dia.png')
        fundo = fundo_tarde
    elif zona_periodo <= 23:
        imagem = Image.open('consulta-clima\images\lua_noite.png')
        fundo = fundo_noite
    else:
        pass

    imagem = imagem.resize((130, 130))
    imagem = ImageTk.PhotoImage(imagem)

    l_icon = Label(frame_corpo, image=imagem, bg=fundo,)
    l_icon.place(x=180, y=50)

    # ----Colorindo o fundo----
    janela.configure(bg=fundo)
    frame_top.configure(bg=fundo)
    frame_corpo.configure(bg=fundo)


    l_cidade['bg'] = fundo
    l_data['bg'] = fundo
    l_temperatura['bg'] = fundo
    l_t_simbolo['bg'] = fundo
    l_velocidade_vento['bg'] = fundo 
    l_pressao['bg'] = fundo
    l_descricao['bg'] = fundo



# configurando o frame_top

input_local = Entry(frame_top, width=20, justify='left', font=("", 14), highlightthickness=1, relief='solid')
input_local.place(x=15, y=10)
botao_ver = Button(frame_top, command=informacao, text='Ver clima', bg=cor1, fg=cor2, font=("Ivy 9 bold"), relief='raised', overrelief=RIDGE)
botao_ver.place(x=250, y=10)


# configurando o frame_corpo

l_cidade = Label(frame_corpo, text='Bem vindo ao Consulta Clima', anchor='center',  bg=fundo, fg=cor1, font=("Arial 14"))
l_cidade.place(x=4, y=4)

l_data = Label(frame_corpo, text='Digite o nome da cidade na barra superior', anchor='center',  bg=fundo, fg=cor1, font=("Arial 10"))
l_data.place(x=10, y=54)

l_temperatura = Label(frame_corpo, text='', anchor='center',  bg=fundo, fg=cor1, font=("Arial 45"))
l_temperatura.place(x=10, y=100)

l_t_simbolo = Label(frame_corpo, text='', anchor='center',  bg=fundo, fg=cor1, font=("Arial 10 bold"))
l_t_simbolo.place(x=150, y=85)

l_pressao = Label(frame_corpo, text='', anchor='center',  bg=fundo, fg=cor1, font=("Arial 10"))
l_pressao.place(x=10, y=184)

l_velocidade_vento = Label(frame_corpo, text='Programa criado por Marcelo Augusto', anchor='center',  bg=fundo, fg=cor1, font=("Arial 10"))
l_velocidade_vento.place(x=10, y=212)


# Descrição do clima
l_descricao = Label(frame_corpo, text='', anchor='center',  bg=fundo, fg=cor1, font=("Arial 10"))
l_descricao.place(x=200, y=190)






janela.mainloop()