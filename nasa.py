import tkinter
import requests
import urllib.request as req
from PIL import Image, ImageTk

lastImageRequestTime = ''
root = tkinter.Tk()
api_key = 'qQSijXTvN8qN3i8tiYhIqi4BjZMeYbYiP7ZuZ9hZ'
api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'


def refresh_data():
    global root, lastImageRequestTime
    response = requests.request('GET', api_url).json()
    hdurl = response['hdurl']
    date = response['date']

    if date != lastImageRequestTime:
        lastImageRequestTime = date

        print('Destroying Root')
        root.destroy()

        print('Downloading URL')
        req.urlretrieve(hdurl, f"images/{date}.jpg")
        pilImage = Image.open(f'images/{date}.jpg')

        print('Creating New Root')
        root = tkinter.Tk()

        print('Creating TKinter Window')
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        root.focus_set()
        root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        canvas = tkinter.Canvas(root, width=w, height=h)
        canvas.pack()
        canvas.configure(background='black')
        imgWidth, imgHeight = pilImage.size
        if imgWidth > w or imgHeight > h:
            ratio = min(w / imgWidth, h / imgHeight)
            imgWidth = int(imgWidth * ratio)
            imgHeight = int(imgHeight * ratio)
            pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = canvas.create_image(w / 2, h / 2, image=image)

        print('Calling root after in 2 hours')
        root.after((1000 * 60) * 120, refresh_data) #3600000 milliseconds in an hour
        print('Running Mainloop')
        root.mainloop()
    else:
        print('No API update. Refreshing later in 2 hours')
        root.after((1000 * 60) * 120, refresh_data) #3600000 milliseconds in an hour


refresh_data()
