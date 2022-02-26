import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Filters
from threading import Timer
import Database
import threading
from tenacity import retry, wait_fixed, stop_after_attempt

lock = threading.Lock()

TOKEN = '1002564110:AAFAxqzYElOAMFc0kHy4mAUUmiBQqbfLZUw'
## test : 1858625868:AAHxsfbOYTux-gSCWTDg2sDRWiTq8gmmykE
## main : 1002564110:AAFAxqzYElOAMFc0kHy4mAUUmiBQqbfLZUw

bot = telebot.TeleBot(token=TOKEN, num_threads=25)

tag_list = {}
chats = {}
tag_message = {}
blocked = {}
activedel = {}
accesstag = {}
panelholder = {}
reptgmsls = {}
isreplying = {}
reptext = {}
savejoinlink = {}
slp = {}
helpme = '''🔅به بخش راهنمای ربات ورولف تگر خوش آمدید🍻

🔅توضیحاتی برای این بات:

🔹این بات یوزر هایی را که در گپ شما پیام میدهند دریافت میکند و با استفاده از دستورات انها را تگ میکند ، این بات به صورت لحظه ایی لیست تگ خود را اپدیت میکند و جدید ترین و فعال ترین اعضا را را برای شما تگ خواهد کرد🔹

❗این بات قادر خواهد بود تا حتی آنهایی که بات را بلاک کرده اند را هم تگ کند❗

🔅دستورات بات به صورت زیر است :

/tag number number
❕شما باید در دو قسمت number عدد قرار دهید تا بات شروع به تگ کند🔸
❕بات برای شما در بازه ایی که خواسته اید شروع به تگ میکند🔸

/tagall
❕شما با این دستور تمام اعضا را تگ میکنید🔸

/replytag number
❗شما با استفاده از این دستور میتوانید حتی انهایی که بات را بلاک کرده اند را تگ کنید❗
❕شما باید در قسمت number یک عدد قرار دهید تا بات شروع به ریپلای زدن روی یوزر ها به مقدار دلخواهتان کند🔸
/stop
❕شما با این دستور میتوانید جلوی تگ کردن بات را بگیرید🔸

/set your text
❕شما میتوانید با نوشتن متن خود جلوی اين دستور متن ریپلای تگ را تغییر دهید🔸

🔅و اما در صورت اسپم دستورات توسط ممبر ها شما میتوانید از دستورات زیر برای محدود کردنشان استفاده کنید:

/blockuser
❕با ریپلای کردن این دستور روی شخص مورد نظر شما میتوانید شخص را از زدن کلیه دستور های بات محروم کنید🔸

/unblockuser
❕شما میتوانید با ریپلای کردن این دستور روی شخص مورد نظر تمام محدودیت ها را بردارید🔸

🔅و اما دستور جذاب این بات❗
/deltag
❕ با زدن این دستور بات تمام پیام های تگ خود را پاک میکند🔸

🔅پنل تنظیمات:
/tagger_setting
❕با زدن این دستور پنل تنظیمات برای شما باز خواهد شد و شما قادر به تنظیم موارد دلخواهتان هستید🔅

⚜پاک کردن خودکار : اگر این گزینه فعال باشد بات در هنگام شروع بازی تمام تگ های خود را پاک میکند در غیر اینصورت شما باید از دستور deltag استفاده کنید⚜

⚜دسترسی برای تگ : اگر این گزینه روی همه باشد یعنی‌ همه اعضای گروه میتوانند از دستورات تگ استفاده کنند در غیراینصورت فقط ادمین ها میتوانند از دستورات تگ‌استفاده کنند⚜

⚜تعداد تگ در هر پیام : با عوض کردن تعداد این بخش تعداد تگ های در هر پیام را میتوانید تغییر دهید⚜ 

❗توجه کنید درهنگام شروع بازی در صورت فعال بودن پاک کردن خودکار تگ ها به صورت خودکار پاک میشوند و نیازی به زدن 
/deltag 

نخواهد بود🔅

❗توجه کنید دستورات زیر :
deltag , blockuser , unblock user , stop
 را فقط ادمین ها میتوانند استفاده کنند 🔅

❗در صورت اسپم هرکدام از دستورات توسط ممبر ها شما میتوانید از دستورات مربوط به بلاک استفاده کنید🔅


❗این اموزش را به بقیه ادمین ها هم بدهید تا کار با ربات را بلد باشند🔅

Channel : @WereWolfTagger  '''


@bot.message_handler(func=Filters.private, commands=['start'])
def start(message):
    chat_id = message.from_user.id
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    try:
        bot.send_message(chat_id, '''به ربات ورولف تگر خوش آمدید🔥

❕برای خواندن راهنمایی ربات دستور زیر را ارسال کنید:
/help

❗برای خرید بات با ایدی زیر در تماس باشید :
@Ee_Alie 🔅

Channel : @WereWolfTagger 🔅 

developed by ✵αℓi αg''')
    except:
        pass


@bot.message_handler(commands=['active'], func=Filters.user([638994540, 1327834355, 835478580]))
def active_group(message):
    gp = message.text.split(" ")
    try:
        gp_id = gp[1]
    except IndexError:
        bot.reply_to(message, "لطفا آیدی عددی گروه را مقابل دستور قرار دهید")
        return
    try:
        if 8 < len(gp_id) < 16:
            gp_id = int(gp_id)
            result = Database.activegap(gp_id)
            bot.reply_to(message, result)
        else:
            bot.reply_to(message, 'this form : 10 < group id < 16')
            return
    except:
        bot.reply_to(message, 'لطفا ایدی عددی را درست وارد کنید❕')
        return


@bot.message_handler(commands=['list'], func=Filters.user([638994540, 1327834355, 835478580]))
def list(message):
    listgp = Database.getactivegaps()
    listgps = 'لیست گروه ها:'
    numgps = 0
    for i in listgp:
        try:
            gp = bot.get_chat(i).title
            listgps += f'\n{numgps}- `{gp}` - (`{i}`)'
            numgps += 1
        except:
            pass
        if numgps == 30:
            bot.send_message(message.chat.id, listgps, parse_mode='Markdown')
            time.sleep(2)
            listgps = 'لیست گروه ها:'
            numgps = 0
    bot.send_message(message.chat.id, listgps, parse_mode='Markdown')


@bot.message_handler(commands=['deactive'], func=Filters.user([638994540, 1327834355, 835478580]))
def diactive(message):
    whichgap = message.text.split(' ')
    try:
        whichgap = int(whichgap[1])
    except:
        bot.reply_to(message, 'آیدی عددی گروه را جلوی دستور قرار دهید❕')
        return
    result = Database.deactivegap(whichgap)
    bot.reply_to(message, result)
    try:
        tag_list.pop(whichgap)
    except:
        pass
    try:
        tag_message.pop(whichgap)
    except:
        pass
    try:
        blocked.pop(whichgap)
    except:
        pass
    try:
        activedel.pop(whichgap)
    except:
        pass
    try:
        accesstag.pop(whichgap)
    except:
        pass
    try:
        panelholder.pop(whichgap)
    except:
        pass
    try:
        reptgmsls.pop(whichgap)
    except:
        pass
    try:
        isreplying.pop(whichgap)
    except:
        pass
    try:
        reptext.pop(whichgap)
    except:
        pass
    try:
        chats.pop(whichgap)
    except:
        pass


@bot.message_handler(func=Filters.private, commands=['help'])
def send_help(message):
    chat_id = message.from_user.id
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    try:
        bot.send_message(chat_id, helpme)
    except:
        pass


@bot.message_handler(func=Filters.private)
def x(message):
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    bot.send_message(message.chat.id, '''⚜لطفا در پیوی ربات فقط از دستورات 
/help , /start
استفاده کنید⚜''', reply_markup=build_markup3())
    pass


@bot.message_handler(commands=['help'])
def send_h(message):
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    try:
        bot.send_message(message.from_user.id, helpme)
        bot.reply_to(message, '⚜آموزش ربات در پیوی شما فرستاده شد⚜')
    except:
        try:
            bot.reply_to(message, '⚜لطفا ابتدا پیوی ربات را استارت کنید و سپس مجددا از دستور استفاده کنید⚜')
        except:
            pass


def forcejoin_channel(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    status = bot.get_chat_member(user_id=user_id, chat_id='@werewolftagger').status
    if status == 'member' or status == 'creator' or status == 'administrator':
        return True
    else:
        bot.send_message(chat_id, '''🔹برای استفاده از دستورات ربات لطفا ابتدا در چنل زیر عضو شوید🔹

🔹سپس دستور مورد نظر خود را ارسال کنید🔹''',
                         reply_to_message_id=message.message_id, reply_markup=build_markup3())
        return False


def add_accesstag(chat_id):
    global accesstag
    if chat_id not in accesstag:
        accesstag.update({chat_id: True})


def add_slp(chat_id):
    global slp
    if chat_id not in slp:
        slp.update({chat_id: 1})


def add_activedel(chat_id):
    global activedel
    if chat_id not in activedel:
        activedel.update({chat_id: True})


def add_isreplying(chat_id):
    global isreplying
    if chat_id not in isreplying:
        isreplying.update({chat_id: False})


def add_reptext(chat_id):
    global reptext
    if chat_id not in reptext:
        reptext.update({chat_id: "🔆 JOIN 🔆"})


def add_blocked(chat_id):
    global blocked
    if chat_id not in blocked:
        blocked.update({chat_id: []})


def add_tag_message(chat_id):
    global tag_message
    if chat_id not in tag_message:
        tag_message.update({chat_id: []})


def add_chats(chat_id):
    global chats
    if chat_id not in chats:
        chats.update({chat_id: False})


def add_tag_list(chat_id):
    global tag_list
    if chat_id not in tag_list:
        try:
            lock.acquire(True)
            if Database.isactive(chat_id):
                tag_list.update({chat_id: []})
            else:
                try:
                    bot.send_message(chat_id, '''⤶اشتراک ربات شما تمام و ربات تا چند ثانیه دیگر لفت خواهد...🤖

⎠برای تمدید خرید دوباره اشتراک و تسویه حساب خود با ایدی「 @GreatAg 」در ارتباط باشید...🗯⎛''', reply_markup=build_markup3())
                    time.sleep(5)
                    bot.leave_chat(chat_id)
                except:
                    bot.leave_chat(chat_id)
                    pass
                return False
        finally:
            lock.release()
    return 1


def add_reptgmsls(chat_id):
    global reptgmsls
    if chat_id not in reptgmsls:
        reptgmsls[chat_id] = []


def check_admin(user_id, chat_id, message):
    if user_id != 638994540:
        status_id = bot.get_chat_member(chat_id, user_id).status
        if status_id != 'administrator' and status_id != 'creator':
            try:
                bot.reply_to(message, '🔹برای استفاده از این دستور باید ادمین گروه باشید🔹')
                return False
            except:
                return False
        else:
            return True
    else:
        return 1


@bot.message_handler(commands=['tag'])
def tagger(message):
    user = message.from_user
    user_id = user.id
    chat_id = message.chat.id
    tf = add_tag_list(chat_id)
    if not tf:
        return


#     global tag_message
#     global chats
#     msg = ''
#     user = message.from_user
#     user_id = user.id
#     chat_id = message.chat.id
#     list_s = message.text.split(" ")
#     add_accesstag(chat_id)
#     add_activedel(chat_id)
#     add_isreplying(chat_id)
#     if not accesstag[chat_id]:
#         ch = check_admin(user_id, chat_id, message)
#         if ch:
#             pass
#         elif not ch:
#             return
#         elif ch == 1:
#             pass
#     add_chats(chat_id)
#     if chat_id in blocked:
#         if user_id in blocked[chat_id]:
#             return
#     isjoin = forcejoin_channel(message)
#     if not isjoin:
#         return
#     try:
#         num = int(list_s[1])
#         num2 = int(list_s[2])
#     except:
#         try:
#             bot.reply_to(message, '''❗لطفا دستور را در فرمت درست وارد کنید❗
# 🔸/tag number number
# 🔸Example : /tag 0 100 ''')
#             return
#         except:
#             return
#     bet = num2 - num
#     if bet != 100:
#         bot.reply_to(message, '''❗اعداد را در بازه های صد تایی وارد کنید❗
# 🔸/tag number number
# 🔸Example : /tag 0 100''')
#         return
#     add_tag_message(chat_id)
#     if not chats[chat_id]:
#         chats[chat_id] = True
#         tf = add_tag_list(chat_id)
#         if not tf:
#             return
#         tgtemp = tag_list[chat_id].copy()
#         bot.send_message(chat_id=638994540, text=f'tag : {len(tgtemp)} : {bot.get_chat(chat_id).title}')
#         if num > len(tgtemp):
#             try:
#                 bot.reply_to(message, '❗یوزری در این بازه ثبت نشده است❗')
#             except:
#                 pass
#             chats[chat_id] = False
#             return
#         tgtemp.reverse()
#         i = num
#         a = 0
#         while num <= i < num2:
#             try:
#                 if not chats[chat_id]:
#                     return
#                 x = bot.get_chat_member(chat_id=message.chat.id, user_id=tgtemp[i])
#                 if not x.user.first_name:
#                     i = i + 1
#                     continue
#                 msg = msg + f'\n[{x.user.first_name}](tg://user?id={x.user.id})'
#                 a += 1
#                 if a == 5:
#                     tag = bot.send_message(chat_id=message.chat.id, text=msg,
#                                            parse_mode='Markdown')
#                     msg = ''
#                     a = 0
#                     try:
#                         tag_message[chat_id].append(tag.message_id)
#                     except:
#                         pass
#                     time.sleep(1)
#                 i = i + 1
#             except:
#                 i = i + 1
#                 pass
#         if msg:
#             tag = bot.send_message(chat_id=message.chat.id, text=msg,
#                                    parse_mode='Markdown')
#             msg = ''
#             try:
#                 tag_message[chat_id].append(tag.message_id)
#             except:
#                 pass
#         chats[chat_id] = False
#         tgtemp.clear()
#     elif chats[chat_id]:
#         try:
#             bot.reply_to(message, "دادا دارم تگ میکنم دیگه❕")
#         except:
#             pass


@bot.message_handler(commands=['stop'])
def stop_tag(message):
    global isreplying
    user_id = message.from_user.id
    chat_id = message.chat.id
    # add_chats(chat_id)
    add_isreplying(chat_id)
    if chat_id in blocked:
        if user_id in blocked[chat_id]:
            return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    ch = check_admin(user_id, chat_id, message)
    if ch:
        pass
    elif not ch:
        return
    elif ch == 1:
        pass
    if isreplying[chat_id]:
        isreplying[chat_id] = False
        try:
            bot.reply_to(message, "STOPPED🔴")
        except:
            pass
    elif not isreplying[chat_id]:
        try:
            bot.reply_to(message, "تگ نمیکنم که دادا❕")
        except:
            pass


@bot.message_handler(commands=['tagall'])
def tag_all(message):
    user = message.from_user
    user_id = user.id
    chat_id = message.chat.id
    tf = add_tag_list(chat_id)
    if not tf:
        return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    bot.reply_to(message, '''امکان استفاده از این دستور فعلا وجود ندارد لطفا از دستور
/replytag , /tag
برای تگ کردن استفاده کنید''')


@bot.message_handler(commands=['deltag'])
def del_tag(message):
    global tag_message
    user_id = message.from_user.id
    chat_id = message.chat.id
    add_tag_message(chat_id)
    if chat_id in blocked:
        if user_id in blocked[chat_id]:
            return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return

    ch = check_admin(user_id, chat_id, message)
    if ch:
        pass
    elif not ch:
        return
    elif ch == 1:
        pass

    if not tag_message[chat_id]:
        try:
            bot.reply_to(message, '🔹منشنی در گپ شما از طرف ربات تشخیص داده نشد🔹')
            return
        except:
            pass
    try:
        for i in tag_message[chat_id]:
            try:
                bot.delete_message(chat_id, i)
            except:
                pass
        tag_message[chat_id].clear()
        try:
            bot.send_message(chat_id, '🔹تمامی تگ های ربات پاک شد🔹', reply_markup=build_markup3())
        except:
            pass
    except:
        pass


@bot.message_handler(regexp='#next', func=Filters.user([1056178279, 957813599, 1048618677, 941773249, 638994540]))
def del_tags(message):
    global tag_message
    chat_id = message.chat.id
    add_activedel(chat_id)
    if not activedel[chat_id]:
        return
    add_tag_message(chat_id)
    if not tag_message[chat_id]:
        return
    for i in tag_message[chat_id]:
        try:
            bot.delete_message(chat_id, i)
        except:
            pass
    tag_message[chat_id].clear()
    try:
        bot.send_message(chat_id, '🔹تمامی تگ های ربات پاک شد🔹', reply_markup=build_markup3())
    except:
        pass


def build_markup3():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('⚜Tagger channel⚜', url='t.me/WereWolfTagger'))
    return markup


@bot.message_handler(commands=['blockuser'])
def block_user(message):
    global blocked
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not message.reply_to_message:
        try:
            bot.reply_to(message, "لطفا دستور را روی شخص مورد نظر ریپلای کنید❕")
            return
        except:
            return
    status_repid = bot.get_chat_member(chat_id, message.reply_to_message.from_user.id).status
    tf = add_tag_list(chat_id)
    if not tf:
        return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    if message.reply_to_message.from_user.id == user_id:
        return
    ch = check_admin(user_id, chat_id, message)
    if ch:
        pass
    elif not ch:
        return
    elif ch == 1:
        pass
    if status_repid == 'administrator' or status_repid == 'creator':
        try:
            bot.reply_to(message, 'شما نمیتوانید ادمین را محدود کنید❕')
            return
        except:
            return
    add_blocked(chat_id)
    if message.reply_to_message.from_user.id in blocked[chat_id]:
        try:
            bot.reply_to(message, "یوزر از قبل بلاک است❕")
            return
        except:
            return
    blocked[chat_id].append(message.reply_to_message.from_user.id)
    try:
        bot.reply_to(message, "BLOKED🔴")
    except:
        pass


@bot.message_handler(commands=['unblockuser'])
def unblock_user(message):
    global blocked
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not message.reply_to_message:
        try:
            bot.reply_to(message, "لطفا دستور را روی شخص مورد نظر ریپلای کنید❕")
            return
        except:
            return
    status_repid = bot.get_chat_member(chat_id, message.reply_to_message.from_user.id).status
    tf = add_tag_list(chat_id)
    if not tf:
        return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    if message.reply_to_message.from_user.id == user_id:
        return
    ch = check_admin(user_id, chat_id, message)
    if ch:
        pass
    elif not ch:
        return
    elif ch == 1:
        pass
    if status_repid == 'administrator' or status_repid == 'creator':
        try:
            bot.reply_to(message, 'شما نمیتوانید ادمین را محدود کنید❕')
            return
        except:
            return
    add_blocked(chat_id)
    if message.reply_to_message.from_user.id not in blocked[chat_id]:
        return
    blocked[chat_id].remove(message.reply_to_message.from_user.id)
    try:
        bot.reply_to(message, 'UNBLOKED🟢')
    except:
        pass


@bot.message_handler(commands=['leave'])
def leave(message):
    chat_id = message.chat.id
    user_id = 638994540
    if message.from_user.id == user_id:
        try:
            bot.leave_chat(chat_id)
        except:
            pass


def build_markup(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if activedel[chat_id]:
        msg = 'فعال✅'
    else:
        msg = 'غیرفعال❌'
    if accesstag[chat_id]:
        msg1 = '🔹همه🔹'
    else:
        msg1 = '🔹فقط ادمین ها🔹'
    speed = slp[chat_id]
    markup.add(InlineKeyboardButton(msg, callback_data='TOF'),
               InlineKeyboardButton('🔅پاک کردن خودکار🔅', callback_data='del'))
    markup.add(InlineKeyboardButton(msg1, callback_data='access'),
               InlineKeyboardButton('🔅دسترسی برای تگ🔅', callback_data='accesspart'))
    markup.add(InlineKeyboardButton('سرعت ریپلای', callback_data='speed'))
    markup.add(InlineKeyboardButton(speed, callback_data='number'))
    markup.add(InlineKeyboardButton('🔺', callback_data='upspeed'),
               InlineKeyboardButton('🔻', callback_data='downspeed'))
    markup.add(InlineKeyboardButton('⚜Tagger channel⚜', url='t.me/WereWolfTagger'))
    markup.add(InlineKeyboardButton('⚜بستن تنظیمات⚜', callback_data='close'))
    return markup


def build_markup2():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('⚜Tagger channel⚜', url='t.me/WereWolfTagger'))
    markup.add(InlineKeyboardButton('@Ee_Alie', url='t.me/ee_alie'))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global accesstag
    global activetag
    global panelholder
    global slp
    chat_id = call.message.chat.id
    try:
        if call.from_user.id == panelholder[call.message.message_id]:
            if call.data == 'TOF':
                if activedel[chat_id]:
                    activedel[chat_id] = False
                    try:
                        bot.answer_callback_query(call.id, '❕پاک کردن خودکار غیرفعال شد❕')
                    except:
                        pass
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                              text='🔆به بخش تنظیمات ربات ورولف تگر خوشامدید🔆',
                                              reply_markup=build_markup(chat_id))
                    except:
                        pass
                elif not activedel[chat_id]:
                    activedel[chat_id] = True
                    try:
                        bot.answer_callback_query(call.id, '❕پاک کردن خودکار فعال شد❕')
                    except:
                        pass

                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                              text='🔆به بخش تنظیمات ربات ورولف تگر خوشامدید🔆',
                                              reply_markup=build_markup(chat_id))
                    except:
                        pass
            if call.data == 'del':
                try:
                    bot.answer_callback_query(call.id, '⚜لطفا انتخاب کنید⚜')
                except:
                    pass
            if call.data == 'speed' or call.data == 'number':
                try:
                    bot.answer_callback_query(call.id, '⚜لطفا با استفاده از دکمه ها انتخاب کنید⚜')
                except:
                    pass
            if call.data == 'upspeed':
                if slp[chat_id] == 10:
                    bot.answer_callback_query(call.id,'بیشتر از 10 نمیتواند باشد')
                else:
                    slp[chat_id] += 1
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                              text='🔆به بخش تنظیمات ربات ورولف تگر خوشامدید🔆',
                                              reply_markup=build_markup(chat_id))
                    except:
                        pass
            if call.data == 'downspeed':
                if slp[chat_id] == 0:
                    bot.answer_callback_query(call.id,'کمتر از یک نمیتواند باشد')
                else:
                    slp[chat_id] -= 1
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                              text='🔆به بخش تنظیمات ربات ورولف تگر خوشامدید🔆',
                                              reply_markup=build_markup(chat_id))
                    except:
                        pass
            if call.data == 'access':
                if accesstag[chat_id]:
                    accesstag[chat_id] = False
                    try:
                        bot.answer_callback_query(call.id, '❕دسترسی تگ فقط برای ادمین ها فعال شد❕')
                    except:
                        pass
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                              text='🔆به بخش تنظیمات ربات ورولف تگر خوشامدید🔆',
                                              reply_markup=build_markup(chat_id))
                    except:
                        pass
                elif not accesstag[chat_id]:
                    accesstag[chat_id] = True
                    try:
                        bot.answer_callback_query(call.id, '❕دسترسی تگ برای همه فعال شد❕')
                    except:
                        pass
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                              text='🔆به بخش تنظیمات ربات ورولف تگر خوشامدید🔆',
                                              reply_markup=build_markup(chat_id))
                    except:
                        pass
            if call.data == 'accesspart':
                try:
                    bot.answer_callback_query(call.id, '⚜لطفا انتخاب کنید⚜')
                except:
                    pass
            if call.data == 'close':
                try:
                    bot.answer_callback_query(call.id, 'تنظیمات ثبت شد✅')
                except:
                    pass
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                          text='''تنظیمات شما ثبت شد✅

⚜در صورت انتقاد ، پیشنهاد ، ایراد میتوانید با ایدی زیر در تماس باشید⚜

⚜برای اطلاع از اخرین آپدیت ها و اخبار ربات در چنل زیر عضو باشید⚜''',
                                          reply_markup=build_markup2())
                except:
                    pass
        else:
            try:
                bot.answer_callback_query(call.id, '❗پنل توسط شخص دیگری باز شده است❗')
            except:
                pass
    except KeyError:
        try:
            bot.answer_callback_query(call.id, '❗پنل منقضی شده است❗')
        except:
            pass


@bot.message_handler(commands=['tagger_setting'])
def setting(message):
    global panelholder
    user_id = message.from_user.id
    chat_id = message.chat.id
    tf = add_tag_list(chat_id)
    if not tf:
        return
    if chat_id in blocked:
        if user_id in blocked[chat_id]:
            return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    ch = check_admin(user_id, chat_id, message)
    if ch:
        pass
    elif not ch:
        return
    elif ch == 1:
        pass
    add_activedel(chat_id)
    add_accesstag(chat_id)
    add_slp(chat_id)
    try:
        panel = bot.send_message(chat_id, "🔆به بخش تنظیمات ربات ورولف تگر خوشامدید🔆", reply_markup=build_markup(chat_id))
        panelholder[panel.message_id] = user_id

        def expirer():
            global panelholder
            del panelholder[panel.message_id]

        t = Timer(180, expirer)
        t.start()
    except:
        pass


def build_markup4(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('🔥JOIN GAME🔥', url=savejoinlink[chat_id]))
    return markup


@bot.message_handler(commands=['replytag'])
def main(message):
    global isreplying
    global tag_message
    global reptgmsls
    global slp
    text = message.text
    user = message.from_user
    user_id = user.id
    chat_id = message.chat.id
    add_reptext(chat_id)
    add_tag_message(chat_id)
    # add_chats(chat_id)
    add_accesstag(chat_id)
    add_isreplying(chat_id)
    add_reptgmsls(chat_id)
    add_slp(chat_id)
    if chat_id in blocked:
        if user_id in blocked[chat_id]:
            return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    if not accesstag[chat_id]:
        ch = check_admin(user_id, chat_id, message)
        if ch:
            pass
        elif not ch:
            return
        elif ch == 1:
            pass
    tedad = text.split(" ")
    try:
        tedad = tedad[1]
    except IndexError:
        try:
            bot.reply_to(message, '''❗لطفا دستور را در فرمت درست وارد کنید❗
🔸/replytag number 
🔸Example : /replytag 10''')
            return
        except:
            return
    try:
        tedad = int(tedad)
    except:
        try:
            bot.reply_to(message, '''❗لطفا دستور را در فرمت درست وارد کنید❗
🔸/replytag number 
🔸Example : /replytag 10''')
            return
        except:
            return
    if tedad < 0:
        try:
            bot.reply_to(message, '❗لطفا عدد را درست وارد کنید❗')
            return
        except:
            return
    if tedad > 500:
        try:
            bot.reply_to(message, '❗لطفا عدد ورودی زیر 500 باشد❗')
            return
        except:
            return
    tagged = 0
    if not isreplying[chat_id]:
        isreplying[chat_id] = True
        tf = add_tag_list(chat_id)
        if not tf:
            return
        reptemp = reptgmsls[chat_id].copy()
        bot.send_message(chat_id=638994540, text=f'replytag : {len(reptemp)} : {bot.get_chat(chat_id).title}')
        reptemp.reverse()
        for rep in reptemp:
            if not isreplying[chat_id]:
                return
            elif tagged != tedad:
                try:
                    tag = bot.send_message(chat_id, reptext[chat_id], reply_to_message_id=rep.message_id)
                    try:
                        tag_message[chat_id].append(tag.message_id)
                    except:
                        pass
                    tagged += 1
                    time.sleep(slp[chat_id])
                except:
                    pass
        isreplying[chat_id] = False
        reptemp.clear()
    else:
        try:
            bot.reply_to(message, '❕دادا دارم ریپلای میکنم دیگه❕')
        except:
            pass


@bot.message_handler(commands=['set'])
def set_text(message):
    global reptext
    chat_id = message.chat.id
    user_id = message.from_user.id
    add_reptext(chat_id)
    tf = add_tag_list(chat_id)
    if not tf:
        return
    isjoin = forcejoin_channel(message)
    if not isjoin:
        return
    ch = check_admin(user_id, chat_id, message)
    if ch:
        pass
    elif not ch:
        return
    elif ch == 1:
        pass
    input = message.text.split(" ")
    str = " ".join(input[1:])
    if str == '':
        try:
            bot.reply_to(message, '❕لطفا مقابل دستور متن موردنظر خود را وارد كنيد❕')
        except:
            pass
        return
    reptext[chat_id] = str
    bot.send_message(chat_id, '🔆متن ریپلای با موفیقت تغییر کرد🔆', reply_markup=build_markup3())


@bot.message_handler(content_types=['text', 'photo', 'sticker', 'video'])
def get_id(message):
    global reptgmsls
    global tag_list
    chat_id = message.chat.id
    user = message.from_user
    user_id = user.id
    add_reptgmsls(chat_id)
    inhere = 0
    tf = add_tag_list(chat_id)
    if not tf:
        return
    if user_id == 951153044 or user_id == 660462150:
        return
    if len(reptgmsls[chat_id]) != 0:
        for i in reptgmsls[chat_id]:
            if i.from_user.id == message.from_user.id:
                try:
                    reptgmsls[chat_id].remove(i)
                except:
                    pass
                reptgmsls[chat_id].append(message)
            else:
                inhere += 1
    if inhere == len(reptgmsls[chat_id]):
        reptgmsls[chat_id].append(message)

    # if user_id in tag_list[chat_id]:
    #     tag_list[chat_id].remove(user_id)
    #     tag_list[chat_id].append(user_id)
    #     return
    # tag_list[chat_id].append(user_id)


bot.send_message(chat_id=638994540, text='tagger is up')


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def poll():
    if __name__ == "__main__":
        try:
            bot.polling(none_stop=True, timeout=234)
        except Exception as e:
            bot.send_message(chat_id=638994540, text=e)
            raise e


poll()

while True:
    pass
