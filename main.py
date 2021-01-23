# import requests, time, tkinter
# import urllib.request as req
# from PIL import Image, ImageTk
#
# lastImageRequestTime = ''
# root = tkinter.Tk()
# api_key = 'qQSijXTvN8qN3i8tiYhIqi4BjZMeYbYiP7ZuZ9hZ'
# api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
# seconds_delay = 60
#
#
# def showPIL(pilImage):
#     w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#     root.overrideredirect(True)
#     root.geometry("%dx%d+0+0" % (w, h))
#     root.focus_set()
#     root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
#     canvas = tkinter.Canvas(root, width=w, height=h)
#     canvas.pack()
#     canvas.configure(background='black')
#     imgWidth, imgHeight = pilImage.size
#     if imgWidth > w or imgHeight > h:
#         ratio = min(w / imgWidth, h / imgHeight)
#         imgWidth = int(imgWidth * ratio)
#         imgHeight = int(imgHeight * ratio)
#         pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
#     image = ImageTk.PhotoImage(pilImage)
#     imagesprite = canvas.create_image(w / 2, h / 2, image=image)
#     root.mainloop()
#
#
# def get_date():
#     response = requests.request('GET', api_url).json()
#     return response['date']
#
#
# def get_hd_image_url(current_time):
#     global lastImageRequestTime
#     if current_time != lastImageRequestTime:
#         lastImageRequestTime = current_time
#         response = requests.request('GET', api_url).json()
#         hdurl = response['hdurl']
#         date = response['date']
#         return {
#             'hdurl': hdurl,
#             'date': date
#         }
#     else:
#         return None
#
#
# def start():
#     global root
#     # while True:
#     current_datetime = get_date()
#     url = get_hd_image_url(current_datetime)
#     print(f'URL: {url}')
#     if url is not None:
#         print('Downloading image')
#         req.urlretrieve(url['hdurl'], f"images/{current_datetime}.jpg")
#         pilImg = Image.open(f'images/{current_datetime}.jpg')
#         root.update()
#         showPIL(pilImg)
#
#     time.sleep(seconds_delay)
#     root.after(seconds_delay * 1000, start)
#
#
# start()
