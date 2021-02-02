#Get Youtube html
import urllib.request
from urllib.request import Request, urlopen
import lxml.html as LH

#Find all youtube IDs
import re
import requests
#Download and convert YT video
import youtube_dl
import time
#Get last song downloaded / delete last song/video
import shutil
import glob
import os
import sys
#Telegram Bot
import telebot
from telegram.ext import Updater
from telegram.ext import CommandHandler
#Get user settings
import json
#Insert song details
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
import numpy as np


# Telegram bot start
# Get the token in "token.json"
token = json.loads(open("token.json").read())
# Load bot with token
bot = telebot.TeleBot(token['token'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Benvenuto nel bot! Controlla /help per tutti i comandi a tua disposizione.\nInserisci il nome o l'url del video da scaricare:")

#Help commands

@bot.message_handler(commands=['help'])
def helpcommand(message):
	bot.reply_to(message, "/mp3 : I prossimi file verranno scaricati in formato mp3\n/mp4 : I prossimi file verranno scaricati in formato mp4")


@bot.message_handler(commands=['mp4'])
def mp4setting(message):
<<<<<<< Updated upstream
    def WritetoJSONFile(path, filename, data):
        filePathNameWExt = './' + filename
        with open(filePathNameWExt, 'w') as fp:
           json.dump(data, fp)

    filename = 'users.json'
    userid = message.chat.id;

    data = {}
    data['setting'] = 'mp4'
    data['userid'] = userid

    WritetoJSONFile('./',filename, data)
=======

    userid = message.chat.id

    data = {}
    def user():
        global data
        a = 0
        while a<5:
            data[userid] = {'format': 'mp4'}
            with open('users.json', 'w') as json_file:
                json.dump(data, json_file)
            a+=1
    user()
>>>>>>> Stashed changes

    bot.reply_to(message, "I prossimi file verranno scaricati in formato mp4!")
    print("Added 1 user preference to users.json: " + str(data))

@bot.message_handler(commands=['mp3'])
def mp3setting(message):

    def WritetoJSONFile(path, filename, data):
        filePathNameWExt = './' + filename
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp)

    filename = 'users.json'
    userid = message.chat.id;
<<<<<<< Updated upstream

    data = {}
    data['setting'] = 'mp3'
    data['userid'] = userid
=======
    usersdata = json.loads(filename)

    data = data[userid].append({
    'format': 'mp3'
    })

>>>>>>> Stashed changes

    WritetoJSONFile('./',filename, data)

    bot.reply_to(message, "I prossimi file verranno scaricati in formato mp3!")
    print("Added 1 user preference to users.json")

#Download video/audio
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    originalmessage = message.text
    #Replace spaces with -
    inputelement = originalmessage.replace(" ", "-")

    directlink = inputelement.startswith("https://")


    if directlink == True:
        if inputelement.startswith("https://music.youtube.com"):
            string = '&list='+ inputelement.split('&list=')[-1]
            # Link without music list
            ytmlink = inputelement[:-len(string)]
            inputelement.rsplit("&list=", 1)[0]

        #Print loading
        bot.reply_to(message, '⚙️Download del video:\n' + inputelement + ' ...(30%)')

        #Get user preferences
        #Get user ID
        iduser = message.chat.id;
        #Open JSON file
        data = json.loads(open("users.json").read())

        if data["userid"] == iduser:
            if data["setting"] == "mp3":
                ydl_opts = {
                'format':"bestaudio/best",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': "mp3",
                        'preferredquality': '192',
                    }],
                }
            else:
                ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio/best'
                }
        else:
            ydl_opts = {
                'format':"bestaudio/best",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': "mp3",
                        'preferredquality': '192',
                    }],
                }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #Download the video
            ydl.download([inputelement])
            meta = ydl.extract_info(inputelement)
            #Get file title
            file_title = meta['title']
            #Get file author
            file_author = meta['uploader']
            bot.reply_to(message, 'Conversione e upload del video... (70%)')

        if data["userid"] == iduser:
            if data["setting"] == "mp3":
                mp3_file = glob.glob("*.mp3")  #consider only files with .mp3 extension
                newest_file = max(mp3_file, key=os.path.getctime)  #get the last file
                os.rename(r"" + newest_file ,r"" + file_title + '.mp3') #Rename the file with real music title
                #Insert audio metadata
                audio = EasyID3(file_title + ".mp3")
                audio['artist'] = file_author
                audio.save()
                audio = open(file_title + '.mp3', 'rb')
                bot.send_audio(message.chat.id, audio)
            else:
                # Consider only files with .mp3 extension
                mp4_file = glob.glob("*.mp4")
                # Get the last mp4 file
                newest_file = max(mp4_file, key=os.path.getctime)
                # Get the title of file
                file_title = os.path.splitext(newest_file)[0]
                # Open & send .mp4 file
                video = open(file_title + '.mp4', 'rb')
                bot.send_video(message.chat.id, video)

        #Delete last song / video downloaded
        if data["setting"] == "mp3":
            audio.close()
            os.remove(file_title + '.mp3')
        else:
            video.close()
            os.remove(file_title + '.mp4')

        print("Last file: " + file_title + " Deleted!")

    if directlink == False:
        #Get html page of youtube
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + inputelement)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        #Find video link
        complete_link = "https://www.youtube.com/watch?v=" + video_ids[0]   #Get the complete YT link

        bot.reply_to(message, '⚙️Download del video:\n' + complete_link)

        # Print loading message
        loadingmessage = bot.reply_to(message, '⚙️Download del video...')
        messageid = loadingmessage.message_id
        #Get user preferences
        #Get user ID
        iduser = message.chat.id
        #Open JSON file
        data = json.loads(open("users.json").read())

        if data["userid"] == iduser:
            if data["setting"] == "mp3":
                ydl_opts = {
                'format':"bestaudio/best",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': "mp3",
                        'preferredquality': '192',
                    }],
                }
            else:
                ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio/best'
                }
        else:
            ydl_opts = {
                'format':"bestaudio/best",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': "mp3",
                        'preferredquality': '192',
                    }],
                }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #Download the video
            ydl.download([complete_link])
            meta = ydl.extract_info(complete_link)
            #Get file title
            file_title = meta['title']
            #Get file author
            file_author = meta['uploader']
            bot.edit_message_text("⚙️Conversione e upload del video... (70%)",iduser, messageid)

        if data["userid"] == iduser:
            if data["setting"] == "mp3":
                mp3_file = glob.glob("*.mp3")  #consider only files with .mp3 extension
                newest_file = max(mp3_file, key=os.path.getctime)  #get the last file
                try:
                    os.rename(r"" + newest_file ,r"" + file_title + '.mp3') #Rename the file with real music title
                    #Insert audio metadata
                    audio = EasyID3(file_title + ".mp3")
                    audio['artist'] = file_author
                    audio['title'] = file_title
                    audio.save()
                    audio = open(file_title + '.mp3', 'rb')
                    bot.send_audio(message.chat.id, audio)

                except:
                    print("Rename failed, sending original filename")
                    #Insert audio metadata
                    audio = EasyID3(file_title + ".mp3")
                    audio['artist'] = file_author
                    audio.save()
                    audio = open(newest_file + '.mp3', 'rb')
                    bot.send_audio(message.chat.id, audio)
            else:
                # Consider only files with .mp4 extension
                mp4_file = glob.glob("*.mp4")
                # Get the last mp4 file
                newest_file = max(mp4_file, key=os.path.getctime)
                # Get the title of file
                file_title = os.path.splitext(newest_file)[0]
                # Open & send .mp4 file
                video = open(file_title + '.mp4', 'rb')
                bot.send_video(message.chat.id, video)

        #Delete last song / video downloaded
        if data["setting"] == "mp3":
            audio.close()
            os.remove(file_title + '.mp3')
        else:
            video.close()
            os.remove(file_title + '.mp4')

        print("Last file: " + file_title + " Deleted!\n")


print("Bot Online!\nListening...")
bot.polling()



