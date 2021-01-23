import tkinter, requests, os, datetime, subprocess
import urllib.request as req
from PIL import Image, ImageTk

lastImageRequestTime = ''
root = tkinter.Tk()
api_key = 'qQSijXTvN8qN3i8tiYhIqi4BjZMeYbYiP7ZuZ9hZ'
api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'

def git_add(file_path):
    return subprocess.check_output(['git', 'add', file_path])

def git_commit(message):
    return subprocess.check_output(['git', 'commit',  '-m', message])

def git_push():
    return subprocess.check_output(['git', 'push', 'origin', 'master'])


def refresh_data():
    global root, lastImageRequestTime
    response = requests.request('GET', api_url).json()
    hdurl = response['hdurl']
    date = response['date']
    today = datetime.datetime.now()

    if date != lastImageRequestTime:
        lastImageRequestTime = date

        print(f'{today}: Destroying Root')
        root.destroy()

        print(f'{today}: Checking if image already exists')
        if os.path.isfile(f'images/{date}.jpg'):
            print(f'{today}: Image exists. Not downloading again')
            pilImage = Image.open(f'images/{date}.jpg')
        else:
            print(f'{today}: Image does not exist. Downloading from URL now')
            req.urlretrieve(hdurl, f"images/{date}.jpg")
            pilImage = Image.open(f'images/{date}.jpg')

            try:
                print(f'{today}: Adding new file to git')
                git_add('images')
                print(f'{today}: Committing new file to git')
                git_commit(f'{today}: adding new file')
                print(f'{today}: Pushing new file to git')
                git_push()
            except subprocess.CalledProcessError as e:
                print(f'{today}: ', e.output)

        print(f'{today}: Creating New Root')
        root = tkinter.Tk()

        print(f'{today}: Creating TKinter Window')
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

        print(f'{today}: Calling root after in 4 hours')
        root.after((1000 * 60) * 240, refresh_data) #3600000 milliseconds in an hour
        print(f'{today}: Running Mainloop')
        root.mainloop()
    else:
        print(f'{today}: No API update. Refreshing later in 4 hours')
        root.after((1000 * 60) * 240, refresh_data) #3600000 milliseconds in an hour


refresh_data()
