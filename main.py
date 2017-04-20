from pyfiglet import Figlet
from functions import *
from subprocess import call,STDOUT
import os

# Fauzanil Zaki , 2017
# feel free to use

if __name__ == '__main__':

    # cool boi

    f = Figlet(font='slant')
    print(f.renderText("CCVS"))
    print("CaesarCipherVideoSteganography")
    print("")
    # print("By : ")
    # print("")
    # print("===Fauzanil Zaki===")
    # print("====Galih Dea P.===")
    # print("====Johan Eko P.===")
    # print("===Wiladhianty Y.==")
    # print("")

    print("Menu :")
    print("")
    print("(a) Encypt & Merge into Video")
    print("(b) Decrypt & Get the plain text")
    print("-----------------------")
    choice = raw_input("(!) Choose option : ")

    if choice == "a":
        # refresh terminal
        call(["clear"])

        print(f.renderText("Encrypt"))
        print("----------------------------------------")
        file_name = raw_input("(1) Video file name in the data folder  ? : ")

        try:
            caesarn = int(raw_input("(2) Caesar cypher n value  ? : "))
        except ValueError:
            print("-----------------------")
            print("(!) n is not an integer ")
            exit()

        try:
            open("data/" + file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        frame_extract(str(file_name))
        print("(-) Extracting audio")
        # using system call
        #ffmpeg -i data/chef.mp4 -q:a 0 -map a temp/audio.mp3 -y
        # 2>/dev/null for supressing the output from ffmpeg
        call(["ffmpeg", "-i", "data/" + str(file_name), "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        # useless
        print("(-) Reading text-to-hide.txt")
        print("(-) Encrypting & appending string into frame(s) ")
        encode_frame("temp", "data/text-to-hide.txt", caesarn)
        print("(-) Merging frame(s) ")
        #ffmpeg -i temp/%d.png -vcodec png data/enc-filename.mov
        call(["ffmpeg", "-i", "temp/%d.png" , "-vcodec", "png", "temp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        print("(-) Optimizing encode & Merging audio ")
        # ffmpeg -i temp/temp-video.avi -i temp/audio.mp3 -codec copy data/enc-chef.mp4 -y
        call(["ffmpeg", "-i", "temp/video.mov", "-i", "temp/audio.mp3", "-codec", "copy","data/enc-" + str(file_name)+".mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        print("(!) Success , output : enc-" + str(file_name)+".mov")

    elif choice == "b" :
        # refresh terminal
        call(["clear"])

        print(f.renderText("Decrypt"))
        print("----------------------------------------")
        file_name = raw_input("(1) Video file name in the data folder  ? : ")

        try:
            caesarn = int(raw_input("(2) Caesar cypher n value  ? : "))
        except ValueError:
            print("-----------------------")
            print("(!) n is not an integer ")
            exit()

        try:
            open("data/" + file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        frame_extract(str(file_name))
        print("(-) Decrypting Frame(s)")
        decode_frame("temp",caesarn)
        #useless
        print("(-) Writing to recovered-text.txt")
        print("(!) Success")


    else:
        exit()

