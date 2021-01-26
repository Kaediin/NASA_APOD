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
    today = datetime.datetime.now()
    hasImage = False
    try:
        response = requests.request('GET', api_url).json()
        hdurl = response['hdurl']
        date = response['date']
        title = response['title']
        # explanation =  "This shadowy landscape of majestic mountains and icy plains stretches toward the horizon on a small, distant world. It was captured from a range of about 18,000 kilometers when New Horizons looked back toward Pluto, 15 minutes after the spacecraft's closest approach on July 14, 2015. The dramatic, low-angle, near-twilight scene follows rugged mountains formally known as Norgay Montes from foreground left, and Hillary Montes along the horizon, giving way to smooth Sputnik Planum at right. Layers of Pluto's tenuous atmosphere are also revealed in the backlit view. With a strangely familiar appearance, the frigid terrain likely includes ices of nitrogen and carbon monoxide with water-ice mountains rising up to 3,500 meters (11,000 feet). That's comparable in height to the majestic mountains of planet Earth. The Plutonian landscape is 380 kilometers (230 miles) across."
        explanation = response['explanation']

        if date != lastImageRequestTime:
            lastImageRequestTime = date

            print(f'{today}: Destroying Root')
            root.destroy()

            print(f'{today}: Checking if image already exists')
            if os.path.isfile(f'images/{date}.jpg'):
                print(f'{today}: Image exists. Not downloading again')
                pilImage = Image.open(f'images/{date}.jpg')
                hasImage = True
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
            canvas.create_text(w / 2, 40, fill='white', font="Roboto 20 normal bold", text=title)
            canvas.create_text(0, 0, anchor='nw', justify='left', fill='white', font="Roboto 11 normal bold",
                               width=w / 8, text=explanation)
            canvas.create_text(w, h, anchor='se', fill='white', font="Roboto 11 normal bold", text=date)
            canvas.configure(highlightthickness=0, borderwidth=0)

            if not hasImage:
                print(f'{today}: Calling root after in 24 hours')
                root.after((1000 * 60) * 1440, refresh_data)  # 3600000 milliseconds in an hour
            else:
                print(f'{today}: No API update. Refreshing later in 1 hour')
                root.after((1000 * 60) * 60, refresh_data)  # 3600000 milliseconds in an hour
            print(f'{today}: Running Mainloop')
            root.mainloop()
        else:
            print(f'{today}: No API update. Refreshing later in 1 hour')
            root.after((1000 * 60) * 60, refresh_data)  # 3600000 milliseconds in an hour

    except Exception as e:
        print(f'Error: {e}')

        # Retrying in 30mins
        root.after((1000 * 60) * 30, refresh_data)



# TODO: Add touch controls
refresh_data()
