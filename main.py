from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import re
import os
import os.path

#Создание папки для файлов пользователей здесь будут распологаться txt файлы каждого
#зарегестрированного пользователся
#Если папки users нету, то она сделается
papka = os.path.exists("users")
if papka == False:
    os.mkdir("users")

#тут идет подгрузка всех форм
Form, Window = uic.loadUiType("KaN.ui")
Form2, Window2 = uic.loadUiType("shif.ui")
Form3, Window3 = uic.loadUiType("vih.ui")


app = QApplication([])

window = Window()
form = Form()
form.setupUi(window)
window.show()

#здесь и в 3 форме .show не пишем, потому что нам пока не надо их показывать 
window2 = Window2()
form2 = Form2()
form2.setupUi(window2)


window3 = Window3()
form3 = Form3()
form3.setupUi(window3)

#Тут дополнительно прописываю текст для 2 формы, потому что знак \ в QT не хочет выводиться
form2.label_9.setText('*если вы хотите использовать его, то введите users\<Ваше_Имя>.txt>')
#Скрываю лишние подсказки
form.label_4.setVisible(False)
form.label_5.setVisible(False)
form.label.setVisible(False)
form.label_6.setVisible(False)
form.label_7.setVisible(False)


#Регистрация
def rreg():
    #Скрываю лишнее
    form.label_7.setVisible(False)
    form.label_6.setVisible(False)
    #Использование только букв и цифр в имени
    bukvi = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    #62 это кол-во символов которые можно использовать
    bukvi_kol = 62
    #задаю значения имени и паролю
    name = form.textEdit.toPlainText()
    parl = form.textEdit_2.toPlainText()
    #тут делаю так, чтобы в имени можно было использовать буквы и цифры
    namei = len(name)
    a = 0
    for i in range(len(bukvi)):
        for j in range(len(name)):
            if bukvi[i] != name[j]:
                a += 1
    if ((bukvi_kol * namei) - a) == namei:
        a = 0
    else:
        a = 1
        form.label_6.setVisible(True)
        form.label_4.setVisible(False)
    #Длина имени и пароля от 4 до 16 символов
    if (len(name) < 4) or (len(name) > 16):
        form.label_4.setVisible(True)
    if (len(name) > 3) and (len(name) < 15):
        form.label_4.setVisible(False)
    if (len(parl) < 4) or (len(parl) > 16):
        form.label_5.setVisible(True)
    if (len(parl) > 3) and (len(parl) < 15):
        form.label_5.setVisible(False)
    if (len(name) > 3) and (len(name) < 15) and (len(parl) > 3) and (len(parl) < 15) and (a == 0):
        form.label_6.setVisible(False)
        #запись данных в файл пользовотелей, тут будет имя пользователя и зашифрованный пароль
        file = open('dan.txt', 'r+', -1, 'utf-8')
        #тут проверяю мб пользователь с таким именем уже есть
        nas = 0
        for line in file:
            if re.search(name, line):
                form.label.setVisible(True)
                nas = 1
        #тут вписываются данные пользователся
        if nas == 0:
            file.write('\n')
            file.write(name)
            file.write(' : ')
            file.write(sha1(parl))
        file.close()
        #создание личного файла пользователя, тут будет его текст
        user = r"users\Q.txt"
        user = user.replace('Q', name)
        my_file = open(user, "w")
        my_file.close()
        #открытие личного кабинета
        form2.label_3.setText('шифр') #на всякий случай вписываю начальные значения
        form2.label_7.setText('шифр из файла')
        form2.textEdit.setText('')
        form2.textEdit_2.setText('')
        #скрываю лишнее
        form2.label_2.setVisible(False)
        form2.label_3.setVisible(False)
        form2.label_7.setVisible(False)
        form2.label_8.setVisible(False)
        #показываю 2 форму
        window2.show()
        #и скрываю первую
        window.hide()
 #активация кнопки регистрации
form.pushButton_2.clicked.connect(rreg)

def avt():
    #Авторизация
    form.label_4.setVisible(False) #опять скрываю лишнее
    form.label_5.setVisible(False)
    form.label.setVisible(False)
    form.label_6.setVisible(False)
    form.label_7.setVisible(False)
    name = form.textEdit.toPlainText() #тут опять задаю переменным имя и пароль
    parl = form.textEdit_2.toPlainText()
    #Проверка регистрации пользователя
    namei = len(name)
    po = 0
    file = open('dan.txt', 'r+', -1, 'utf-8') #тут проверка либо неверное имя либо пароль либо вообще не зарегистрирован
    for line in file:
        if re.search(name, line): #если нашел имя, то проверяю пароль
            lini = line
            lini = lini.replace(name, '')
            lini = lini.replace(' : ', '')
            lini = lini.replace('\n', '')
            l = sha1(parl)
            if lini == l: #тут если пароль верный
                window2.show() #открываю 2 форму
                window.hide() #скрываю первую
                po = 1
                form.label_7.setVisible(False) #коректирую и убераю лишнее
                form2.label_3.setText('шифр')
                form2.label_7.setText('шифр из файла')
                form2.textEdit.setText('')
                form2.textEdit_2.setText('')
                form2.label_2.setVisible(False)
                form2.label_3.setVisible(False)
                form2.label_7.setVisible(False)
                form2.label_8.setVisible(False)
            else:
                form.label_7.setVisible(True)
                po = po + 0
        elif po == 0: #опа пароль не совпал ты не зайдешь хехе)
            form.label_7.setVisible(True)
     #тут проверяю длинну имя и пароля
    if (len(name) < 4) or (len(name) > 16):
        form.label_4.setVisible(True)
        form.label_7.setVisible(False)
    if (len(name) > 3) and (len(name) < 15):
        form.label_4.setVisible(False)
    if (len(parl) < 4) or (len(parl) > 16):
        form.label_5.setVisible(True)
        form.label_7.setVisible(False)
    if (len(parl) > 3) and (len(parl) < 15):
        form.label_5.setVisible(False)
        #а тут проверяю использованные символы в имени
    bukvi = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    bukvi_kol = 62
    a = 0
    for i in range(len(bukvi)):
        for j in range(len(name)):
            if bukvi[i] != name[j]:
                a += 1
    if ((bukvi_kol * namei) - a) == namei:
        a = 0
    else:
        a = 1
        form.label_6.setVisible(True)
        form.label_4.setVisible(False)
form.pushButton.clicked.connect(avt)

#выход отмена на главную это в 3 форме
#выход
def quit():
    app.quit()

#отмена
def otm():
    window3.hide()
    window2.show()

#на главную
def glav():
    window3.hide()
    form.textEdit.setText('')
    form.textEdit_2.setText('')
    window.show()


#тут для кнопки назад 
def naz():
    window2.hide()
    window3.show()
    form3.pushButton_2.clicked.connect(quit)
    form3.pushButton_3.clicked.connect(otm)
    form3.pushButton.clicked.connect(glav)
form2.pushButton.clicked.connect(naz)

def shif_text():
    #шифрование текста в 2 форме
    text = form2.textEdit.toPlainText() #это текст ввели
    text_1 = sha1(text) #тут его зашифровали
    form2.label_3.setText('') #опять коррекция
    form2.label_2.setVisible(True)
    form2.label_3.setVisible(True)
    form2.label_3.setText(text_1)
    #тут создается личный документ для пользователся
    name = form.textEdit.toPlainText()
    user = r"users\Q.txt"
    user = user.replace('Q', name) #здесь Q заменяется на имя, чтобы файл бы ИМЯ_ПОЛЬЗОВАЛЯ.txt
    file = open(user, 'a', -1, 'utf-8')
    file.write('\n')
    file.write(text)
    file.write(' : ')
    file.write(text_1)
    file.close()
form2.pushButton_2.clicked.connect(shif_text)

def ras_text():
    #расшифровка
    # шифра из файла
    form2.label_7.setVisible(False) #коррекцияяяяяяяяяяяяяяяяя)
    form2.label_8.setVisible(False)
    text = form2.textEdit.toPlainText() #тут задается шифр который нужно будет найти в файле и расшифровать
    #тут проверяем есть ли вообще файл, если ты сделал свой
    file_s = form2.textEdit_2.toPlainText()
    s_file = os.path.exists(file_s) 
    a = 0
    if s_file == True and len(text) == 40: #если нашел файл и длина шифра равна 40 символам в SHA1 эт всегда так
        file = open(file_s, 'r', -1, 'utf-8')
        for line in file: #ищу строку в файле где есть нужный шифр
            if re.search(text, line): #тут если нашел молодец)
                form2.label_7.setVisible(True)
                form2.label_8.setVisible(True)
                lize = line #очищаю нужную строку, чтобы осталось только расшифровка
                lize = lize.replace(text, '')
                lize = lize.replace(' : ', '')
                lize = lize.replace('\n', '')
                form2.label_7.setText(lize)
                a = 1
            elif a == 0: #ну тут не нашел, сам виноват, не зашифровал
                form2.label_7.setVisible(True)
                form2.label_7.setText('Расшифровка не найдена')
    elif file_s == '': #это если в пути к файлу ничего не написал. Вот поленился теперь работать не будет
        form2.label_7.setVisible(False)
        form2.label_8.setVisible(False)
    elif len(text) != 40: #тут если шифр не 40 символов в SHA1 такое не бывает, не обманывай программу она работать не будет
        form2.label_7.setVisible(False)
        form2.label_8.setVisible(False)
    else: #ну иначе файл не найден, нечего свой пихать, я для тебя и так создал
        form2.label_7.setVisible(True)
        form2.label_7.setText('Файл не найден')
form2.pushButton_3.clicked.connect(ras_text)

def sha1(data):
    #код шифрования SHA1
    bytes = ""

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for n in range(len(data)):
        bytes+='{0:08b}'.format(ord(data[n]))
    bits = bytes+"1"
    pBits = bits

    while len(pBits)%512 != 448:
        pBits+="0"

    pBits+='{0:064b}'.format(len(bits)-1)

    def chunks(l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]

    def rol(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    for c in chunks(pBits, 512):
        words = chunks(c, 32)
        w = [0]*80
        for n in range(0, 16):
            w[n] = int(words[n], 2)
        for i in range(16, 80):
            w[i] = rol((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = rol(a, 5) + f + e + k + w[i] & 0xffffffff
            e = d
            d = c
            c = rol(b, 30)
            b = a
            a = temp

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

app.exec()
