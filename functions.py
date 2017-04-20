from PIL import Image
import shutil,cv2,os

# references :
#
# https://www.daniweb.com/programming/software-development/code/485063/hide-private-message-in-an-image-python
# http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
# http://tsaith.github.io/combine-images-into-a-video-with-python-3-and-opencv-3.html

# Fauzanil Zaki , 2017

def frame_extract(video):
    temp_folder = 'temp'
    try:
        os.mkdir(temp_folder)
    except OSError:
        remove(temp_folder)
        os.mkdir(temp_folder)

    vidcap = cv2.VideoCapture("data/"+str(video))
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))



def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))




def caesar_ascii(char,mode,n):
    if mode == "enc" :
        ascii = ord(char)
        return chr((ascii + n) % 128)
    elif mode == "dec" :
        ascii = ord(char)
        return chr((ascii - n) % 128)


def encode_frame(frame_dir,text_to_hide,caesarn):



    # open the text file

    text_to_hide_open = open(text_to_hide, "r")
    text_to_hide = repr(text_to_hide_open.read())

    # split text to max 255 char each

    text_to_hide_chopped =  split2len(text_to_hide,255)

    for text in text_to_hide_chopped:
        length = len(text)
        chopped_text_index = text_to_hide_chopped.index(text)
        frame = Image.open(str(frame_dir) +"/" + str(chopped_text_index+1) + ".png")

        if frame.mode != "RGB":
            print("Source frame must be in RGB format")
            return False

        # use copy of the file

        encoded = frame.copy()
        width, height = frame.size

        index = 0
        a = object
        for row in range(height):
            for col in range(width):
                r,g,b = frame.getpixel((col,row))

                # first value is length of the message per frame
                if row == 0 and col == 0 and index < length:
                    asc = length
                    if text_to_hide_chopped.index(text) == 0 :
                        total_encoded_frame = len(text_to_hide_chopped)
                    else:
                        total_encoded_frame = g
                elif index <= length:
                    c = text[index -1]
                    # put the encypted character into ascii value
                    asc = ord(caesar_ascii(c,"enc",caesarn))
                    total_encoded_frame = g
                else:
                    asc = r
                    total_encoded_frame = g
                encoded.putpixel((col,row),(asc,total_encoded_frame,b))
                index += 1
        if encoded:
            encoded.save(str(frame_dir)+"/"+str(chopped_text_index+1) + ".png",compress_level=0)

def decode_frame(frame_dir,caesarn):

    #take the first frame to get width, height, and total encoded frame

    # first_frame = Image.open(str(frame_dir) + "/0.jpg")
    first_frame = Image.open(str(frame_dir)+ "/" + "1.png")
    r,g,b = first_frame.getpixel((0,0))
    total_encoded_frame = g
    msg = ""
    for i in range (1,total_encoded_frame+1):
        frame = Image.open(str(frame_dir) + "/" + str(i) + ".png")
        width, height = frame.size
        index = 0
        for row in range(height):
            for col in range(width):
                try :
                    r,g,b = frame.getpixel((col,row))
                except ValueError:

                    # for some ong a(transparancy) is needed
                    r, g, b, a = frame.getpixel((col, row))
                if row == 0 and col == 0:
                    length = r
                elif index <= length:
                    # put the decrypted character into string
                    msg += caesar_ascii(chr(r),"dec",caesarn)
                index +=1
    #remove the first and the last quote
    msg = msg[1:-1]
    recovered_txt = open("data/recovered-text.txt", "w")
    recovered_txt.write(str(msg.decode('string_escape')))



