import telebot
from telebot import types # для указание типов
import config

from datetime import date
from datetime import datetime
from tkinter import * 
import json
import time
import pygame.mixer
import sqlite3



pygame.init()

date = datetime.now().strftime('%Y-%m-%d')
time = datetime.now().strftime('%H:%M')

win = Tk()
win.geometry("240x280+100+200")
win.title("Молочный справочник")

mleco = Entry(win, justify=RIGHT, font=('Arial', 15))


def add_digit(digit):
    value = mleco.get() + str(digit)
    mleco.delete(0, END)
    mleco.insert(0, value)
    pygame.mixer.music.load('click.mp3')
    pygame.mixer.music.play()


def create_db():
    db = sqlite3.connect("milky_data_base.db")
    c = db.cursor()
    c.execute("CREATE TABLE milk (litr text, date text, time time)")
    db.commit()
    db.close()


def save():   
    try:
        db = sqlite3.connect("milky_data_base.db")
        print("\nПодключение базы данных..")
        c = db.cursor()
        liters = mleco.get()
        if liters[:9] == "Сохранено":
            liters = liters.replace(liters[:9], "")
        
        c.execute(f"INSERT INTO milk VALUES ('{liters}', '{str(date)}', '{str(time)}')")
        print(f"Данные записаны:\n{liters} л.\n{str(date)}\n{str(time)}")

        db.commit()
        

        mleco.delete(0, END)
        mleco.insert(0, "Сохранено")
        pygame.mixer.music.load('click.mp3')
        pygame.mixer.music.play()

    except Exception:
        print("Не удается записать данные")    
        create_db()
        print("Создана новая база данных")    

        db = sqlite3.connect("milky_data_base.db")
        print("База данных подключена")
        c = db.cursor()
        c.execute(f"INSERT INTO milk VALUES ('{liters}', '{str(date)}', '{str(time)}')")
        print(f"Данные записаны:\n{liters} л.\n{str(date)}\n{str(time)}")

        db.commit()

    finally:
        db.close()
        print("Файл базы данных закрыт")

        
def clear():
    mleco.delete(0, END)
    pygame.mixer.music.load('click.mp3')
    pygame.mixer.music.play()


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


token = ""   
bot = telebot.TeleBot(token=token)


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Показать")
btn2 = types.KeyboardButton("Посчитать")
markup.add(btn1, btn2)  


@bot.message_handler(content_types=['text'])
def send_counted_milk(message):
    if message.text == 'Посчитать':
        try:
            db = sqlite3.connect("milky_data_base.db")
            c = db.cursor()
            c.execute(f"SELECT litr FROM milk")
            all_liters = c.fetchall()
            resault = 0
            for litr in all_liters:
                for num in litr:
                    print(num)
                    resault += float(num)
            bot.send_message(message.chat.id, f"Всего {resault} литров", reply_markup=markup)

        except:
            bot.send_message(message.chat.id, "Не удалось посчитать")        

        finally:
            db.close()

    
@bot.message_handler()
def send(message):
        
    try:       
        db = sqlite3.connect("milky_data_base.db")
        c = db.cursor()
        c.execute(f"SELECT * FROM milk")
        items = c.fetchall()
        information = ""
        for item in items:
            item = "  ".join(item)
            information = information + item + "\n"  
        bot.send_message(message.chat.id, information, reply_markup=markup)

    except:
        bot.send_message(message.chat.id, "не найдено")
        print("not found")

    finally:
        db.close()
      
bot.polling()

