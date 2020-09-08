from mydewsbotslib.linepy import *
from mydewsbotslib.akad.ttypes import *
from multiprocessing import Pool, Process
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.request, urllib.parse, urllib.error, urllib.parse,subprocess,unicodedata, timeit, atexit, traceback
_session = requests.session()
from gtts import gTTS
from firebase import firebase

firebase = firebase.FirebaseApplication("firebase", None)

line = LINE("@com","password")
print ("login success")

lineMID = line.profile.mid
lineProfile = line.getProfile()
lineSettings = line.getSettings()

oepoll = OEPoll(line)

Rfu = [line]
Exc = [line]
lineMID = line.getProfile().mid

RfuProtect = {
    "autoAdd": {},
    "protect": {},
    "cancelprotect": {},
    "inviteprotect": {},
    "linkprotect": {},
    "Protectjoin": {},
    "Wc": {}
}

def sendMessageWithMention(to, lineMID):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(lineMID)+'}'
        text_ = '@x '
        line.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)

def logError(text):
    line.log("[ แจ้งเตือน ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))

def myhelp():
    myHelp = """>คำสั่งทั่วไป<
เช็ค =[เช็คว่าเราเปิดคำสั่งอะไรอยู่]
คำสั่ง  =[คำสั่งทัวไป]
คำสั่ง1 =[โหมดบอทป้องกันกลุ่ม]
คำสั่ง2 =[โหมดในกลุ่ม]"""
    return myHelp

def listgrup():
    listGrup = """>โหมดในกลุ่ม<
ยัดดำ @ =[แบนไม่ให้เข้ากลุ่ม]
บัญชีดำ =[เช็คบัญชีดำ]
ล้างดำ =[ล้างบช.ดำ]"""
    return listGrup

def helpset():
    helpSet = """>โหมดป้องกันกลุ่ม<
>คำสั่งเปิดป้องกันทั้งหมด<
เปิดระบบป้องกัน/ปิดระบบป้องกัน
เปิดป้องกันลิ้ง/ปิดป้องกันลิ้ง          
เปิดกันเข้า/ปิดกันเข้า
เปิดกันเชิญ/ปิดกันเชิญ

>ตั้งต้อนรับเปิดปิด<
ข้อความต้อนรับ: ข้อความ
เปิดข้อความ 
ปิดข้อความ"""
    return helpSet

def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            RfuProtect = firebase.get("/setting",'')
            if RfuProtect["autoAdd"] == True:
                line.blockContact(op.param1)
        if op.type in [25,26]:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != line.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
            if msg.contentType == 0:
                RfuProtect = firebase.get("/setting",'')
                if text is None:
                    return
                elif msg.text in ["เช็ค"]:
                    try:
                        ret_ = "สถานะที่เปิดอยู่"
                        if RfuProtect["autoAdd"] == True: ret_ += "\nออโต้บล็อค✔"
                        else: ret_ += "\nออโต้บล็อค ✘ "
                        if RfuProtect["Wc"] == True: ret_ += "\nเปิดข้อความต้อนรับสมาชิก ✔"
                        else: ret_ += "\nเปิดข้อความต้อนรับสมาชิก    ✘ " 
                        if RfuProtect["inviteprotect"] == True: ret_ += "\nป้องกันเชิญเข้ากลุ่ม ✔"
                        else: ret_ += "\nป้องกันเชิญเข้ากลุ่ม ✘ "
                        if RfuProtect["cancelprotect"] == True: ret_ += "\nป้องกันยกเลิกค้างเชิญ ✔"
                        else: ret_ += "\nป้องกันยกเลิกค้างเชิญ ✘ "
                        if RfuProtect["protect"] == True: ret_ += "\nป้องกันลบสมาชิก ✔"
                        else: ret_ += "\nป้องกันลบสมาชิก ✘ "
                        if RfuProtect["linkprotect"] == True: ret_ += "\nป้องกันเปิดลิ้ง ✔"
                        else: ret_ += "\nป้องกันเปิดลิ้ง ✘ "
                        if RfuProtect["Protectjoin"] == True: ret_ += "\nป้องกันเข้ากลุ่ม ✔"
                        else: ret_ += "\nป้องกันเข้ากลุ่ม ✘ "
                        line.sendMessage(to, str(ret_))
                        sendMessageWithMention(to, lineMID)
                        line.sendMessage(to, "" +datetime.today().strftime('%H:%M:%S')) 
                    except Exception as e:
                        line.sendMessage(msg.to, str(e))
                elif msg.text in ["คำสั่ง","help"]:
                    myHelp = myhelp()
                    line.sendMessage(to, str(myHelp))
                    sendMessageWithMention(to, lineMID)
                    line.sendMessage(to, "" +datetime.today().strftime('%H:%M:%S')+ "") 
                elif msg.text in ["คำสั่ง1","help1"]:
                    helpSet = helpset()
                    line.sendMessage(to, str(helpSet))
                    sendMessageWithMention(to, lineMID)
                    line.sendMessage(to, "" +datetime.today().strftime('%H:%M:%S')+ "") 
                elif msg.text in ["คำสั่ง2","help2"]:
                    listGrup = listgrup()
                    line.sendMessage(to, str(listGrup))
                    sendMessageWithMention(to, lineMID)
                    line.sendMessage(to, "" +datetime.today().strftime('%H:%M:%S')+ "") 
                elif msg.text.lower().startswith("ไอดี "):
                    if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        line.sendMessage(msg.to, str(ret_))
                elif msg.text.lower() == "เปิดระบบป้องกัน":
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["protect"] = True
                    RfuProtect["cancelprotect"] = True
                    RfuProtect["inviteprotect"] = True
                    RfuProtect["linkprotect"] = True
                    RfuProtect["Protectjoin"] = True
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(to,"_เปิดระบบป้องกันทั้งหมด\n" +datetime.today().strftime('%H:%M:%S'))
                elif msg.text in ["ปิดระบบป้องกัน"]:
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["protect"] = False
                    RfuProtect["cancelprotect"] = False
                    RfuProtect["inviteprotect"] = False
                    RfuProtect["linkprotect"] = False
                    RfuProtect["Protectjoin"] = False
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(to,"_ปิดระบบป้องกันทั้งหมด\n" +datetime.today().strftime('%H:%M:%S'))
                
                elif msg.text.lower() in ['เปิดป้องกันลิ้ง','เปิดป้องกันลิงค์']:
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["linkprotect"] = True
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_เปิดป้องกันลิ้งแล้ว")

                elif msg.text.lower() in ['ปิดป้องกันลิ้ง','ปิดป้องกันลิงค์']:
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["linkprotect"] = False
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_ปิดป้องกันลิ้งแล้ว") 

                elif msg.text.lower() == 'เปิดกันเข้า':
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["Protectjoin"] = True
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_เปิดกันเข้ากลุ่ม")

                elif msg.text.lower() == 'ปิดกันเข้า':
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["Protectjoin"] = False
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_ปิดกันเข้ากลุ่ม")

                elif msg.text.lower() == 'เปิดกันเชิญ':
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["inviteprotect"] = True
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_เปิดป้องกันเชิญเข้ากลุ่ม")

                elif msg.text.lower() == 'ปิดกันเชิญ':
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["inviteprotect"] = False
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_ปิดป้องกันเชิญเข้ากลุ่ม")

                elif msg.text.lower() == 'เปิดกันยกเลิกเชิญ':
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["cancelprotect"] = True
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_เปิดป้องกันยกเลิกเชิญ")

                elif msg.text.lower() == 'ปิดกันยกเลิกเชิญ':
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["cancelprotect"] = True
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(msg.to,"_เปิดป้องกันยกเลิกเชิญ")

                elif msg.text in ["เปิดข้อความ"]:
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["Wc"] = True
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(to,"_เปิดข้อความตอนรับ")

                elif msg.text in ["ปิดข้อความ"]:
                    RfuProtect = firebase.get("/setting",'')
                    RfuProtect["Wc"] = False
                    result = firebase.put('',"/setting",RfuProtect)
                    line.sendMessage(to,"_ปิดข้อความตอนรับ")

                elif msg.text in ["ล้างดำ"]:
                    try:
                        result = firebase.delete("/banlist",'')
                        datapass = { 'id' : 'dummy'}
                        result = firebase.post("/banlist",datapass)
                    except:
                        pass
                    line.sendMessage(msg.to,"_ล้างบัญชีดำเรียบร้อย")
                    print ("Clear Ban")
                elif msg.text in ["เช็คดำ","บัญชีดำ"]:
                    result = firebase.get("/banlist",'')
                    banlist = {'id': {}}
                    try:
                        for data in result:
                            banlist["id"][result[data]["id"]] = True
                    except:
                        pass
                    if banlist["id"] == {}:
                        line.sendMessage(msg.to,"ไม่มีลิสในบัญชีดำ")
                    else:
                        line.sendMessage(msg.to,"รายชื่อบัญชีดำ " +datetime.today().strftime('%H:%M:%S'))
                        mc = "<Blacklist>\n" 
                        for mi_d in banlist["id"]:
                              mc += "[" + line.getContact(mi_d).displayName + "] \n"
                        line.sendMessage(msg.to, mc + "") 
                elif 'ยัดดำ' in text.lower():
                       targets = []
                       key = eval(msg.contentMetadata["MENTION"])
                       key["MENTIONEES"] [0] ["M"]
                       for x in key["MENTIONEES"]:
                           targets.append(x["M"])
                       for target in targets:
                           try:
                               datapass = {
                                   'id' : str(target)
                               }
                               result = firebase.post("/banlist",datapass)
                               line.sendMessage(msg.to,"ยัดดำเรียบร้อยแล้ว")
                               print ("Banned User")
                           except:
                               line.sendMessage(msg.to,"ไม่สามารถยัดดำได้")           
        
        if op.type == 19:           
            adminlist = {'id':{}}

            result = firebase.get("/adminlist",'')
            for data in result:
                adminlist["id"][result[data]["id"]] = True
            if op.param3 in adminlist["id"]:
                random.choice(Rfu).inviteIntoGroup(op.param1,[op.param3])
                print("adminkick")              
            if op.param2 in adminlist["id"]:
                pass
            elif RfuProtect["protect"] == True:
                datapost = {
                    'id': str(op.param2)
                }
                result = firebase.post("/banlist",datapost)
                random.choice(Rfu).kickoutFromGroup(op.param1,[op.param2])
                random.choice(Rfu).inviteIntoGroup(op.param1,[op.param3])
        if op.type == 11:
            adminlist = {'id':{}}

            result = firebase.get("/adminlist",'')
            for data in result:
                adminlist["id"][result[data]["id"]] = True
            if RfuProtect["linkprotect"] == True:
                if op.param2 in adminlist["id"]:
                    pass
                    print("admin open link")
                else:
                    datapost = {'id': str(op.param2)}
                    try:
                        result = firebase.post("/banlist",datapost)
                    except Exception as error:
                        logError(error)
                    G = line.getGroup(op.param1)
                    G.preventedJoinByTicket = True
                    random.choice(Rfu).updateGroup(G)
                    random.choice(Rfu).kickoutFromGroup(op.param1,[op.param2])
        if op.type == 17:
            RfuProtect = firebase.get("/setting",'')
            if RfuProtect["Wc"] == True:
                if op.param2 in lineMID:
                 return
            dan = line.getContact(op.param2)
            tgb = line.getGroup(op.param1)
            line.sendMessage(op.param1, "ยินดีต้อนรับ" + "\n"+"\n{}\n{}".format(str(dan.displayName),str(tgb.name)))
        if op.type == 13:
            adminlist = {'id':{}}
            result = firebase.get("/adminlist",'')
            for data in result:
                adminlist["id"][result[data]["id"]] = True
            if op.param2 in adminlist["id"]:
                group = line.getGroup(op.param1)
                line.acceptGroupInvitation(op.param1)
        if op.type == 17:
            adminlist = {'id':{}}

            result = firebase.get("/adminlist",'')
            for data in result:
                adminlist["id"][result[data]["id"]] = True
            if op.param2 in adminlist["id"]:
                pass
            if RfuProtect["protect"] == True:
                if settings["blacklist"][op.param2] == True:
                    try:
                        line.kickoutFromGroup(op.param1,[op.param2])
                        G = line.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        line.updateGroup(G)
                    except:
                        try:
                            line.kickoutFromGroup(op.param1,[op.param2])
                            G = line.getGroup(op.param1)
                            G.preventedJoinByTicket = True
                            line.updateGroup(G)
                        except:
                            pass      
            
    except Exception as error:
        logError(error)
def restartBot():
    print ("RESTART BOT")
    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
while True:
    try:
        ops = oepoll.singleTrace(count=5)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)