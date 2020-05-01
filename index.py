# PRISM Security Suite - Protocol Response Interface for Systems Management
# Copyright (C) HYPE Industries Military Defense Division - All Rights Reserved (HYPE-MMD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, April 2020 (CORONA-VACATION)


import PIL
from PIL import Image,ImageTk
import pytesseract
import cv2
from tkinter import *
from tkinter import messagebox
from time import sleep
import datetime
import copy
import time
from darkflow.net.build import TFNet



import license_popup
import process
import hardware

cooldown = 30;

# Might fix memory errors
# import gc
# gc.collect()

options = {
    'pbLoad': './built_graph/prism.pb',
    'metaLoad': './built_graph/prism.meta',
    'threshold': 0.35,
}

#0.15

tfnet = TFNet(options);


# Globals
splash_root   = None;
main_root     = None;
main_canvas   = None;
width         = None;
height        = None;
cameras = [];
# Define Window




def load_cameras():
    global cameras;
    cameras = hardware.init();



# Main Screen
def main():
    global main_root, main_canvas;
    main_root = Tk();
    main_root.title( "Prism Community Edition 2020 | Weapon Detection Dashboard" );
    main_root.bind( '<Escape>', lambda e: main_root.quit() );
    width = int( main_root.winfo_screenwidth() * 0.80 );
    height = int( main_root.winfo_screenheight() * 0.80 );
    main_root.geometry( str( width ) + "x" + str( height ) );
    main_canvas = Canvas( main_root, width=width, height=height );
    main_canvas.pack( fill="both", expand=True );

# Class Canvas Update
def show_frame( self, cameras ):
    global width, height;

    width  = self.winfo_width();
    height = self.winfo_height();


    # footer
    # _, frame = cameras[0].read();

    self.delete("all");

    for cam in cameras:
        if cam.width and cam.height:
            cam._frame = cv2.resize( cam._frame, ( cam.width, cam.height ), interpolation = cv2.INTER_AREA )
        self.img0 = ImageTk.PhotoImage( PIL.Image.fromarray( cv2.cvtColor( cv2.flip( cam._frame, 1 ), cv2.COLOR_BGR2RGBA ) ) );
        self.create_image( int( 20 + cam.x_pos ), int( 80 + cam.y_pos ), anchor=NW, image=self.img0 );


    # Control bar
    self.image = ImageTk.PhotoImage( PIL.Image.open( "assets/hype-logo-black-padding-75.png" ) );
    self.create_image( 10, 0, image=self.image, anchor=NW );
    self.create_text( 150, 18, fill="black", font="Helvetica 15", text="Prism Server 2020 COVer-19", anchor=NW );
    self.create_text( 150, 40, fill="grey", font="Helvetica 8", text="1.0.0 Beta", anchor=NW );
    self.create_text( width - 600, 14, fill="black", font="Helvetica 20", text=str( datetime.datetime.now().hour ) + ":" + str( datetime.datetime.now().minute ) + ":" + str( datetime.datetime.now().second ) + "." + str( datetime.datetime.now().microsecond )[:2], anchor=NW );
    self.create_text( width - 600, 45, fill="grey", font="Helvetica 8", text=datetime.datetime.now().strftime("%a, %b %d, %Y"), anchor=NW );
    button( self, "License", width - 435, 18, license_popup.dialog );
    button( self, "Screenshot", width - 340, 18, clicked );
    button( self, "Shutdown", width - 225, 18, shutdown );
    button( self, "Lockdown", width - 120, 18, clicked, bg="red", fg="white" );


def button( canvas, text, x, y, action, bg="grey80", fg="black" ):
    padding = ( 20, 10 );
    buttonTXTGhost = Label( canvas, text=text, font='Helvetica 10', fg=fg, bg=bg, justify=LEFT ); # just fot scale
    buttonBG  = canvas.create_rectangle( x, y, ( x + buttonTXTGhost.winfo_reqwidth() + ( 2 * padding[ 0 ] ) - 7 ),  ( y + buttonTXTGhost.winfo_reqheight() + ( 2 * padding[ 1 ] ) - 5 ), fill=bg, outline="grey60" );
    buttonTXT = canvas.create_text( x + padding[0], y + padding[1], text=text, font='Helvetica 10', fill=fg, anchor=NW, justify=LEFT );
    canvas.tag_bind( buttonBG, "<Button-1>", action );
    canvas.tag_bind( buttonTXT, "<Button-1>", action );

def clicked( event ):
    print("cciked")

def splash_screen():
    global splash_root;
    splash_root = Tk()
    splash_root.overrideredirect( 1 );
    splash_root.lift();
    splash_root.wm_attributes("-topmost", True)
    # splash_root.wm_attributes("-disabled", True)

    # Center On Screen
    w  = 800;
    h  = 500;
    ws = splash_root.winfo_screenwidth();
    hs = splash_root.winfo_screenheight();
    x  = (ws/2) - (w/2)
    y  = (hs/2) - (h/2)
    splash_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    splash_root.title( "Prism Mainframe 2020 | Hype Industries" );
    splash_root.configure()
    spath = "assets/splash.png"
    simg = ImageTk.PhotoImage( PIL.Image.open(spath))
    my = Label(splash_root,image=simg)
    my.image = simg
    my.place(x=0,y=0)
    lbl1 = Label(splash_root, text="1.0.0 Beta", font='Helvetica 10', fg='grey', bg='white', justify=LEFT )
    lbl1.place(x=60,y=240)

# Shutdown Command
def shutdown( event ):
    global main_root;
    print("wer")
    option = messagebox.askquestion(title="Shutdown Prism Server 2020", message="Are you sure you want to shutdown?\nWeapon detection and other Security options will be offline for the deration of downtime.",icon='warning',default='no');
    if option == "yes":
        main_root.destroy();

# Step 1 Startup
def startup():
    global main_root, main_canvas, splash_root;
    splash_screen();
    splash_root.after(1000, post);
    splash_root.mainloop();

face_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Step 2 Startup
def post():
    global cooldown;
    load_cameras();
    splash_root.destroy();
    main();

    while 1:
        frames = [];

        for cam in cameras:
            frame = cam.frame();
            _frame = copy.copy(frame);
            for (x,y,w,h) in process.faces( frame ):
                # crop = frame[ y:(y+h), x:(x+w) ]
                try:
                    crop = frame[int(y-(h/2)):int(y+h+(h/2)),frame.shape[1], int(x-(w/2)):int(x+w+(w/2))]
                except:
                    crop = frame[ y:(y+h), x:(x+w) ]
                cv2.rectangle(_frame, (x,y), (x+w,y+h), (255, 0, 0), 1)
                if len( tfnet.return_predict( crop ) ) == 0:
                    if cam.cooldown < int(time.time()):
                        cv2.imwrite("output/" + str(int(time.time())) + "_" + cam.id + "_" + str(x) + "_" + str(y) + ".png", crop)
                    cv2.rectangle(_frame, (x,y), (x+w,y+h), (0, 0, 255), 3)
                    cam.cooldown = int(time.time()) + cooldown
                    print("someone not wearing mask");
            cam._frame = _frame;
        show_frame( main_canvas, cameras );
        # main_canvas.update_idletasks();
        main_canvas.update();

    main_root.mainloop()


startup();
