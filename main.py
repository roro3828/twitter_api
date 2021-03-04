import twitter_api
import tkinter

root=tkinter.Tk()
root.title('Twitter')
f=tkinter.Frame(root,width=120,height=720)

tweets=twitter_api.timelines(9334242,20)

for i in tweets:
    label=tkinter.Label(f,text=i['text'])
    label.grid()

f.pack()

root.mainloop()