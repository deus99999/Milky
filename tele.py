import telebot
from telebot import types # для указание типов
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from datetime import date
from datetime import datetime
from tkinter import * 
import json
import time
import pygame.mixer
import sqlite3

from config import token

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
    c.execute("CREATE TABLE milk (litr text, date text, time time, price text)")
    db.commit()
    db.close()

def get_price(price=20):
    return price

def save():   
    try:
        db = sqlite3.connect("milky_data_base.db")
        print("\nПодключение базы данных..")
        c = db.cursor()
        liters = mleco.get()
        if liters[:9] == "Сохранено":
            liters = liters.replace(liters[:9], "")
        
        c.execute(f"INSERT INTO milk VALUES ('{liters}', '{str(date)}', '{str(time)}', '{str(get_price())}')")
        print(f"Данные записаны:\n{liters} л.\n{str(date)}\n{str(time)}\n{str(get_price())}")

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
        c.execute(f"INSERT INTO milk VALUES ('{liters}', '{str(date)}', '{str(time)}', '{get_price()}')")
        print(f"Данные записаны:\n{liters} л.\n{str(date)}\n{str(time)}\n{get_price()}")

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


bot = telebot.TeleBot(token=token)


markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Показать")
btn2 = types.KeyboardButton("Посчитать")
btn3 = types.KeyboardButton("Ввести стоимость за литр")

markup.add(btn1, btn2)
markup.add(btn3)


keyboard = InlineKeyboardMarkup()
keyboard.add(InlineKeyboardButton(text=f"Умножить на {get_price()} грн", callback_data="value"))


@bot.message_handler(content_types=['text'])
def buttons_menu(message):
    if message.text == 'Показать':
        try:
            db = sqlite3.connect("milky_data_base.db")
            c = db.cursor()
            c.execute(f"SELECT * FROM milk")
            items = c.fetchall()

            information = ""

            for item in items:
                item = "  | ".join(item)
                information = information + item + "грн" + "\n"                  
            bot.send_message(message.chat.id, information, reply_markup=markup)

        except:
            bot.send_message(message.chat.id, "Не удалось вывести базу данных")        

        finally:
            db.close()
            
    if message.text == 'Посчитать':
        try:
            db = sqlite3.connect("milky_data_base.db")
            c = db.cursor()
            c.execute(f"SELECT litr FROM milk")
            all_liters = c.fetchall()
            resault = 0
            for litr in all_liters:
                for num in litr:
                    resault += float(num)
            bot.send_message(message.chat.id, f"Всего {resault} литров", reply_markup=keyboard)
            
            @bot.callback_query_handler(func=lambda c: c.data == 'value') 

            def process_callback_button1(callback_query: types.CallbackQuery):
                try:
                    milk_value = resault * get_price()
                    bot.answer_callback_query(callback_query.id)                           
                    bot.send_message(callback_query.from_user.id, f"{resault} л x {get_price()} грн = {milk_value} грн")
                except:
                    bot.send_message(callback_query.from_user.id, "Не удалось высчитать стоимость.")
        except:
            bot.send_message(message.chat.id, "Не удалось посчитать")        

        finally:
            db.close()

    if message.text == "Ввести стоимость за литр":
        bot.send_message(message.chat.id, "Введите новую цену за один литр молока:")
        




    
      
bot.polling()

