from tkinter import *
import socket
from threading import *
from tkinter.scrolledtext import ScrolledText

class msj_entrante():
  def __init__(self, conexion, mensaje):
    self.conexion = conexion
    self.mensaje = mensaje
    while 1:
      try:
        text = self.conexion.recv(1024)
        if not text: break
        self.mensaje.configure(state=NORMAL)
        self.mensaje.tag_config("yo", foreground='black', font='Fixedsys 14')
        self.mensaje.insert(END,'Cliente  >> %s\n'%text,"yo")
        self.mensaje.configure(state=DISABLED)
        self.mensaje.see(END)
      except:
        break

class Principal(Thread):
  conexion = socket.socket()
  conexion.bind(('localhost', 20001))
  conexion.listen(5)
  client,addr = conexion.accept()

  def __init__(self, master):
    Thread.__init__(self)
    frame = Frame(master)
    frame.pack()
    self.mensaje = ScrolledText(frame, height=10, width=80, bg='mint cream', state=NORMAL)
    self.mensaje.pack()
    sframe = Frame(frame)
    sframe.pack(anchor='w')
    self.pro = Label(sframe, text="Servidor >>");
    self.env_msj = Entry(sframe,width=80)
    self.env_msj.focus_set()
    self.env_msj.bind(sequence="<Return>", func=self.enviar)
    self.pro.pack(side=LEFT)
    self.env_msj.pack(side=LEFT)
    self.boton = Button(text="Cerrar", command = ventana.destroy, height=2, width=10, bg="MistyRose3")
    self.boton.pack(side=RIGHT)
    self.mensaje.tag_config("yo", foreground='black', font='Fixedsys 14')
    self.mensaje.insert(END,'Bienvenido al Chat Servidor\n\n',"yo")
    self.mensaje.configure(state=DISABLED)

  def enviar(self, args):
    self.mensaje.configure(state=NORMAL)
    text = self.env_msj.get()
    if text=="": text=" "
    self.mensaje.tag_config("el", foreground='midnight blue', font='Fixedsys 14')
    self.mensaje.insert(END,'Servidor >> %s \n'%text,"el")
    self.env_msj.delete(0,END)
    self.client.send(str.encode(text))
    self.env_msj.focus_set()
    self.mensaje.configure(state=DISABLED)
    self.mensaje.see(END)

  def run(self):
    msj_entrante(self.client, self.mensaje)

ventana = Tk()
ventana.title('Chat del Servidor')
principal = Principal(ventana).start()
ventana.mainloop()
