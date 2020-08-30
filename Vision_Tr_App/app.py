from tkinter import *
from colors import *
from bot import *
import multiprocessing as mp
import threading
from zoomtestlabel import * 
from audio_denoiser import main_audio_denoiser
import xlsxwriter


global loginWaitTime
loginWaitTime = 1.8

lista_de_participantes = []
def getParticipants():
    workbook = xlsxwriter.Workbook('Lista_De_Asistencia.xlsx')
    worksheet = workbook.add_worksheet()
    print("getParticipantes..")
    participants = take_attendance(driver)
    for i in range(len(participants)):
        lista_de_participantes.append(participants[i])
        print(participants[i])
    row = 0
    col = 0
    for persona in (lista_de_participantes):
        worksheet.write(row, col,persona)
        row += 1
    workbook.close()

def getEmotions():
    print('Get participants emotions...')
    mainzoomlabel("forframes.jpg","response.jpg",5)

def getHands():
    print("gethands")
    countHands(driver)


def exitF():
    print("exit")
    menu_frame.pack_forget()
    start_frame.pack()
    leaveMeeting(driver)

# join meeting and show functions


def go():
    clipboard = root.clipboard_get()
    # get goal link to access via web
    lastUrl = getUrl(clipboard)
    # join meeting
    joinMeeting(driver, lastUrl)
    menu_frame.pack()
    start_frame.pack_forget()


def initBot():
    global driver
    driver = start_driver()
    enterZoom(driver, loginWaitTime)
    print('Ready to GO!')


# main
def main():
    global root
    root = Tk()
    root.title('Zoomer')
    root.iconbitmap()
    root.geometry("230x1000")
    root.config(bg=black)

    # loading_menu
    global loading_frame
    loading_frame = Frame(root, width=230, height=1000, bg=black)
    title = Label(loading_frame, text='Edu+', fg=blue,
                  bg=black, font=('Montserrat', 23, 'bold'))
    title.place(relx=0.5, rely=0.1, anchor=CENTER)

    info = Label(loading_frame, height=3, text='Loading',
                 fg=grey, bg=black, font=('Montserrat', 12))
    info.place(relx=0.5, rely=0.3, anchor=CENTER)

    # start_menu
    global start_frame
    start_frame = Frame(root, width=230, height=1000, bg=black)
    title = Label(start_frame, text='Zoomer', fg=blue,
                  bg=black, font=('Montserrat', 23, 'bold'))
    title.place(relx=0.5, rely=0.1, anchor=CENTER)

    info = Label(start_frame, height=3, text='Copy the meeting link \n in your clipboard \n and hit go!',
                 fg=grey, bg=black, font=('Montserrat', 12))
    info.place(relx=0.5, rely=0.3, anchor=CENTER)

    button = Button(start_frame, text='Go!', command=go, font=(
        'Montserrat', 16), bg=blue, fg=platinum,relief=SUNKEN)
    button.place(relx=0.5, rely=0.5, anchor=CENTER)

    start_frame.pack()

    # create menu frame
    global menu_frame
    menu_frame = Frame(root, width=350, height=1000, bg=black)

    title = Label(menu_frame, text='Zoomer', fg=blue,
                  bg=black, font=('Montserrat', 23, 'bold'))
    title.place(relx=0.5, rely=0.1, anchor=CENTER)

    info = Label(menu_frame, height=2, text="Welcome",
                 fg=grey, bg=black, font=('Montserrat', 12))
    info.place(relx=0.5, rely=0.2, anchor=CENTER)

    button = Button(menu_frame, text='Get Participants',
                    command=getParticipants, font=('Montserrat', 12), bg=blue, fg=platinum)
    button.place(relx=0.5, rely=0.4, anchor=CENTER)

    button = Button(menu_frame, text='Count Hands',
                    command=getHands, font=('Montserrat', 12), bg=blue, fg=platinum)
    button.place(relx=0.5, rely=0.5, anchor=CENTER)

    button =Button(menu_frame,text='Sense emotions',
                   command=getEmotions, font=('Montserrat', 12), bg=blue, fg=platinum)
    button.place(relx=0.5, rely=0.6, anchor=CENTER)

    button =Button(menu_frame,text='Noise Cancel',
                   command=main_audio_denoiser, font=('Montserrat', 12), bg=blue, fg=platinum)
    button.place(relx=0.5, rely=0.7, anchor=CENTER)

    button = Button(menu_frame, text='Exit', command=exitF,
                    font=('Montserrat', 12), bg=orange, fg=platinum)
    button.place(relx=0.5, rely=1.03, anchor=CENTER)

    root.mainloop()


if __name__ == '__main__':
    threading.Thread(target=initBot).start()
    main()
