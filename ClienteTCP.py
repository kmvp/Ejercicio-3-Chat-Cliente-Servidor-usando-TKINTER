from tkinter import *
import socket
from threading import *
from tkinter.scrolledtext import ScrolledText

class msj_entrante():
  def __init__(self, conexion, mensaje):
    while 1:
      try:
        text = conexion.recv(1024)
        if not text: break
        mensaje.configure(state='normal')
        mensaje.tag_config("yo", foreground='black', font='Fixedsys 14')
        mensaje.insert(END,'Servidor >> %s\n'%text,"yo")
        mensaje.configure(state='disabled')
        mensaje.see(END)
      except:
        break

class Principal(Thread):
  client = socket.socket()
  client.connect(('localhost', 20001))

  def __init__(self, master):
    Thread.__init__(self)
    frame = Frame(master)
    frame.pack()
    self.mensaje = ScrolledText(frame, height=10, width=80, bg='mint cream')
    self.mensaje.pack()
    self.mensaje.tag_config("yo", foreground='black', font='Fixedsys 14')
    self.mensaje.insert(END,'Bienvenido al Chat Cliente\n\n',"yo")
    self.mensaje.configure(state='disabled')
    sframe = Frame(frame)
    sframe.pack(anchor='w')
    self.pro = Label(sframe, text="Cliente  >>");
    self.env_msj = Entry(sframe,width=80)
    self.env_msj.focus_set()
    self.env_msj.bind(sequence="<Return>", func=self.enviar)
    self.pro.pack(side=LEFT)
    self.env_msj.pack(side=LEFT)
    self.boton = Button(text="Cerrar", command = ventana.destroy, height=2, width=10, bg="MistyRose3")
    self.boton.pack(side=RIGHT)

  def enviar(self, args):
    self.mensaje.configure(state='normal')
    text = self.env_msj.get()
    if text=="": text=" "
    self.mensaje.tag_config("el", foreground='midnight blue', font='Fixedsys 14')
    self.mensaje.insert(END,'Cliente  >> %s\n'%text,"el")
    self.env_msj.delete(0,END)
    self.client.send(str.encode(text))
    self.env_msj.focus_set()
    self.mensaje.configure(state='disabled')
    self.mensaje.see(END)

  def run(self):
    msj_entrante(self.client, self.mensaje)

ventana = Tk()
ventana.title('Chat del Cliente')
principal = Principal(ventana).start()
ventana.mainloop()
