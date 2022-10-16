import telebot
from datetime import date
from datetime import datetime
from tkinter import * 
import json
import time
import pygame.mixer


pygame.init()

current_time = datetime.now()

def add_digit(digit):
    value = mleco.get() + str(digit)
    mleco.delete(0, END)
    mleco.insert(0, value)
    pygame.mixer.music.load('click.mp3')
    pygame.mixer.music.play()
    
def save():
    text = "\n"  + " " + mleco.get() + " " + "liters" + " " + str(current_time) 
    filename = "data_list.txt"
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
    mleco.delete(0, END)
    mleco.insert(0, "Сохранено")
    pygame.mixer.music.load('click.mp3')
    pygame.mixer.music.play()

    
def clear():
    mleco.delete(0, END)
    pygame.mixer.music.load('click.mp3')
    pygame.mixer.music.play()


 
win = Tk()
win.geometry("240x280+100+200")
win.title("Молочный справочник")

mleco = Entry(win, justify=RIGHT, font=('Arial', 15))

mleco.grid(row=0, column=0, columnspan=4, padx=7, pady=5)

Button(text='1', font=('Arial', 12), command=lambda : add_digit(1)).grid(row=1, column=0, stick='wens', padx=1, pady=1)
Button(text='2', font=('Arial', 12), command=lambda : add_digit(2)).grid(row=1, column=1, stick='wens', padx=1, pady=1)
Button(text='3', font=('Arial', 12), command=lambda : add_digit(3)).grid(row=1, column=2, stick='wens', padx=1, pady=1)
Button(text='4', font=('Arial', 12), command=lambda : add_digit(4)).grid(row=2, column=0, stick='wens', padx=1, pady=1)
Button(text='5', font=('Arial', 12), command=lambda : add_digit(5)).grid(row=2, column=1, stick='wens', padx=1, pady=1)
Button(text='6', font=('Arial', 12), command=lambda : add_digit(6)).grid(row=2, column=2, stick='wens', padx=1, pady=2)
Button(text='7', font=('Arial', 12), command=lambda : add_digit(7)).grid(row=3, column=0, stick='wens', padx=1, pady=1)
Button(text='8', font=('Arial', 12), command=lambda : add_digit(8)).grid(row=3, column=1, stick='wens', padx=1, pady=1)
Button(text='9', font=('Arial', 12), command=lambda : add_digit(9)).grid(row=3, column=2, stick='wens', padx=1, pady=1)
Button(text='0', font=('Arial', 12), command=lambda : add_digit(0)).grid(row=4, column=1, stick='wens', padx=1, pady=1)
Button(text='.', font=('Arial', 12), command=lambda : add_digit('.')).grid(row=4, column=2, stick='wens', padx=1, pady=1)
Button(text='Save', font=('Arial', 12), command=lambda : save()).grid(row=4, column=0, stick='wens', padx=1, pady=1)
Button(text='Clear', font=('Arial', 12), command=lambda : clear()).grid(row=1, column=3, stick='wens', padx=1, pady=1)


win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)

win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=60)
win.grid_rowconfigure(4, minsize=60)

win.mainloop()


token = "токен"   
bot = telebot.TeleBot(token=token)


@bot.message_handler(content_types=['text'])
def send(message):
    try:
        with open("data_list.txt","rb") as file:
            f = file.read()

        bot.send_document(message.chat.id, f, "data_list.txt")

    except:
        bot.send_message(message.chat.id, "файл не найден")
        print("not found")
bot.polling()

