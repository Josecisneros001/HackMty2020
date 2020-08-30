from tkinter import *
from colors import *
from bot import *

root = Tk()
root.title('Zoomer')
root.iconbitmap()
root.geometry("230x1000")
root.config(bg=black)

def getParticipants(driver):
      countParticipants(driver)

def getHands(driver):
      countHands(driver)
      
#join meeting and show functions
def go():

    clipboard = root.clipboard_get()
    # start driver
    driver = start_driver()
    # get goal link to access via web
    lastUrl = getUrl(clipboard)
    # join meeting
    joinMeeting(driver,lastUrl)

    start_frame.pack(fill="both", expand=1)
    title1 = Label(start_frame, text='Zoomer', fg=blue,
                   bg=black, font=('Lato', 23, 'bold'))
    title1.place(relx=0.5, rely=0.1, anchor=CENTER)

    info = Label(start_frame, height=2, text="ID:\n" +
                 id, fg=grey, bg=black, font=('Lato', 12))
    info.place(relx=0.5, rely=0.2, anchor=CENTER)

    button = Button(start_frame, text='Get Participants',
                    command=getParticipants(driver), font=('Lato', 12), bg=blue, fg=platinum)
    button.place(relx=0.5, rely=0.4, anchor=CENTER)

    button = Button(start_frame, text='Count Hands',
                    command=getHands(driver), font=('Lato', 12), bg=blue, fg=platinum)
    button.place(relx=0.5, rely=0.5, anchor=CENTER)

    button = Button(start_frame, text='Exit', command=exit,
                    font=('Lato', 12), bg=orange, fg=platinum)
    button.place(relx=0.5, rely=0.83, anchor=CENTER)

           
# main
title = Label(text='Zoomer', fg=blue, bg=black, font=('Lato', 23, 'bold'))
title.place(relx=0.5, rely=0.1, anchor=CENTER)


info = Label(height=3, text='Copy the meeting link \n in your clipboard \n and hit go!',
             fg=grey, bg=black, font=('Lato', 12))
info.place(relx=0.5, rely=0.3, anchor=CENTER)

button = Button(text='Go!', command=go, font=(
    'Lato', 16), bg=blue, fg=platinum)
button.place(relx=0.5, rely=0.5, anchor=CENTER)

# create start frame
start_frame = Frame(root, width=230, height=1000, bg=black)


root.mainloop()
