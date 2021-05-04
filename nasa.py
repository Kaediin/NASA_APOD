import tkinter, requests, os, datetime, subprocess, time, pathlib, glob, os
import urllib.request as req
from PIL import Image, ImageTk


print('Sleeping 15 seconds')
time.sleep(15)

if os.environ.get('DISPLAY','') == '':
    print('No display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

lastImageRequestTime = ''
root = tkinter.Tk()
canvas = None
explanation_hidden = False
explanation_widget = None
api_key = 'qQSijXTvN8qN3i8tiYhIqi4BjZMeYbYiP7ZuZ9hZ'
# api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date=2021-02-16'
api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'

def button_1(event):
    global explanation_hidden
    if not explanation_hidden:
        canvas.itemconfigure(explanation_widget, state='hidden')
    else:
        canvas.itemconfigure(explanation_widget, state='normal')
    explanation_hidden = not explanation_hidden


def refresh_data():
    global root, lastImageRequestTime, canvas, explanation_widget

    today = datetime.datetime.now()
    hasImage = False
    try:
        response = requests.request('GET', api_url).json()
        try:
            hdurl = response['hdurl']
        except:
            if hasImage:
                append_log(f'{today}: Image already being displayed. No image found for next day. Continuing with previous image')
                raise Exception
            append_log(f'{today}: No image being displayed. No image for next day. Getting last image from folder')
            hdurl = None
        date = response['date']
        title = response['title']
        # explanation =  "This shadowy landscape of majestic mountains and icy plains stretches toward the horizon on a small, distant world. It was captured from a range of about 18,000 kilometers when New Horizons looked back toward Pluto, 15 minutes after the spacecraft's closest approach on July 14, 2015. The dramatic, low-angle, near-twilight scene follows rugged mountains formally known as Norgay Montes from foreground left, and Hillary Montes along the horizon, giving way to smooth Sputnik Planum at right. Layers of Pluto's tenuous atmosphere are also revealed in the backlit view. With a strangely familiar appearance, the frigid terrain likely includes ices of nitrogen and carbon monoxide with water-ice mountains rising up to 3,500 meters (11,000 feet). That's comparable in height to the majestic mountains of planet Earth. The Plutonian landscape is 380 kilometers (230 miles) across."
        explanation = response['explanation']

        if date != lastImageRequestTime:
            lastImageRequestTime = date
            img_path = f'{pathlib.Path(__file__).parent.absolute()}/images/{date}.jpg'

            append_log(f'\n\n{today}: Image path: {img_path}')

            append_log(f'{today}: Destroying Root')
            root.destroy()

            append_log(f'{today}: Checking if image already exists')
            if os.path.isfile(img_path):
                append_log(f'{today}: Image exists. Not downloading again')
                pilImage = Image.open(img_path)
                hasImage = True
            else:
                append_log(f'{today}: Image does not exist. Downloading from URL now')
                append_log(f'{today}: Retrieving img from URL')
                if hdurl is not None:
                    req.urlretrieve(hdurl, img_path)
                else:
                    append_log(f'{today}: Error loading next image. Loading previous one')
                    img_path = max(glob.glob(f'{pathlib.Path(__file__).parent.absolute()}/images/*'), key=os.path.getctime)
                    title = ''
                    explanation = f'No image found for {today.date()} :('

                append_log(f'{today}: Creating Pillow image')
                pilImage = Image.open(img_path)

            append_log(f'{today}: Creating New Root')
            root = tkinter.Tk()

            append_log(f'{today}: Creating TKinter Window')
            w, h = root.winfo_screenwidth(), root.winfo_screenheight()
            root.overrideredirect(1)
            root.geometry("%dx%d+0+0" % (w, h))
            root.focus_set()
            root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
            canvas = tkinter.Canvas(root, width=w, height=h)
            canvas.bind("<Button-1>", button_1)
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
            canvas.create_text(w, 0, anchor='ne', fill='white', font="Roboto 16 normal bold", text=title)
            explanation_widget = canvas.create_text(0, 0, anchor='nw', justify='left', fill='white', font="Roboto 11 normal bold",
                               width=w / 8, text=explanation)
            canvas.create_text(w, h, anchor='se', fill='white', font="Roboto 11 normal bold", text=date)
            canvas.configure(highlightthickness=0, borderwidth=0)

            if not hasImage:
                append_log(f'{today}: Calling root after in 24 hours')
                root.after((1000 * 60) * 1440, refresh_data)  # 3600000 milliseconds in an hour
            else:
                append_log(f'{today}: No API update. Refreshing later in 1 hour')
                root.after((1000 * 60) * 60, refresh_data)  # 3600000 milliseconds in an hour
            append_log(f'{today}: Running Mainloop')
            root.mainloop()
        else:
            append_log(f'{today}: No API update. Refreshing later in 1 hour')
            root.after((1000 * 60) * 60, refresh_data)  # 3600000 milliseconds in an hour

    except Exception as e:
        append_log(f'Error: {e}')

        # Retrying in 30mins
        root.after((1000 * 60) * 30, refresh_data)

def append_log(msg):
    print(msg)
    with open(f'{pathlib.Path(__file__).parent.absolute()}/log.txt', 'a') as file:
        file.write(f'{msg}\n')

refresh_data()
