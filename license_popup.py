# PRISM Security Suite - Protocol Response Interface for Systems Management
# Copyright (C) HYPE Industries Military Defense Division - All Rights Reserved (HYPE-MMD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, April 2020 (CORONA-VACATION)


import PIL
from tkinter import *
from PIL import Image,ImageTk


def dialog( self ):
    self.root = Toplevel();
    # self.root.lift();
    self.root.resizable( False, False );
    self.root.bind( '<Escape>', lambda e: self.root.quit() );

    w  = 600;
    h  = 380;
    ws = self.root.winfo_screenwidth();
    hs = self.root.winfo_screenheight();
    x  = (ws/2) - (w/2)
    y  = (hs/2) - (h/2)
    self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    self.root.title( "Prism Community Edition 2020 | License" );
    self.root.configure();

    self.canvas = Canvas( self.root, width=w, height=h );
    self.canvas.pack( fill="both", expand=True );
    self.canvas.create_text( 300, 45, fill="black", font="Helvetica 15", text="Prism Community Edition 2020", anchor=CENTER );
    self.canvas.create_text( 300, 70, fill="grey", font="Helvetica 12", text="1.0.0 Beta", anchor=CENTER );
    self.canvas.create_text( 300, 150, fill="grey", font="Helvetica 10", text="All information contained herein is, and remains the property of HYPE Industries and its suppliers, if any. The intellectual and technical concepts contained herein are proprietary to HYPE Industries and its suppliers and may be covered by U.S. and Foreign Patents, patents in process, and are protected by trade secret or copyright law. Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtaine from HYPE Industries.", anchor=CENTER, justify=CENTER, width="500" );
    self.canvas.create_text( 300, 225, fill="grey", font="Helvetica 10", text="Copyright (C) HYPE Industries Military Defense Division - All Rights Reserved (HYPE-MMD) Dissemination of this information or reproduction of this material is strictly forbidden by penalty of law.", anchor=CENTER, justify=CENTER, width="500" );
    self.canvas.create_text( 300, 300, fill="black", font="Helvetica 10", text="Designed by HYPE Industries. Written by Evan Sellers.", anchor=CENTER );
    self.canvas.create_text( 300, 330, fill="grey", font="Helvetica 10", text="Zach Bostock, Yash Gajjar, Connor Harrison, Nishant Murugesan, Matthew Patrohay, Sam Pfister, Jack Saysana, Evan Sellers", anchor=CENTER, justify=CENTER, width="500" );

    self.root.focus_set()
    self.root.grab_set()
    self.root.wait_window()
