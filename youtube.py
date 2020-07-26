from tkinter import *
from pytube import YouTube
import os


root=Tk()

root.geometry('750x350+100+10')
root.title("Youtube downloader")
root.resizable(height = None, width = None)
logo=PhotoImage(file="logo.png")
root.iconphoto(False, logo)
scrollbar = Scrollbar(root)

top = Frame(root)
bottom = Frame(root)
top.pack(side=TOP)
bottom.pack(side=BOTTOM, expand=True)

TxtBox=Text(root,height=10,width=100,yscrollcommand=scrollbar.set,borderwidth=5)

def get_formats():
    global video
    global title
    global itag
    itag=[]
    if link.get()[0:24]!="https://www.youtube.com/":
        myVar.set("Enter the correct link ")
        link.set("")
    else:
        try:
            myVar.set("Fetching formats ..... ")
            video=YouTube(link.get())
            title=video.title
            root.update()
                    
            TxtBox.pack(fill=BOTH,expand=0,pady=10,padx=30)
            TxtBox.delete("1.0","end")
            TxtBox.insert(END,title+"\n\n")
            TxtBox.insert(END,"[#] Only \" progresssive--> True \" videos contain both audio and video \n\n")
            
            
            for i in video.streams:
                if i.is_progressive:
                    TxtBox.insert(END,"[#] ")
                else:
                    TxtBox.insert(END,"[ ] ")
                
                if str(i.type)=="video":
                    TxtBox.insert(END,"itag = "+str(i.itag)+"   "+"["+str(i.resolution)+" "+str(i.type)+" "+str(i.filesize/1000000)[0:5]+"mb"+" "
                                  +"Progressive --> "+str(i.is_progressive)+" ]\n")
                if str(i.type)=="audio":
                    TxtBox.insert(END,"itag = "+str(i.itag)+"   "+"["+str(i.abr)+" "+str(i.type)+" "+str(i.filesize/1000000)+"mb"+" "
                                  +"Progressive --> "+str(i.is_progressive)+" ]\n")
                itag.append(str(i.itag))
                    
##            list2g=[]
##            list2g=video.streams
##            for i in list2g:
##                i=str(i)
##                TxtBox.insert(END,i+"\n")
                
            scrollbar.config( command = TxtBox.yview)
            myVar.set("Enter Path (If Left empty gets downloaded to this file path)")
            ink.set("Enter itag value here")
            root.update()

        except Exception as e:
            if YouTube(link.get()).streams == None:
                Label(root, text=e, font="Consolas 10 bold").pack()
                myVar.set(e)
                root.update()
                link.set("Check Your Link")
            else:
                myVar.set("Enter Path (If Left like this gets downloaded to this file path)")
                link.set("Enter itag value here")
                
                root.update()
                

def download():
    try:
        global d_video
        if myVar.get() == "Enter Path (If Left like this gets downloaded to this file path)" or myVar.get()=="Enter the link below to download" or myVar.get()=="Video contains no audio" or myVar.get()=="Enter correct itag value.... " or myVar.get()=="Went WRONG....... ":
            def_path=""
        else:
            def_path=myVar.get()
        title=video.title
        video_format=link.get()
        if link.get()in itag:
            video_format=int(video_format)        
        
            try:
                myVar.set("Downloading..........")
                d_video=video.streams.get_by_itag(video_format)
                filename=title+str(video_format)
                if str(d_video.type)=="audio":
                    d_video.download(output_path= def_path,filename= filename)
                    myVar.set("Enter the link below to download")
                    link.set(title+" Downloaded Successfully to " + def_path)
                else:
                    if d_video.is_progressive:
                        d_video.download(output_path= def_path,filename=filename)
                        myVar.set("Enter the link below to download")
                        link.set(" Downloaded Successfully to " + def_path)
                    else:
                        d_video.download(output_path= def_path,filename=filename)
                        myVar.set("Video contains no audio")
                        link.set(" Downloaded Successfully - " + def_path)
                root.update()
            
            except Exception as e:
                link.set("Check your link")
                myVar.set(e)
                Label(root, text=e, font="Consolas 15 bold").pack()
            
        else:
            myVar.set("Enter correct itag value.... ")
            root.update()
            
    except Exception as e:
        Label(root, text=e, font="Consolas 10 bold").pack()
        myVar.set("Went WRONG....... ")
    

Label(root, text="Youtube Downloader", font="Consolas 15 bold").pack(in_=top, side=LEFT)

myVar=StringVar()
link=StringVar()

e=Entry(root,textvariable=myVar, width=70, borderwidth=5,justify=CENTER)
e.pack(pady=10)
Entry(root,textvariable=link, width=70, borderwidth=5,justify=CENTER).pack(pady=10)

myVar.set("Enter the link below")
link.set("")

Button(root, text="Get Formats", command=get_formats).pack(pady=5,in_=bottom,side=LEFT)
Button(root, text="Download file", command=download).pack(pady=5,in_=bottom,side=LEFT)


root.mainloop()
