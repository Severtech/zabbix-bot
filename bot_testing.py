import telebot
import mechanicalsoup
from pyzabbix import ZabbixAPI

# Создаем экземпляр бота
bot = telebot.TeleBot("2114371612:AAFlbZVrPByePucq0kXOcbCx2HNTHGyH9fA")
print("OK")


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False) :
    bot.send_message(m.chat.id, "Я на связи. Напиши мне что-нибудь )")


# Получение сообщений от юзера
# noinspection PyBroadException
@bot.message_handler(content_types=["text"])
def handle_text(message) :
    problemName = message.text
    problemName = problemName[problemName.find("Problem") + 9 :]
    problemName = problemName[: problemName.find("Problem") - 2]
    problemName = problemName.strip()
    print(problemName)
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://d.sever.tech:6018/index.php")
    browser.select_form('form[action="index.php"]')
    browser["name"] = "admin-zabbix"
    browser["password"] = "42FnWwFQWqmQPV3"
    zapi = ZabbixAPI("http://d.sever.tech:6018/")
    zabbix_login = "admin-zabbix"
    zabbix_password = "42FnWwFQWqmQPV3"
    zabbix_availability = True
    try :
        zapi.login(zabbix_login, zabbix_password)
        res1 = zapi.httptest.get(output="extend", selectTags="extend", hostids="10084")
        for i in res1 :
            if i["name"] == problemName :
                browser.open("http://d.sever.tech:6018/httpdetails.php?httptestid=" + str(i["httptestid"]))
                temp = browser.page.find_all("span")
                tempString = str(temp[0])
                tempString = tempString[tempString.find(">") + 1 : tempString.rfind("<")]
                print(tempString)
                bot.send_message(message.chat.id, tempString)

        zapi.user.logout()
    except :
        zabbix_availability = False


# Запускаем бота
bot.polling(none_stop=True, interval=0)
