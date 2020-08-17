from tkinter import messagebox
from fpdf import FPDF
from tkinter import *
import os.path as path
import pickle
import random
import time
import os

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# grabar listas de partidas en un archivo
archivo = open("futoshiki2020partidas.dat","wb")

# 3 partidas por nivel
lista_partidas_facil = [ ((">", 0, 0), (">", 0, 2), (">", 0, 3), ("4", 1, 0), ("2", 1, 4), ("4", 2, 2), ("<", 3, 3), ("4", 3, 4), ("<", 4, 0), ("<", 4, 1)),
                         (("<", 0, 0), ("∧", 0, 3), ("1", 0, 4), ("<", 1, 0), ("4", 1, 4), ("∧", 2, 4), ("<", 3, 0), ("2", 3, 2), (">", 3, 3)),
                         (("∧", 0, 1), ("∧", 0, 2), ("∧", 0, 3), (">", 2, 0), ("v", 2, 1), ("v", 2, 3), ("<", 3, 0), ("v", 3, 1), ("4", 4, 0)),
                         (("v", 1, 0), ("v", 1, 2), (">", 2, 2), ("v", 3, 0), ("3", 3, 3), ("v", 3, 3), ("<", 4, 1), (">", 4, 3))]

lista_partidas_intermedio = [ ((">", 0, 2), ("v", 0, 3), ("<", 0, 3), ("∧", 1, 0), ("∧", 1, 1), ("v", 1, 4), ("<", 2, 1), ("∧", 2, 4), ("v", 3, 3), ("∧", 3, 4), ("<", 4, 2)),
                              (("2", 0, 0), ("2", 1, 1), (">", 1, 2), ("∧", 1, 4), ("∧", 2, 4), ("v", 3, 0), ("<", 3, 1), (">", 4, 0), ("2", 4, 4)),
                              (("3", 0, 0), (">", 0, 0), ("v", 0, 0), ("∧", 1, 2), (">", 2, 3), ("2", 2, 4), ("<", 3, 0), ("<", 3, 1), ("∧", 3, 3), ("∧", 3, 4))]

lista_partidas_dificil = [ (("v", 0, 0), ("v", 0, 3), ("∧", 1, 1), ("v", 2, 3), ("<", 2, 3), ("<", 3, 2), ("∧", 3, 3), ("∧", 3, 4), ("<", 4, 0)),
                           (("v", 0, 0), ("<", 0, 0), ("∧", 0, 1), ("∧", 0, 3), ("5", 2, 0), ("∧", 2, 1), (">", 2, 2), ("∧", 2, 4), ("∧", 3, 1), ("<", 3, 1), (">", 3, 3), (">", 4, 3)),
                           (("4", 0, 0), (">", 0, 0), ("<", 0, 3), ("∧", 1, 0), ("∧", 1, 1), ("∧", 1, 3), ("∧", 2, 0), ("<", 2, 1), ("<", 3, 2), (">", 4, 3))]

pickle.dump(lista_partidas_facil, archivo)
pickle.dump(lista_partidas_intermedio ,archivo)
pickle.dump(lista_partidas_dificil, archivo)

archivo.close()

# lee las partidas guardadas 
archivo = open("futoshiki2020partidas.dat","rb")

lista_facil = pickle.load(archivo)
lista_inter = pickle.load(archivo)
lista_dif = pickle.load(archivo)
archivo.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# variables para el reloj
s = 0 
m = 0
h = 0

# variable para guardar el tiempo obtenido
proceso = ""

# banderas
indicador = False
indicador2 = False
indicador3 = False
indicador4 = False
indicador5 = False
paused = False
click = False
expirado = False
guardado = False
multinivel = False
global nivel

# cantidad de partidas en cada lista de nivel
max_facil = len(lista_facil)-1
max_inter = len(lista_inter)-1
max_dificil = len(lista_dif)-1

# ventanas globales
ventana_jugar = None
ventana_config = None
ventana_top = None

# variables para configuracion e inicio de juego
global nombre
global modo
global reloj
global pos

# variables para datos del timer
global segundos
global minutos
global horas
global s2,m2,h2
global timer_string
global proceso_string

# variables para obtener el valor de los radiobutton(configuracion)
global var1,var2,var3,n

# variables botones para cambiar su estado
global b_iniciar
global b_borrar1
global b_terminar
global b_borrar2
global b_guardar
global b_cargar
global b_devolverse
global b_rehacer
global b_solucion
global b_posibles_jugadas

# variable para obtener la partida
global partida
global listaBotones,listaDigitos,lista_partida
global digito,index
global lista_movimientos
global jugadas_borradas

# Colores y fonts

button_main_font = "Helvetica"
main_titulo_font = ("Courier", 50)
main_color = "gold"
color2 = "steelblue"
color3 = "black"
color4 = "goldenrod"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

principal = Tk()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def jugar():
    global n
    global indicador,expirado
    global ventana_jugar
    global b_borrar1,b_terminar,b_borrar2,b_guardar,b_cargar,b_iniciar,b_devolverse,b_rehacer,b_solucion,b_posibles_jugadas
    global s,m,h
    global s2,m2,h2,nivel

    expirado = False
    if not indicador:
        messagebox.showinfo("Mensaje",message="Primero debe configurar el juego")
    
    else:
        if guardado:
            if reloj == 1 or reloj == 2:
                s = 0
                m = 0
                h = 0
            if reloj == 3:
                segundos = s2
                minutos = m2
                horas = h2
        
        principal.withdraw()
        ventana_jugar = Tk()
        ventana_jugar.title("Jugar")
        ventana_jugar.geometry('850x850+500+80')
        ventana_jugar.resizable(width = False,height = False)
        ventana_jugar.config(background = main_color)

        label = Label(ventana_jugar, text = "FUTOSHIKI",fg = color2,bg = main_color,font=('System', 28)).pack(pady=10)
        label2 = Label(ventana_jugar,text="Nombre del jugador:",fg = color3,bg = main_color,
                            font =('System',10)).place(x=250,y=120)

        n = Entry(ventana_jugar)
        n.place(x=420,y=123,width = '200')

        
        b_iniciar = Button(ventana_jugar,text="Iniciar juego",width = 12, bg = color2,command = lambda:iniciar(n.get()))
        b_iniciar.place(x=300,y=660)

        label_pj = Label(ventana_jugar,text="Posibles jugadas:",font=(None,12),bg=main_color)
        label_pj.place(x=50,y=680)
        b_posibles_jugadas = Button(ventana_jugar,text="Posibles jugadas", width = 12, bg = color2,state="disable")
        b_posibles_jugadas.place(x=300,y=730)
        
        b_borrar1 = Button(ventana_jugar,text="Borrar jugada", width = 12, command = borrar_jugada,bg = color2,state="disable")
        b_terminar = Button(ventana_jugar,text="Terminar juego", width = 12, command = terminar_juego, bg = color2,state="disable")
        b_borrar2 = Button(ventana_jugar,text="Borrar juego", width = 12,command = borrar_juego,bg = color2,state="disable") 
        b_top = Button(ventana_jugar,text="TOP 10", width = 12, command = top10_ventana, bg = color2)
        b_devolverse = Button(ventana_jugar,text="Volver a menú principal", width = 18, command = volver2, bg = color2)
        b_rehacer = Button(ventana_jugar,text="Rehacer jugada", width = 12, command = rehacer_jugada, bg = color2,state="disable")
        b_solucion = Button(ventana_jugar,text="Solucionar juego", width = 14, command = solucion_juego, bg = color2,state="disable")
        
        b_borrar1.place(x=420,y=730)
        b_terminar.place(x=570,y=660)
        b_borrar2.place(x=435,y=660)
        b_devolverse.place(x=660,y=800)
        b_rehacer.place(x=555,y=730)
        b_top.place(x=705,y=660)
        b_solucion.place(x=690,y=730)

        b_guardar = Button(ventana_jugar,text="Guardar juego",width = 12, command = guardar, bg = color2,state="disable")
        b_cargar = Button(ventana_jugar,text="Cargar juego",width = 12, bg = color2, command = cargar, state="normal")

        b_guardar.place(x=390,y=800)
        b_cargar.place(x=525,y=800)

        if modo == 1:
            nivel = Label(ventana_jugar,text="Nivel: Fácil",bg = main_color, font = ("Helvetica",14))
            nivel.pack()
            
        if modo == 2:
            nivel = Label(ventana_jugar,text="Nivel: Intermedio",bg = main_color, font = ("Helvetica",14))
            nivel.pack()
            
        if modo == 3:
            nivel = Label(ventana_jugar,text="Nivel: Difícil",bg = main_color, font = ("Helvetica",14))
            nivel.pack()

        if modo == 4:
            nivel = Label(ventana_jugar,text="Nivel: Multinivel",bg = main_color, font = ("Helvetica",14))
            nivel.pack()
        
        ventana_jugar.mainloop()


def iniciar(var_n):
    global nombre
    global b_iniciar,b_borrar1,b_terminar,b_borrar2,b_guardar,b_cargar,b_devolverse,b_posibles_jugadas
    global partida
    global indicador2,guardado
    global modo,multinivel
    
    guardado = False
    indicador2 = True

    frame = Frame(ventana_jugar,bg=color4)
    label_fila = Label(frame,text="Fila casilla",bg=color4,font=(None,11))
    label_fila.grid(row=0,column=0)
    entry_pj1 = Entry(frame,width = 6)
    entry_pj1.grid(row=0,column=1)
    label_col = Label(frame,text="Columna casilla",bg=color4,font=(None,11))
    label_col.grid(row=1,column=0)
    entry_pj2 = Entry(frame,width = 6)
    entry_pj2.grid(row=1,column=1)

    frame.place(x=45,y=740)
    
    nombre = var_n
    if nombre == "":
        messagebox.showerror("Error",message = "Ingrese el nombre del jugador antes de iniciar")
    elif len(nombre)>20:
        messagebox.showerror("Error",message = "Nombre debe tener entre 1-20 caracteres")
    else:
        
        label_nombre = Label(ventana_jugar,text=nombre) # esconde el entry
        label_nombre.place(x=420,y=123,width = '200')
        label_nuevo = Label(ventana_jugar,text="",font=(None,12),bg = main_color,fg='blue')

        # cambia el estado de los botones al iniciar juego
        b_iniciar['state'] = 'disable'
        b_borrar1['state'] = 'normal'
        b_terminar['state'] = 'normal'
        b_borrar2['state'] = 'normal'
        b_guardar['state'] = 'normal'
        b_cargar['state'] = 'disable'
        b_devolverse['state'] = 'disable'
        b_rehacer['state'] = 'normal'
        b_solucion['state'] = 'normal'
        b_posibles_jugadas['state'] = 'normal'
        b_posibles_jugadas['command'] = lambda:posibles_jugadas(entry_pj1,entry_pj2,entry_pj1.get(),entry_pj2.get(),label_nuevo)

        if modo == 4:
            modo = 1
            multinivel = True
            
        if modo == 1:
            if lista_facil == []:
                messagebox.showerror("Error",message="No hay partidas para este nivel")
                volver2()
            else: # indicador3, 4 y 5 se enciende cuando se termina juego ya que indica que fue elegida otra dif al terminar la anterior
                if not indicador3:
                    partida = elegir_partida()
                relojes()
                crear_partida()

        if modo == 2:
            if lista_inter == []:
                messagebox.showerror("Error",message="No hay partidas para este nivel")
                volver2()
            else:
                if not indicador4:
                    partida = elegir_partida()
                relojes()
                crear_partida()
                
        if modo == 3:
            if lista_dif == []:
                messagebox.showerror("Error",message="No hay partidas para este nivel")
                volver2()
            else:
                if not indicador5:
                    partida = elegir_partida()
                relojes()
                crear_partida()

            
def relojes():
    global segundos,minutos,horas
    global s,m,h
    global s2,m2,h2,timer_string,proceso_string
    global paused
    global clock_label,timer_label
    
    if reloj == 1: 
        paused = False
        frame = Frame(ventana_jugar)
        label = Label(frame,text = "Reloj:",bg = main_color,fg='red', width=20, font=("","11"))
        label.grid(row=0)
        clock_label = Label(frame,bg = main_color,width=20, font=("","12"))
        clock_label.grid(row=1)
        frame.place(x=-40,y=12)
        frame.config(bg=main_color)

        if expirado:
            s = s2
            m = m2
            h = h2
            clock()
        else:
            clock()

        if multinivel:
            pr_s = int(proceso[-2:])
            pr_m = int(proceso[-5:-3])
            pr_h = int(proceso[:-6])

            if pr_s<10:
                pr_s = '0'+str(pr_s)
            if pr_m<10:
                pr_m = '0'+str(pr_m)
            if pr_h<10:
                pr_h = '0'+str(pr_h)
            proceso_string = str(pr_h)+":"+str(pr_m)+":"+str(pr_s)
        
    if reloj == 2: 
        paused = False
        clock2()
        
    if reloj == 3:
        paused = False
        
        segundos = int(segundos)
        minutos = int(minutos)
        horas = int(horas)

        ss = segundos
        mm = minutos
        hh = horas
        if ss<10:
            ss = '0'+str(ss)
        if mm<10:
            mm = '0'+str(mm)
        if hh<10:
            hh = '0'+str(hh)
        timer_string = str(hh)+":"+str(mm)+":"+str(ss)
        
        #copia de datos del timer
        s2 = segundos
        m2 = minutos
        h2 = horas

        frame = Frame(ventana_jugar)
        label = Label(frame,text = "Timer:",bg = main_color,fg='red', width=20, font=("","11"))
        label.grid(row=0)
        timer_label = Label(frame,bg = main_color,width=20, font=("","12"))
        timer_label.grid(row=1)
        frame.place(x=-40,y=12)
        frame.config(bg=main_color)
        timer()


def clock():
    # funciona cuando reloj es 1
    global s,m,h
    global proceso
    global clock_label

    if paused:
        return proceso
    else:
        
        s = s+1
        se = str(s)
        if s>=60:
            s = 0
            m = m+1
            mi = str(m)
            if m>=60:
                m = 0
                h = h+1
                hh = str(h)
        if s<10:
            se = '0'+str(s)
        else:
            se = str(s)
        if m<10:
            mi = '0'+str(m)
        else:
            mi = str(m)
        if h<10:
            hh = '0'+str(h)
        else:
            hh = str(h)

        proceso = (hh+':'+mi+':'+se)
        clock_label['text'] = proceso
        ventana_jugar.after(1000,clock)


def clock2():
    # funciona cuando reloj es 2
    global s,m,h
    global proceso

    if paused:
        return proceso
    else:
        s = s+1
        se = str(s)
        if s>=60:
            s = 0
            m = m+1
            mi = str(m)
            if m>=60:
                m = 0
                h = h+1
                hh = str(h)
        if s<10:
            se = '0'+str(s)
        else:
            se = str(s)
        if m<10:
            mi = '0'+str(m)
        else:
            mi = str(m)
        if h<10:
            hh = '0'+str(h)
        else:
            hh = str(h)

        proceso = (hh+':'+mi+':'+se)
        ventana_jugar.after(1000,clock2)


def timer():
    # funciona cuando reloj es 3
    global segundos,minutos,horas
    global timer_label
    global proceso,expirado,reloj
    global listaBotones,lista_movimientos,lista_partida

    if paused:
        return proceso
    else:
        if segundos>0 or minutos>0 or horas>0:
            se = str(segundos)
            segundos = segundos-1
            mi = str(minutos)
            hh = str(horas)
            if segundos<0 and minutos>=0:
                segundos = 59
                if minutos>0:
                    minutos = minutos-1
                    if minutos<0:
                        minutos = 59
                else:
                    minutos = 59
                    if horas>0:
                        horas = horas-1
                        
            if segundos<10:
                se = '0'+str(segundos)
            if segundos>=10:
                se = str(segundos)
            if minutos<10:
                mi = '0'+str(minutos)
            if minutos>=10:
                mi = str(minutos)
            if horas<10:
                hh = '0'+str(horas)
            if horas>=10:
                hh = str(horas)

            proceso = (hh+':'+mi+':'+se)
            timer_label['text'] = proceso
            ventana_jugar.after(1000,timer)

        else:
            respuesta = messagebox.askquestion(title="Tiempo expirado",message="¿Desea continuar el mismo juego?")
            segundos = s2
            minutos = m2
            horas = h2
            if respuesta == "yes":
                expirado = True
                reloj = 1
                relojes()
            else:
                ventana_jugar.withdraw()
                jugar()


def elegir_partida(): # solo escoge una partida aleatoria
    global lista_facil,lista_inter,lista_dif
    global max_facil,max_inter,max_dificil

    if modo == 1:

        if max_facil==0:
            partida = lista_facil[0]
        else: 
            num_random1 = random.randint(0,max_facil)
            #print("random",num_random1)
            partida = lista_facil[num_random1]
            #print(lista_facil)
            
    if modo == 2:
        if max_inter==0:
            partida = lista_inter[0]
        else: 
            num_random1 = random.randint(0,max_inter)
            partida = lista_inter[num_random1]
            
    if modo == 3:
        if max_dificil==0:
            partida = lista_dif[0]
        else: 
            num_random1 = random.randint(0,max_dificil)
            partida = lista_dif[num_random1]

    return partida
        
 
def crear_partida():
    global listaBotones
    global listaDigitos
    global lista_partida
    global lista_movimientos
    global jugadas_borradas

    frame = Frame(ventana_jugar)

    # crea los 25 botones
    b1 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b2 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b3 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b4 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b5 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b6 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b7 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b8 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b9 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b10 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b11 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b12 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b13 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b14 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b15 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b16 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b17 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b18 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b19 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b20 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b21 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b22 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b23 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b24 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b25 = Button(ventana_jugar,bg="white",width = 5, height = 2)


    # matriz de botones 5x5
    listaBotones = [[b1, b2, b3, b4, b5],
                    [b6, b7, b8, b9, b10],
                    [b11, b12, b13, b14, b15],
                    [b16, b17, b18, b19, b20],
                    [b21, b22, b23, b24, b25]]

    # matriz de la partida

    lista_partida = [[0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0]]

    copia = [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]]

    lista_movimientos = []
    jugadas_borradas = []
    lista_operador_pos = []
    listaDigitos = []
    
    label = Label(frame,text="Dígitos")
    label.config(font=("Helvetica", 10),bg=color4)
    label.grid(row = 0, padx=7)


    # crea botones de digitos y los coloca en el frame
    fila = 1
    for i in range(1,6):
        boton1 = Button(frame,text=str(i),bg = 'white',command = lambda a=i,b=i-1 : click_digito(a,b), width = 5, height = 2)
        boton1.grid(row=fila,column=0,pady=7,padx=7)
        listaDigitos += [boton1]
        fila += 1

            
    # coloca la posicion del frame digitos segun configuracion
    if pos==1: # derecha
        frame.config(bg=color4,borderwidth=2,relief="solid")
        frame.place(x=700,y=230)
        
    if pos==2: # izquierda
        frame.config(bg=color4,borderwidth=2,relief="solid")
        frame.place(x=100,y=230)


    # crea lista de comparadores y coloca los comparadores segun la partida
    lista_comparadores = []
    
    for casilla in partida:
        if not casilla[0].isdigit():
            lista_comparadores.append((casilla[0],casilla[1],casilla[2]))


    f2 = 305
    c2 = 208
    for i in range(5):
        for j in range(5):
            for comparador in lista_comparadores: 
                if (comparador[1],comparador[2]) == (i,j):
                    
                    if comparador[0] == ">": 
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14),bg= main_color)
                        signo.place(x=f2,y=c2)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1],comparador[2]+1)))
                        
                    if comparador[0] == "<":
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14),bg= main_color)
                        signo.place(x=f2,y=c2)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1],comparador[2]+1)))
                        
                    if comparador[0] == "∧":
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14,"bold"),width=3,bg= main_color)
                        signo.place(x=f2-54,y=c2+43)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1]+1,comparador[2])))
                        
                    if comparador[0] == "v":
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14),width=3,bg= main_color)
                        signo.place(x=f2-54,y=c2+43)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1]+1,comparador[2])))
            f2 += 85
        c2 += 85
        f2 = 305

    # agrega los numeros fijos a la lista de partida y a la copia de la misma
    for i in range(5):
        for j in range(5):
            for casilla in partida:
                if (i,j) == (casilla[1],casilla[2]) and casilla[0].isdigit():
                    lista_partida[i][j] = int(casilla[0])
                    copia[i][j] = int(casilla[0])
            
    # coloca los botones con su numero fijo segun la partida
    f = 248
    c = 198
    for i in range(5):
        for j in range(5):
            listaBotones[i][j]['command'] = lambda a=i,b=j : click_cuadricula(a,b,lista_operador_pos,copia)
            listaBotones[i][j].place(x=f,y=c)
            for casilla in partida:
                if (i,j) == (casilla[1],casilla[2]) and casilla[0].isdigit():
                    listaBotones[i][j]['text'] = casilla[0] 
            f += 85
        c += 85
        f = 248


def crear_partida_guardada():
    global listaBotones
    global listaDigitos
    global lista_partida

    frame = Frame(ventana_jugar)

    # crea los 25 botones
    b1 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b2 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b3 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b4 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b5 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b6 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b7 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b8 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b9 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b10 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b11 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b12 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b13 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b14 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b15 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b16 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b17 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b18 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b19 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b20 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b21 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b22 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b23 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b24 = Button(ventana_jugar,bg="white",width = 5, height = 2)
    b25 = Button(ventana_jugar,bg="white",width = 5, height = 2)


    # matriz de botones 5x5
    listaBotones = [[b1, b2, b3, b4, b5],
                    [b6, b7, b8, b9, b10],
                    [b11, b12, b13, b14, b15],
                    [b16, b17, b18, b19, b20],
                    [b21, b22, b23, b24, b25]]

    # matriz de la partida

    copia = [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]]

    
    lista_operador_pos = []
    listaDigitos = []
    
    label = Label(frame,text="Dígitos")
    label.config(font=("Helvetica", 10),bg=color4)
    label.grid(row = 0, padx=7)


    # crea botones de digitos y los coloca en el frame
    fila = 1
    for i in range(1,6):
        boton1 = Button(frame,text=str(i),bg = 'white',command = lambda a=i,b=i-1 : click_digito(a,b), width = 5, height = 2)
        boton1.grid(row=fila,column=0,pady=7,padx=7)
        listaDigitos += [boton1]
        fila += 1

            
    # coloca la posicion del frame digitos segun configuracion
    if pos==1: # derecha
        frame.config(bg=color4,borderwidth=2,relief="solid")
        frame.place(x=700,y=230)
        
    if pos==2: # izquierda
        frame.config(bg=color4,borderwidth=2,relief="solid")
        frame.place(x=100,y=230)


    # crea lista de comparadores y coloca los comparadores segun la partida
    lista_comparadores = []
    
    for casilla in partida:
        if not casilla[0].isdigit():
            lista_comparadores.append((casilla[0],casilla[1],casilla[2]))


    f2 = 305
    c2 = 208
    for i in range(5):
        for j in range(5):
            for comparador in lista_comparadores: 
                if (comparador[1],comparador[2]) == (i,j):
                    
                    if comparador[0] == ">": 
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14),bg= main_color)
                        signo.place(x=f2,y=c2)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1],comparador[2]+1)))
                        
                    if comparador[0] == "<":
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14),bg= main_color)
                        signo.place(x=f2,y=c2)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1],comparador[2]+1)))
                        
                    if comparador[0] == "∧":
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14,"bold"),width=3,bg= main_color)
                        signo.place(x=f2-54,y=c2+43)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1]+1,comparador[2])))
                        
                    if comparador[0] == "v":
                        signo = Label(ventana_jugar,text=comparador[0],font= ("",14),width=3,bg= main_color)
                        signo.place(x=f2-54,y=c2+43)
                        lista_operador_pos.append((comparador[0],(comparador[1],comparador[2]),(comparador[1]+1,comparador[2])))
            f2 += 85
        c2 += 85
        f2 = 305

    # agrega los numeros fijos a la copia de la misma y los coloca en los botones segun la partida

    f = 248
    c = 198
    for i in range(5):
        for j in range(5):
            listaBotones[i][j]['command'] = lambda a=i,b=j : click_cuadricula(a,b,lista_operador_pos,copia)
            listaBotones[i][j].place(x=f,y=c)
            for casilla in partida:
                if (i,j) == (casilla[1],casilla[2]) and casilla[0].isdigit():
                    copia[i][j] = int(casilla[0])
                    listaBotones[i][j]['text'] = casilla[0]
            f += 85     
        c += 85
        f = 248


    # coloca los movimientos guardados en los botones
    for move in lista_movimientos:
        x = move[1]
        y = move[2]
        if lista_partida[x][y] != 0:
            listaBotones[x][y]['text'] = move[0]
    


def click_digito(dig,i):
    global digito,index
    global click
    global listaDigitos
    global paused
    
    digito = dig
    index = i
    listaDigitos[index]['bg'] = 'green'
    click = True


def click_cuadricula(x,y,operadores,copia): # valida cada movimiento
    global click
    global paused
    global lista_movimientos,lista_partida
    global paused
    
    if click:
        bandera = False
        texto = listaBotones[x][y]['text']
        listaDigitos[index]['bg'] = 'white'
        
        # comprueba si el elemento ya está en la columna
        for i in range(5): 
            if digito == lista_partida[i][y]:
                bandera = True

        # verifica si la posicion del digito a colocar es un numero fijo
        if copia[x][y] != 0:
            paused= True
            listaBotones[x][y]['bg'] = "red"
            messagebox.showerror(title="Error",message="El elemento es un dígito fijo")
            listaBotones[x][y]['bg'] = "white"
            pausas()


        # comprueba si digito está en la fila
        elif digito in lista_partida[x]:
            paused= True
            listaBotones[x][y]['bg'] = "red"
            listaBotones[x][y]['text'] = str(digito)
            messagebox.showerror(title="Error",message="El elemento está en la fila")

            if lista_partida[x][y]!=0:
                listaBotones[x][y]['text'] = lista_partida[x][y]
            else:
                listaBotones[x][y]['text'] = ""
            listaBotones[x][y]['bg'] = "white"
            pausas()
            
        elif bandera:
            paused= True
            listaBotones[x][y]['bg'] = "red"
            listaBotones[x][y]['text'] = str(digito)
            messagebox.showerror(title="Error",message="El elemento está en la columna")
            if lista_partida[x][y]!=0:
                listaBotones[x][y]['text'] = lista_partida[x][y]
            else:
                listaBotones[x][y]['text'] = ""
            listaBotones[x][y]['bg'] = "white"
            pausas()


        else:
            restricciones = operador(x,y,operadores)
            
            # 0 valida
            # 1 incumpla mayor
            # 2 incumple menor
            if copia[x][y] == 0: #copia para que me deje cambiarlo
                if restricciones == []:
                    lista_partida[x][y] = digito
                    listaBotones[x][y]['text'] = str(digito)
                    lista_movimientos += [(digito,x,y)]
                else:
                    estado = valida_desigualdad(restricciones,x,y)
                    if estado == 0:
                        lista_partida[x][y] = digito
                        listaBotones[x][y]['text'] = str(digito)
                        lista_movimientos += [(digito,x,y)]
                    if estado == 1:
                        paused = True
                        listaBotones[x][y]['bg'] = "red"
                        messagebox.showerror(title="Error",message="Incumple restriccion de mayor")
                        listaBotones[x][y]['bg'] = "white"
                        pausas()
                    if estado == 2:
                        paused = True
                        listaBotones[x][y]['bg'] = "red"
                        messagebox.showerror(title="Error",message="Incumple restriccion de menor")
                        listaBotones[x][y]['bg'] = "white"
                        pausas()

                    
        click = False
        comprueba = revision()
        if comprueba:
            gana_partida()
        
    else:
        listaBotones[x][y]['bg'] = "red"
        paused = True
        messagebox.showerror(title="Error", message="Primero debe seleccionar un digito antes de marcar una casilla de la cuadricula")
        listaBotones[x][y]['bg'] = "white"
        pausas()



def operador(x,y,operadores):
    # crea una lista con solo los operadores 
    lista = []
    for operador in operadores:
        for i in range(1,len(operador)):
            if operador[i] ==(x,y):
                lista.append(operador)

    return lista
            
        
def valida_desigualdad(restricciones,x,y):
    bandera = -1
    for restriccion in restricciones:
        x1 = restriccion[1][0]
        y1 = restriccion[1][1]
        x2 = restriccion[2][0]
        y2 = restriccion[2][1]
        if restriccion[0] == '>' or restriccion[0] == 'v':
            
            if lista_partida[x1][y1]==0 and lista_partida[x2][y2]==0:
                bandera = 0
            elif lista_partida[x1][y1]!=0 and lista_partida[x2][y2]==0:
                if digito>lista_partida[x1][y1] and (x,y)!=(x1,y1):
                    bandera = 1
                else:
                    bandera = 0
            elif lista_partida[x1][y1]==0 and lista_partida[x2][y2]!=0:
                if lista_partida[x2][y2]>digito and (x,y)!=(x1,y1):
                    bandera = 0
                if digito>lista_partida[x2][y2]:
                    bandera = 0
                else:
                    bandera = 1
            
            elif lista_partida[x2][y2]!=0 and lista_partida[x1][y1]!=0:
                
                if digito>lista_partida[x1][y1] and (x,y)!=(x1,y1):
                    bandera = 1
                if lista_partida[x2][y2]>digito and (x,y)!=(x1,y1):
                    bandera = 0
                if lista_partida[x2][y2]>digito and (x,y)==(x1,y1):
                    bandera = 1
                else:
                    bandera = 0
        else:
            if lista_partida[x1][y1]==0 and lista_partida[x2][y2]==0:
                bandera = 0
            elif lista_partida[x1][y1]!=0 and lista_partida[x2][y2]==0:
                if digito<lista_partida[x1][y1] and (x,y)!=(x1,y1):
                    bandera = 2
                else:
                    bandera = 0
            elif lista_partida[x1][y1]==0 and lista_partida[x2][y2]!=0:
                if lista_partida[x2][y2]<digito and (x,y)!=(x1,y1):
                    bandera = 0
                if digito<lista_partida[x2][y2]:
                    bandera = 0
                else:
                    bandera = 2
            
            elif lista_partida[x2][y2]!=0 and lista_partida[x1][y1]!=0:
                if digito<lista_partida[x1][y1] and (x,y)!=(x1,y1):
                    bandera = 2
                if lista_partida[x2][y2]<digito and (x,y)!=(x1,y1):
                    bandera = 0
                if lista_partida[x2][y2]<digito and (x,y)==(x1,y1):
                    bandera = 2
                else:
                    bandera = 0

    return bandera 

    
def revision():
    # revisa que no hay ningun cero en lista_partida para dar por entendido que ganó
    for fila in lista_partida:
        if 0 in fila:
            return False
    return True


def borrar_jugada():
    global listaBotones,lista_partida,lista_movimientos,jugadas_borradas
    global paused

    if lista_movimientos == []:
        paused = True
        messagebox.showerror(title="Error",message="No existen más movimientos")
        pausas()
    else:
        jugada = lista_movimientos.pop()
        jugadas_borradas.append(jugada)
        x = jugada[1] # fila
        y = jugada[2] # columna

        listaBotones[x][y]['text'] = ""
        lista_partida[x][y] = 0
        
    
def terminar_juego(): 
    global max_facil,max_inter,max_dificil
    global lista_facil,lista_inter,lista_dif
    global partida,modo
    global paused
    global s,m,h
    global segundos,minutos,horas
    global indicador2,indicador3,indicador4,indicador5
    global lista_movimientos,jugadas_borradas

    partida_anterior = partida

    paused = True
    indicador2 = False
    lista_movimientos = []
    jugadas_borradas = []
    
    respuesta = messagebox.askquestion(title="Confirmación",message="¿Desea terminar el juego?")
    if respuesta == "yes":
        s = 0
        m = 0
        h = 0
        if reloj == 3:
            segundos = s2
            minutos = m2
            horas = h2
    
        if modo == 1:
            if max_facil>0:
                if partida in lista_facil:
                    # elimina partida actual para que se escoja una diferente a esa
                    lista_facil.remove(partida)
                    # se resta la cantidad de partidas de la lista
                    max_facil -= 1
                    partida = elegir_partida()
                    indicador3 = True # indica que partida diferente fue elegida y no tendrá que volver a elegir partida como al principio cuando la nueva ventana jugar aparece
                    # se suma una vez que una partida diferente es elegida y se agrega la partida antes de la actual
                    max_facil += 1
                    lista_facil.append(partida_anterior)
                
        if modo == 2:
            if max_inter>0:
                if partida in lista_inter:
                    lista_inter.remove(partida)
                    max_inter -= 1
                    partida = elegir_partida()
                    indicador4 = True
                    max_inter += 1
                    lista_inter.append(partida_anterior)

        if modo == 3:
            if max_dificil>0:
                if partida in lista_dif:
                    lista_dif.remove(partida)
                    max_dificil -= 1
                    partida = elegir_partida()
                    indicador5 = True
                    max_dificil += 1
                    lista_dif.append(partida_anterior)

        if multinivel:
            modo = 4
        
        ventana_jugar.withdraw()
        jugar()
        
    else:
        pausas()


def borrar_juego():
    global listaBotones,lista_partida,lista_movimientos
    global paused,jugadas_borradas

    jugadas_borradas = []
    paused = True
    respuesta = messagebox.askquestion(title="Confirmación",message="¿Desea borrar el juego?")
    pausas()
    if respuesta == "yes":
        if lista_movimientos == []:
            paused = True
            messagebox.showinfo(title=None,message="El juego ya se ha borrado")
            pausas()
        else:
            for pos in lista_movimientos:
                x = pos[1] # fila
                y = pos[2] # columna
                listaBotones[x][y]['text'] = ""
                lista_partida[x][y] = 0
                lista_movimientos = lista_movimientos[1:]


def rehacer_jugada():
    global jugadas_borradas
    global lista_movimientos

    if jugadas_borradas!=[]:
        jugada = jugadas_borradas.pop()
        dig = jugada[0]
        x = jugada[1] # fila
        y = jugada[2] # columna

        listaBotones[x][y]['text'] = str(dig)
        lista_partida[x][y] = dig
        lista_movimientos.append(jugada)
    else:
        messagebox.showerror(title="Error", message="No hay jugadas para rehacer")
    


def solucion_juego():
    print('sirve')
    #backtracking


def posibles_jugadas(e1,e2,fila,columna,label_nuevo):
    global paused
    
    if fila == "" or columna == "":
        paused = True
        messagebox.showerror(title="Error",message="Debe colocar la fila y la columna de la casilla")
        pausas()

    elif not fila.isdigit() or not columna.isdigit():
        paused = True
        messagebox.showerror(title="Error",message="Entradas deben ser numeros")
        pausas()
        e1.delete(0,END)
        e2.delete(0,END)

    else:
        fila = int(fila)
        columna = int(columna)
        if not 1<=fila<=5 or not 1<=columna<=5:
            paused = True
            messagebox.showerror(title="Error",message="Número de fila y columna debe estar entre 1 y 5")
            pausas()
            
        else:
            fila -= 1
            columna -= 1

            if lista_partida[fila][columna]==0:
                # crea lista de la columna segun donde se ubique la posicion dela casilla
                cont = 0
                f = []
                c = []
                while cont<len(lista_partida):
                    elem = lista_partida[cont][columna]
                    c.append(elem)
                    cont+=1

                # crea lista de posibles jugadas
                posibles = []
                f = lista_partida[fila]
                for boton in listaDigitos:
                    num = int(boton['text'])
                    if num not in f and num not in c:
                        posibles.append(num)

                #si no hay posibles significa que la fila y la columna estan llenas
                #de lo contrario se convertirá a string para agregarlo a un label
                if posibles!=[]:
                    nuevo = ""
                    for num in posibles:
                        num = str(num)
                        nuevo+=num
                        nuevo+=" "
                        
                    if label_nuevo['text'] == "":
                        label_nuevo['text'] = nuevo
                    else:
                        label_nuevo['text'] = nuevo
                    label_nuevo.place(x=95,y=705)
                    # se deben tomar en cuenta los operadores????????????
                    
                else:
                    paused = True
                    messagebox.showinfo(title="Error",message="La casilla no tiene posibles jugadas")
                    pausas()

            else:
                paused = True
                messagebox.showinfo(title="Posibles jugadas",message="La casilla no tiene posibles jugadas")
                pausas()
            
            # limpia los entries
            e1.delete(0,END)
            e2.delete(0,END)

    
def gana_partida():
    global modo,multinivel
    
    ganar()
    datos_partida_arch()
    
    if multinivel:
        modo = modo+1
        if modo<3:
            iniciar(nombre)
        else:
            modo = 3
            iniciar(nombre)
            multinivel = False
    else:
        volver2()


def ganar():
    global max_facil,max_inter,max_dificil
    global lista_facil,lista_inter,lista_dif
    global s,m,h
    global proceso
    global segundos,minutos,horas
    global paused
    global indicador2,indicador3,indicador4,indicador5
    global lista_movimientos,jugadas_borradas

    paused = True
    indicador2 = False
    lista_movimientos = []
    jugadas_borradas = []

    # muestra proceso dependiendo del reloj escogido antes de reestablecer variables

    pr_s = int(proceso[-2:])
    pr_m = int(proceso[-5:-3])
    pr_h = int(proceso[:-6])
    
    if reloj == 1 or reloj == 2: 
        # reestablece variables a su valor de inicio
        if not multinivel:
            s = 0
            m = 0
            h = 0
        else:
            pr2_s = int(proceso_string[-2:])
            pr2_m = int(proceso_string[-5:-3])
            pr2_h = int(proceso_string[:-6])

            pr2_ss = pr2_s+(pr2_m*60)+(pr2_h*3600)
            pr_ss = pr_s+(pr_m*60)+(pr_h*3600)

            # resta de cuanto tiempo duró en completarlo
            dif = abs(pr2_ss-pr_ss)

            # proceso es actualizado al tiempo real que lo completó
            proceso = time.strftime('%H:%M:%S',time.gmtime(dif))

            s = pr_s
            m = pr_m
            h = pr_h
            
    if reloj == 3:
        if not expirado:
            ts_s = int(timer_string[-2:])
            ts_m = int(timer_string[-5:-3])
            ts_h = int(timer_string[:-6])

            # segundos de timer_string y proceso
            ts_ss = ts_s+(ts_m*60)+(ts_h*3600)
            pr2_ss = pr2_s+(pr2_m*60)+(pr2_h*3600)

            # resta de cuanto tiempo duró en completarlo
            dif = abs(ts_ss-pr2_ss)

            # proceso es actualizado al tiempo real que lo completó
            proceso = time.strftime('%H:%M:%S',time.gmtime(dif))
            
            # reestablece variables a su valor de inicio
        if not multinivel:
            segundos = s2
            minutos = m2
            horas = h2
            
        if multinivel:
            segundos = pr2_s
            minutos = pr2_m
            horas = pr2_h
                

    if modo == 1:
        messagebox.showinfo(title="Partida fácil completada",message="¡Excelente, buen trabajo!")
        indicador3 = False
        if partida in lista_facil:
            if len(lista_facil)>1:
                lista_facil.remove(partida)
                max_facil -= 1
            elif len(lista_facil)==1:
                # cuando solo queda una partida 
                lista_facil.remove(lista_facil[0])

            
    if modo == 2:
        messagebox.showinfo(title="Partida intermedio completada",message="¡Excelente, buen trabajo!")
        indicador4 = False
        if partida in lista_inter:
            if len(lista_inter)>1:
                lista_inter.remove(partida)
                max_inter -= 1
            elif len(lista_inter)==1:
                lista_inter.remove(lista_inter[0])
            
    if modo == 3:
        messagebox.showinfo(title="Partida difícil completada",message="¡Excelente, buen trabajo!")
        indicador5 = False
        if partida in lista_dif:
            if len(lista_dif)>1:
                lista_dif.remove(partida)
                max_dificil -= 1
            elif len(lista_dif)==1:
                lista_dif.remove(lista_dif[0])


def datos_partida_arch():
    # guarda datos de nombre, modo, proceso y eso llega a top10 solo si ya gana partida
    
    registro = (nombre,proceso)

    if not path.exists('futoshiki2020top10.dat'):
        facil = []
        intermedio = []
        dificil = []

        if modo == 1:
            facil.append(registro)

        if modo == 2:
            intermedio.append(registro)

        if modo == 3:
            dificil.append(registro)
            
        archivo = open('futoshiki2020top10.dat',"wb")
        pickle.dump(facil,archivo)
        pickle.dump(intermedio,archivo)
        pickle.dump(dificil,archivo)
        
        archivo.close()
        
    else:
        archivo = open('futoshiki2020top10.dat',"rb")
        facil = pickle.load(archivo)
        intermedio = pickle.load(archivo)
        dificil = pickle.load(archivo)
        archivo.close()

        if modo == 1:
            for dato in facil:
                ds = int(dato[1][-2:])
                dm = int(dato[1][-5:-3])
                dh = int(dato[1][:-6])

                rs = int(registro[1][-2:])
                rm = int(registro[1][-5:-3])
                rh = int(registro[1][:-6])

                # pasa a segundos los tiempos para cmompararlos
                dss = ds+(dm*60)+(dh*3600)
                rss = rs+(rm*60)+(rh*3600)

                if rss<=dss:
                    i = facil.index(dato)
                    facil.insert(i,registro)
                    break
                else:
                    i = facil.index(dato)+1
                    if registro not in facil:
                        facil.insert(i,registro)

        if modo == 2:
            for dato in intermedio:
                ds = int(dato[1][-2:])
                dm = int(dato[1][-5:-3])
                dh = int(dato[1][:-6])

                rs = int(registro[1][-2:])
                rm = int(registro[1][-5:-3])
                rh = int(registro[1][:-6])

                # pasa a segundos los tiempos para cmompararlos
                dss = ds+(dm*60)+(dh*3600)
                rss = rs+(rm*60)+(rh*3600)

                if rss<=dss:
                    i = intermedio.index(dato)
                    intermedio.insert(i,registro)
                    break
                else:
                    i = intermedio.index(dato)+1
                    if registro not in intermedio:
                        intermedio.insert(i,registro)

        if modo == 3:
            for dato in dificil:
                ds = int(dato[1][-2:])
                dm = int(dato[1][-5:-3])
                dh = int(dato[1][:-6])

                rs = int(registro[1][-2:])
                rm = int(registro[1][-5:-3])
                rh = int(registro[1][:-6])

                # pasa a segundos los tiempos para cmompararlos
                dss = ds+(dm*60)+(dh*3600)
                rss = rs+(rm*60)+(rh*3600)

                if rss<=dss:
                    i = dificil.index(dato)
                    dificil.insert(i,registro)
                    break
                else:
                    i = dificil.index(dato)+1
                    if registro not in dificil:
                        dificil.insert(i,registro) 

        archivo = open('futoshiki2020top10.dat',"wb")
        pickle.dump(facil,archivo)
        pickle.dump(intermedio,archivo)
        pickle.dump(dificil,archivo)

        archivo.close() 


def top10_ventana():
    
    global ventana_top
    global paused

    paused = True
    
     
    ventana_jugar.withdraw()
    ventana_top = Tk()
    ventana_top.geometry('700x800+600+100')
    ventana_top.title("Top 10")
    ventana_top.config(background = main_color)
    ventana_top.resizable(width = False,height = False)

    label1 = Label(ventana_top,text="Nivel: Fácil",bg=main_color,font=("",12))
    label2 = Label(ventana_top,text="Jugador",bg=main_color,font=("",12))
    label3 = Label(ventana_top,text="Tiempo",bg=main_color,font=("",12))

    label1.place(x=10,y=15)
    label2.place(x=210,y=15)
    label3.place(x=370,y=15)


    label4 = Label(ventana_top,text="Nivel: Intermedio",bg=main_color,font=("",12))
    label5 = Label(ventana_top,text="Jugador",bg=main_color,font=("",12))
    label6 = Label(ventana_top,text="Tiempo",bg=main_color,font=("",12))

    label4.place(x=10,y=270)
    label5.place(x=210,y=270)
    label6.place(x=370,y=270)


    label7 = Label(ventana_top,text="Nivel: Difícil",bg=main_color,font=("",12))
    label8 = Label(ventana_top,text="Jugador",bg=main_color,font=("",12))
    label9 = Label(ventana_top,text="Tiempo",bg=main_color,font=("",12))

    label7.place(x=10,y=550)
    label8.place(x=210,y=550)
    label9.place(x=370,y=550)

    if path.exists('futoshiki2020top10.dat'):
        archivo = open('futoshiki2020top10.dat',"rb")

        facil = pickle.load(archivo)
        intermedio = pickle.load(archivo)
        dificil = pickle.load(archivo)
            
        archivo.close()

        if facil!=[]:
            posicion_label(190,50,facil)
            f = 210
            c = 50
            for dato in facil:
                label_dato1 = Label(ventana_top,text=str(dato[0]),font=("",10),fg='red',bg=main_color)
                label_dato2 = Label(ventana_top,text=str(dato[1]),font=("",10),fg='red',bg=main_color)

                label_dato1.place(x=f,y=c)
                label_dato2.place(x=f+160,y=c)

                c += 20

                i = facil.index(dato) # se detiene de colocar los labels cuando el indice sea 9
                if i == 9:
                    break
        else:
            label = Label(ventana_top,text="NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL",bg = main_color,fg='red',font=('',10))
            label.place(x=10,y=55)

        if intermedio!=[]:
            posicion_label(190,305,intermedio)
            f = 210
            c = 305
            for dato in intermedio:
                label_dato1 = Label(ventana_top,text=str(dato[0]),font=("",10),fg='red',bg=main_color)
                label_dato2 = Label(ventana_top,text=str(dato[1]),font=("",10),fg='red',bg=main_color)

                label_dato1.place(x=f,y=c)
                label_dato2.place(x=f+160,y=c)

                c += 20

                i = intermedio.index(dato)
                if i == 9:
                    break

        else:
            label = Label(ventana_top,text="NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL",bg = main_color,fg='red',font=('',10))
            label.place(x=10,y=310)

        if dificil!=[]:
            posicion_label(190,585,dificil)
            f = 210
            c = 585
            for dato in dificil:
                label_dato1 = Label(ventana_top,text=str(dato[0]),font=("",10),fg='red',bg=main_color)
                label_dato2 = Label(ventana_top,text=str(dato[1]),font=("",10),fg='red',bg=main_color)

                label_dato1.place(x=f,y=c)
                label_dato2.place(x=f+160,y=c)

                c += 20

                i = dificil.index(dato)
                if i == 9:
                    break

        else:
            label = Label(ventana_top,text="NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL",bg = main_color,fg='red',font=('',10))
            label.place(x=10,y=590)
            
    label1 = Label(ventana_top,text="NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL",bg = main_color,fg='red',font=('',10))
    label1.place(x=10,y=55)
    
    label2 = Label(ventana_top,text="NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL",bg = main_color,fg='red',font=('',10))
    label2.place(x=10,y=310)
            
    label3 = Label(ventana_top,text="NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL",bg = main_color,fg='red',font=('',10))
    label3.place(x=10,y=590)
    
    b_continuar = Button(ventana_top,text="Continuar jugando",width = 15,bg = color2,command = volver3)
    b_continuar.place(x=545,y=730)

    b_imprimir = Button(ventana_top,text="Imprimir ",bg=color2,width = 15, command=imprimir_top)
    b_imprimir.place(x=545,y=680)

    ventana_top.mainloop()


def posicion_label(f,c,nivel):
    # coloca los numeros del top en la ventana
    for i in range(1,11):
        label = Label(ventana_top,text=str(i)+'.',font=("",10),bg=main_color)
        label.place(x=f,y=c)
        c += 20
        if i == len(nivel):
            break


def imprimir_top():
    #crea un archivo pdf del top10 de cada nivel
    #cada nivel se despiega en una pagina diferente

    file = FPDF()
    file.add_page()
    file.set_font('Arial','B',16)
    file.text(85,20,'Top 10 Futoshiki')
    file.ln(20) # line break

    if path.exists('futoshiki2020top10.dat'):
        archivo = open('futoshiki2020top10.dat',"rb")

        facil = pickle.load(archivo)
        intermedio = pickle.load(archivo)
        dificil = pickle.load(archivo)    
        archivo.close()

        file.set_font('Arial','B',14)
        file.write(10,'Nivel Fácil')

        file.set_font('Arial','',14)
        file.text(10,50,'Jugador                           Tiempo')
        file.ln(20)

        if facil == []:
            file.text(10,60,'NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL')
        else:
            x = 10
            y = 60
            pos = 1
            for dato in facil:
                file.text(x,y,str(pos)+'. '+str(dato[0]))
                file.text(x+55,y,str(dato[1]))
                y += 10
                pos += 1
                i = facil.index(dato)
                if i == 9:
                    break

        agrega_pagina_formato(file)
        
        file.set_font('Arial','B',14)
        file.write(10,'Nivel Intermedio')

        file.set_font('Arial','',14)
        file.text(10,50,'Jugador                           Tiempo')
        file.ln(20)
        
        if intermedio == []:
            file.text(10,60,'NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL')

        else:
            x = 10
            y = 60
            pos = 1
            for dato in intermedio:
                file.text(x,y,str(pos)+'. '+str(dato[0]))
                file.text(x+55,y,str(dato[1]))
                y += 10
                pos += 1
                i = intermedio.index(dato)
                if i == 9:
                    break

        agrega_pagina_formato(file)
        
        file.set_font('Arial','B',14)
        file.write(10,'Nivel Difícil')

        file.set_font('Arial','',14)
        file.text(10,50,'Jugador                           Tiempo')
        file.ln(20)    

        if dificil == []:
            file.text(10,60,'NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL')

        else:
            x = 10
            y = 60
            pos = 1
            for dato in dificil:
                file.text(x,y,str(pos)+'. '+str(dato[0]))
                file.text(x+55,y,str(dato[1]))
                y += 10
                pos += 1
                i = dificil.index(dato)
                if i == 9:
                    break
        
            
    else:
        file.set_font('Arial','B',14)
        file.write(10,'Nivel Fácil')

        file.set_font('Arial','',14)
        file.text(10,50,'Jugador                           Tiempo')
        file.ln(20)
        file.text(10,60,'NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL')

        agrega_pagina_formato(file)

        file.set_font('Arial','B',14)
        file.write(10,'Nivel Intermedio')

        file.set_font('Arial','',14)
        file.text(10,50,'Jugador                           Tiempo')
        file.ln(20)
        file.text(10,60,'NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL')

        
        agrega_pagina_formato(file)

        file.set_font('Arial','B',14)
        file.write(10,'Nivel Difícil')

        file.set_font('Arial','',14)
        file.text(10,50,'Jugador                           Tiempo')
        file.ln(20)
        file.text(10,60,'NO HAY REGISTRO DE JUGADORES EN ESTE NIVEL')

    # guarda y abre documento      
    file.output('Top10_Futoshiki.pdf','F')
    os.startfile('Top10_Futoshiki.pdf')
        

def agrega_pagina_formato(file):

    file.add_page()
    file.set_font('Arial','B',16)
    file.text(85,20,'Top 10 Futoshiki')
    file.ln(20) # line break


  
def volver3(): 
    global paused
    paused = False

    if reloj == 1:
        if indicador2==True:
            clock()
            
    if reloj == 2:
        if indicador2==True:
            clock2()
            
    if reloj == 3:
        if indicador2==True:
            timer()
   
    ventana_top.withdraw()
    ventana_jugar.deiconify()
     


def pausas(): # controla las pausas y continua con el reloj respectivo
    global paused

    paused = False

    if reloj == 1:
        clock()
    if reloj == 2:
        clock2()
    if reloj == 3:
        timer()


def volver2():
    ventana_jugar.withdraw()
    principal.deiconify()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def guardar():
    global s,m,h
    global segundos,minutos,horas
    global paused
    global guardado
    global modo
    # lee archivo de configuracion
    archivo = open("futoshiki2020juegoactual.dat","wb")

    paused = True

    if reloj == 3:
        segundos = int(proceso[-2:])
        minutos = int(proceso[-5:-3])
        horas = int(proceso[:-6])

    if reloj == 1 or reloj == 2:
        s = int(proceso[-2:])
        m = int(proceso[-5:-3])
        h = int(proceso[:-6])

    if multinivel:
        modo = 4

    name = nombre
    mod = modo
    r = reloj
    p = pos
    relojS = s
    relojM = m
    relojH = h
    timerS = segundos
    timerM = minutos
    timerH = horas
    par = partida
    lp = lista_partida
    lm = lista_movimientos
    lr = jugadas_borradas

    
    pickle.dump(name, archivo)
    pickle.dump(mod, archivo)
    pickle.dump(r,archivo)
    pickle.dump(p,archivo)
    pickle.dump(relojS,archivo)
    pickle.dump(relojM,archivo)
    pickle.dump(relojH,archivo)
    pickle.dump(timerS,archivo)
    pickle.dump(timerM,archivo)
    pickle.dump(timerH,archivo)
    pickle.dump(par,archivo)
    pickle.dump(lp,archivo)
    pickle.dump(lm,archivo)
    pickle.dump(lr,archivo)

    archivo.close()
    guardado = True
    volver2()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def cargar():
    # considerar el boton de terminar para el maximo de cada lista de partidas etc etc
    global nombre,modo,reloj,pos
    global s,m,h
    global segundos,minutos,horas
    global partida,lista_partida,lista_movimientos,jugadas_borradas
    global b_iniciar,b_cargar
    global guardado,modo

    if path.exists("futoshiki2020juegoactual.dat"): # retorna True si el archivo existe
        archivo = open("futoshiki2020juegoactual.dat","rb")

        nombre = pickle.load(archivo)
        modo = pickle.load(archivo)
        reloj = pickle.load(archivo)
        pos = pickle.load(archivo)
        s = pickle.load(archivo)
        m = pickle.load(archivo)
        h = pickle.load(archivo)
        segundos = pickle.load(archivo)
        minutos = pickle.load(archivo)
        horas = pickle.load(archivo)
        partida = pickle.load(archivo)
        lista_partida = pickle.load(archivo)
        lista_movimientos = pickle.load(archivo)
        jugadas_borradas = pickle.load(archivo)
        
        archivo.close()
        
        guardado = False
        label_load = Label(ventana_jugar,text="Partida cargada, inicie juego para continuar",bg=main_color,font=(None,14))
        b_iniciar['command'] = lambda:iniciar2(label_load)
        b_cargar['state'] = 'disable'
        label_nombre = Label(ventana_jugar,text=nombre) # esconde el entry tapandolo
        label_nombre.place(x=420,y=123,width = '200')
        label_load.place(x=225,y=350)
        

    else:
        messagebox.showerror(title="Error",message="No hay partida guardada")


def iniciar2(label):
    global nombre
    global b_iniciar,b_borrar1,b_terminar,b_borrar2,b_guardar,b_cargar,b_devolverse,b_rehacer,b_solucion,b_posibles_jugadas
    global max_facil,max_inter,max_dificil
    global lista_facil,lista_inter,lista_dif,nivel

    label.destroy()
    nivel.destroy()

    frame = Frame(ventana_jugar,bg=color4)
    label_fila = Label(frame,text="Fila casilla",bg=color4,font=(None,11))
    label_fila.grid(row=0,column=0)
    entry_pj1 = Entry(frame,width = 6)
    entry_pj1.grid(row=0,column=1)
    label_col = Label(frame,text="Columna casilla",bg=color4,font=(None,11))
    label_col.grid(row=1,column=0)
    entry_pj2 = Entry(frame,width = 6)
    entry_pj2.grid(row=1,column=1)

    frame.place(x=45,y=740)

    label_nuevo = Label(ventana_jugar,text="",font=(None,12),bg = main_color,fg='blue')
    
    if modo == 1:
        nivel = Label(ventana_jugar,text="Nivel: Fácil",bg = main_color, font = ("Helvetica",14))
        nivel.pack()
        
    if modo == 2:
        nivel = Label(ventana_jugar,text="Nivel: Intermedio",bg = main_color, font = ("Helvetica",14))
        nivel.pack()
        
    if modo == 3:
        nivel = Label(ventana_jugar,text="Nivel: Difícil",bg = main_color, font = ("Helvetica",14))
        nivel.pack()

    if modo == 4:
        nivel = Label(ventana_jugar,text="Nivel: Multinivel",bg = main_color, font = ("Helvetica",14))
        nivel.pack()
        
    b_iniciar['command'] = lambda:iniciar(nombre)
        
    # cambia el estado de los botones al iniciar juego
    b_iniciar['state'] = 'disable'
    b_borrar1['state'] = 'normal'
    b_terminar['state'] = 'normal'
    b_borrar2['state'] = 'normal'
    b_guardar['state'] = 'normal'
    b_cargar['state'] = 'disable'
    b_devolverse['state'] = 'disable'
    b_rehacer['state'] = 'normal'
    b_solucion['state'] = 'normal'
    b_posibles_jugadas['state'] = 'normal'
    b_posibles_jugadas['command'] = lambda:posibles_jugadas(entry_pj1,entry_pj2,entry_pj1.get(),entry_pj2.get(),label_nuevo)
    
    relojes()
    crear_partida_guardada()


    
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def configuracion():
    global var1,var2,var3
    global ventana_config
    global indicador

    indicador = True

    principal.withdraw()
    ventana_config = Tk()
    ventana_config.geometry('700x800+600+100')
    ventana_config.title("Configuración")
    ventana_config.config(background = main_color)
    ventana_config.resizable(width = False,height = False)

    # modo de juego
    mensaje = Message(ventana_config,text="Modo de juego")
    mensaje.place(x=10,y=20)
    mensaje.config(fg = color3,bg = main_color,font =('Segoe Print',12),width='300')

    var1 = IntVar(ventana_config)
    radioboton1 = Radiobutton(ventana_config,text="Fácil",font = (None,10),variable = var1, value = 1)
    radioboton2 = Radiobutton(ventana_config,text="Intermedio",font = (None,10),variable = var1, value = 2)
    radioboton3 = Radiobutton(ventana_config,text="Difícil",font = (None,10),variable = var1 , value = 3)
    radioboton4 = Radiobutton(ventana_config,text="Multinivel",font = (None,10),variable = var1 , value = 4)

    radioboton1.config(bg = main_color)
    radioboton2.config(bg = main_color)
    radioboton3.config(bg = main_color)
    radioboton4.config(bg = main_color)
    
    radioboton1.place(x=40,y=70)
    radioboton2.place(x=40,y=95)
    radioboton3.place(x=40,y=120)
    radioboton4.place(x=40,y=145)

    # reloj o timer
    mensaje2 = Message(ventana_config,text="Reloj\n")
    mensaje2.place(x=10,y=180)
    mensaje2.config(fg = color3,bg = main_color,font =('Segoe Print',12),width='300')
                    
    var2 = IntVar(ventana_config)
    radioboton4 = Radiobutton(ventana_config,text="Sí",font = (None,10),variable = var2, value = 1)
    radioboton5 = Radiobutton(ventana_config,text="No",font = (None,10),variable = var2, value = 2)
    radioboton6 = Radiobutton(ventana_config,text="Timer",font = (None,10),variable = var2, value = 3)

    radioboton4.config(bg = main_color)
    radioboton5.config(bg = main_color)
    radioboton6.config(bg = main_color)

    radioboton4.place(x=40,y=230)
    radioboton5.place(x=40,y=255)
    radioboton6.place(x=40,y=280)
    

    # datos para el timer en caso de que reloj tenga como valor un 3

    frame = Frame(ventana_config)
    m_horas = Label(frame,text="Horas")
    m_horas.config(font=("system",5),bg = color4)
    m_mins = Label(frame,text="Minutos")
    m_mins.config(font=("system",5),bg = color4)
    m_seg = Label(frame,text="Segundos")
    m_seg.config(font=("system",5),bg = color4)

    m_horas.grid(row=15,column=15,padx=5,pady=5)
    m_mins.grid(row=15,column=16,padx=5,pady=5)
    m_seg.grid(row=15,column=17,padx=5,pady=5)

    H = Entry(frame,width=6)
    M = Entry(frame,width=6)
    S = Entry(frame,width=6)
    
    H.grid(row=16,column=15,padx=5,pady=5)
    M.grid(row=16,column=16,padx=5,pady=5)
    S.grid(row=16,column=17,padx=5,pady=5)

    frame.config(bg=color4,borderwidth=2,relief="solid")
    frame.place(x=230,y=225)
    

    # posicion digitos
    mensaje3 = Message(ventana_config,text="Posición dígitos\n")
    mensaje3.config(fg = color3,bg = main_color,font =('Segoe Print',12),width='300')
    mensaje3.place(x=10,y=330)

    var3 = IntVar(ventana_config)
    radioboton7 = Radiobutton(ventana_config,text="Derecha",font = (None,10),variable = var3, value = 1)
    radioboton8 = Radiobutton(ventana_config,text="Izquierda",font = (None,10),variable = var3, value = 2)

    radioboton7.config(bg = main_color)
    radioboton8.config(bg = main_color)
    
    radioboton7.place(x=40,y=380)
    radioboton8.place(x=40,y=405)
    
    b_volver = Button(ventana_config,text="Volver a la pantalla principal",bg = color2,command=lambda:comprueba(H.get(),M.get(),S.get()))
    b_volver.place(x=500,y=730)

    if var1.get() == 0:
        var1.set(1)
        
    if var2.get() == 0:
        var2.set(1)
        
    if var3.get() == 0:
        var3.set(1)

        
    ventana_config.mainloop()


def comprueba(r1,r2,r3):
    global segundos,minutos,horas
    global modo,reloj,pos

    modo = var1.get()
    reloj = var2.get()
    pos = var3.get()
    
    if reloj==3:
        horas = r1
        minutos = r2
        segundos = r3
        if horas == "" or minutos == "" or segundos == "":
            messagebox.showerror("Error","Ingrese horas, minutos y segundos para el timer",parent= ventana_config)
        elif int(horas)==0 and int(minutos)==0 and int(segundos)==0:
            messagebox.showerror("Error","Ingrese un tiempo válido",parent= ventana_config)
        elif horas.isdigit()==False or minutos.isdigit()==False or segundos.isdigit()==False:
            messagebox.showerror("Error","Entradas deben ser numeros enteros",parent= ventana_config)
        elif int(horas)>2:
            messagebox.showerror("Error","La cantidad de horas debe estar entre 0 y 2",parent= ventana_config)
        elif int(minutos)>59:
            messagebox.showerror("Error","La cantidad de minutos debe estar entre 0 y 59",parent= ventana_config)
        elif int(segundos)>59:
            messagebox.showerror("Error","La cantidad de segundos debe estar entre 0 y 59",parent= ventana_config)
        else:
            volver()
    else:
        horas = 0
        minutos = 0
        segundos = 0
        volver()

    arch_config()


def arch_config():

    archivo = open("futoshiki2020configuracion.dat","wb")

    config = [modo,reloj,horas,minutos,segundos,pos]
    pickle.dump(config, archivo)
    archivo.close()


def volver():
    ventana_config.withdraw()
    principal.deiconify()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def acercade():

    ventana_acercade = Toplevel()
    frame = Frame(ventana_acercade)
    ventana_acercade.geometry('700x700+700+200') # ventana se abre en el centro de la pantalla buscar codigo en fotos
    ventana_acercade.title("Acerca de")
    ventana_acercade.configure(background = main_color)
    ventana_acercade.resizable(width = False,height = False)

    label1 = Label(frame,text="Nombre del Programa: Futoshiki",bg = "peach puff",font=(None,15))
    label2 = Label(frame,text="Autora: Alexia Cerdas Aguilar",bg = "peach puff",font=(None,15))
    label3 = Label(frame,text="Fecha creación: 30/6/20",bg = "peach puff",font=(None,15))
    label4 = Label(frame,text="Versión: 1.0.0",bg = "peach puff",font=(None,15))

    label1.grid(row=0,pady=12,padx=5)
    label2.grid(row=1,pady=12,padx=5)
    label3.grid(row=2,pady=12,padx=5)
    label4.grid(row=3,pady=12,padx=5)

    frame.place(x=175,y=200)
    frame.config(bg = "peach puff",borderwidth=2,relief="solid")
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def ayuda():
    os.startfile('manual_de_usuario_futoshiki.pdf')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def salir():
    #elimina la ventana sin destruirla
    principal.withdraw()
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ventana principal
label_nombre_juego = Label(principal, text = "FUTOSHIKI")
label_nombre_juego.config(font = main_titulo_font)
label_nombre_juego.pack(pady = 50)
label_nombre_juego.config(bg = main_color)

imagen = PhotoImage(file = 'futoshiki2.png')
label_img = Label(principal,image=imagen)
label_img.place(x=280,y=150)


principal.geometry('850x850+500+80') # ventana se abre en el centro de la pantalla buscar codigo en fotos
principal.title("Principal")
principal.configure(background = main_color)
principal.resizable(width = False,height = False)

b_jugar = Button(principal,text = "Jugar",command= jugar,font = button_main_font,bg = color2,width = 12,height = 2)
b_jugar.place(x=275,y=510)
b_config = Button(principal,text = "Configuración",command = configuracion,font = button_main_font,bg = color2,width = 12,height = 2)
b_config.place(x=445,y=510)
b_acercade = Button(principal,text = "Acerca de",command = acercade,font = button_main_font,bg=color2,width = 12,height = 2)
b_acercade.place(x=275,y=610)
b_ayuda = Button(principal,text = "Ayuda",command = ayuda,font = button_main_font,bg = color2,width = 12,height = 2)
b_ayuda.place(x=445,y=610)
b_salir = Button(principal,text = "Salir",command = salir,font = button_main_font,bg = color2,width = 12,height = 2)
b_salir.place(x=360,y=710)

principal.mainloop()
