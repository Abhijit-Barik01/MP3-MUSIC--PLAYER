from tkinter import*
from tkinter import filedialog #ttk widget
import pygame
import time
from mutagen.mp3 import MP3 #pip install mutagen


root =Tk() #window is  root
root.title("MP3 Player")
root.geometry("500x400")#size of my app
# Initialize Pygame
pygame.mixer.init()

#in Tkinter everything is widget.widget has atrribute
#creating one song add function
def add_song():
	song=filedialog.askopenfilename(initialdir='audio/',title="choose A song",filetypes=(("mp3 File","*.mp3"),))
	song=song.replace("C:/mp3/audio/","")
	song=song.replace(".mp3","")


	playlist_box.insert(END,song)# inserting song in playlist_box

#creating many song add function
def add_many_songs():
	songs=filedialog.askopenfilenames(initialdir='audio/',title="choose many song",filetypes=(("mp3 File","*.mp3"),))
	#Loop through song list and replace directory structure and mp3 song name

	for song in songs:
		#strip out directory structure and mp3
		song=song.replace("C:/mp3/audio/","")
		song=song.replace(".mp3","")
		playlist_box.insert(END,song)# inserting song in playlist_box


	# Create Function To Delete One Song From Playlists
def delete_song():
	# Delete Highlighted Song From Playlist
	playlist_box.delete(ANCHOR) #anchor is highlighted area

# Create Function To Delete All Songs From Playlist
def delete_all_songs():
	# Delete ALL songs 
	playlist_box.delete(0, END)

# Create Play Function
def play():
	
	# Reconstruct song with directory structure stuff
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	
	#Load song with pygame mixer
	pygame.mixer.music.load(song)
	#Play song with pygame mixer
	pygame.mixer.music.play(loops=0)
	# Get Song Time
	play_time()
	# Create Stopped Variable
def stop():
	# Stop the song
	pygame.mixer.music.stop()
	# Clear Playlist Bar
	playlist_box.selection_clear(ACTIVE)
	status_bar.config(text='')


# Create Paused Variable
global paused 
paused = False
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		#Pause
		pygame.mixer.music.pause()
		paused = True
# Create Function To Play The Next Song
def next_song():
	
	#Get current song number
	next_one = playlist_box.curselection()
	# Add One To The Current Song Number Tuple/list
	next_one = next_one[0] + 1

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	# Add directory structure stuff to the song title
	song = f'C:/mp3/audio/{song}.mp3'
	#Load song with pygame mixer
	pygame.mixer.music.load(song)
	#Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear Active Bar in Playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set Active Bar To next song
	playlist_box.selection_set(next_one, last=None)
 #Create function to play previous song
def previous_song():
	
	#Get current song number
	next_one = playlist_box.curselection()
	# Add One To The Current Song Number Tuple/list
	next_one = next_one[0] - 1

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	# Add directory structure stuff to the song title
	song = f'C:/mp3/audio/{song}.mp3'
	#Load song with pygame mixer
	pygame.mixer.music.load(song)
	#Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear Active Bar in Playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set Active Bar To next song
	playlist_box.selection_set(next_one, last=None)

# Create Function To Deal With Time
def play_time():
	

	# Grab Current Song Time
	current_time = pygame.mixer.music.get_pos() / 1000
	# Convert Song Time To Time Format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))


	# Reconstruct song with directory structure stuff
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'

	# Find Current Song Length
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length
	# Convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
	

	# Add Current Time To Status Bar
	if current_time >=1:
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
	
	# Create Loop To Check the time every second
	status_bar.after(1000, play_time)


playlist_box=Listbox(root,bg="black",fg="green",width=60,selectbackground="green",selectforeground="black")#Here we define play_list variable.List_box() is widget.in side widget(root) ,root is attribute
playlist_box.pack(pady=20)#here we put listbox  in screen.pady is for padding in window acccording y axis
#  we want to something like box for putting image button in it.so to do that we use frame widget
control_frame=Frame(root)
control_frame.pack(pady=20)
#Define button images For controls
back_btn_img=PhotoImage(file='images/back50.png')
forward_btn_img=PhotoImage(file='images/forward50.png')
play_btn_img=PhotoImage(file='images/play50.png')
pause_btn_img=PhotoImage(file='images/Pause50.png')
stop_btn_img=PhotoImage(file='images/stop50.png')






#create play/stop etc Button.Hhere i have defined button widget
back_button=Button(control_frame,image=back_btn_img,borderwidth=0, command=previous_song)
forward_button=Button(control_frame,image=forward_btn_img,borderwidth=0, command=next_song)

play_button=Button(control_frame,image=play_btn_img,borderwidth=0,command=play)

pause_button= Button(control_frame,image=pause_btn_img,borderwidth=0, command=lambda: pause(paused))

stop_button=Button(control_frame,image=stop_btn_img,borderwidth=0,command=stop)
#Instead of pack here i have used grid().
back_button.grid(row=0,column=0,padx=10) #i have used padx=10 for given space between button
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

#CREATE MENU
my_menu=Menu(root)
root.config(menu=my_menu)

#Create Add Song Menu Dropdows
add_song_menu=Menu(my_menu,tearoff=0) #creating sub menu
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
#Add one song
add_song_menu.add_command(label="Add one song to a playlist",command=add_song)
#Add many song
add_song_menu.add_command(label="Add many song to a playlist",command=add_many_songs)

# Create Delete Song Menu Dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)
# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Temorary label
my_label=Label(root,text='')
my_label.pack(pady=20)

root.mainloop()