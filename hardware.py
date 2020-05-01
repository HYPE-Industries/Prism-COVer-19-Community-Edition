# PRISM Security Suite - Protocol Response Interface for Systems Management
# Copyright (C) HYPE Industries Military Defense Division - All Rights Reserved (HYPE-MMD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, April 2020 (CORONA-VACATION)


import cv2
import PIL
from PIL import Image
import ctypes
import requests
import os
import json
import process



# Camera
class camera:
    def __init__( self, name, address, priority=0, description="", nullPatch=None, motionSensitivity=0.2, crop=None, disableCapture=None, x_pos=0, y_pos=0, width=None, height=None ):
        self.id                = name.replace( " ", "" ).lower();
        self.name              = name;
        self.address           = address;
        self.priority          = priority;
        self.description       = description;
        self.nullPatch         = nullPatch;
        self.motionSensitivity = motionSensitivity;
        self.crop              = crop;
        self.disableCapture    = disableCapture;
        self.size              = [];
        self.x_pos             = x_pos;
        self.y_pos             = y_pos;
        self.width             = width;
        self.height            = height;
        self.cooldown          = None;

        if disableCapture != True:
            self.capture    = cv2.VideoCapture( address );
            self.firstFrame = self.frame(); # First Frame

            if self.capture.isOpened() == False:
                print( "[WDS] Error unable to open camera " + self.name );
                # ctypes.windll.user32.MessageBoxW( 0, "Unable to access camera " + self.name + "@" + str( self.address ) + "\nSystem Halt.", "Prism WDS Error", 16 );
                quit();

            if process.blackScreen( self.firstFrame ):
                print( "[WDS] Warning. Camera " + self.name + "@" + str( self.address ) + " view appears to be obstructed." );
                # ctypes.windll.user32.MessageBoxW( 0, "[WDS] Camera " + self.name + "@" + str( self.address ) + " view appears to be obstructed. \n System will proceed.", "Prism WDS Warning", 16 );
                quit();
        else:
            self.capture    = None;
            self.firstFrame = None;



    def frame( self ):
        _, frame = self.capture.read();
        frame = cv2.flip( frame, 1 );
        self._frame = frame;
        # apply crop
        self.lastFrame = frame;
        return frame;


# loads from array
def load( array, disableCapture = None ):
    cams = [];
    for cam in array:
        for _search in cams:
            if cam[ "name" ].replace( " ", "" ).lower() == _search.name:
                print( "[WDS] Error unable to add camera " + cam[ "name" ].replace( " ", "" ).lower() + ". As it's name is conflicting. Spaces and Caps." );
                # ctypes.windll.user32.MessageBoxW( 0, "Error unable to add camera " + cam[ "name" ].replace( " ", "" ).lower() + ". As it's name is conflicting. Spaces and Caps.\nSystem Halt.", "Prism WDS Error", 16 );
                quit();
        cams.append( camera( cam[ "name" ], cam[ "address" ],
            priority = cam[ "priority" ] if "priority" in cam else None,
            description = cam[ "description" ] if "description" in cam else None,
            nullPatch = cam[ "nullPatch" ] if "nullPatch" in cam else None,
            motionSensitivity = cam[ "motionSensitivity" ] if "motionSensitivity" in cam else None,
            crop = cam[ "crop" ] if "crop" in cam else None,
            x_pos = cam[ "x_pos" ] if "x_pos" in cam else 0,
            y_pos = cam[ "y_pos" ] if "y_pos" in cam else 0,
            width = cam[ "width" ] if "width" in cam else None,
            height = cam[ "height" ] if "height" in cam else None,
            disableCapture = disableCapture ) );
    return cams;


# will load hardware from json file
def init( disableCapture = None ):
    file = os.path.join( os.getcwd(), "hardware.json" );

    if not os.path.isfile( file ):
        print( "[WDS] Error unable to open hardware file: " + file );
        # ctypes.windll.user32.MessageBoxW( 0, "Error unable to open hardware file: " + file + "\nSystem Halt.", "Prism WDS Error", 16 );
        quit();


    try:
        data = json.load( open( file ) );
    except:
        print( "[WDS] Error unable to open hardware file. File seems to have syntext promblem." );
        # ctypes.windll.user32.MessageBoxW( 0, "Error unable to open hardware file. File seems to have syntext promblem.\nSystem Halt.", "Prism WDS Error", 16 );
        quit();

    return load( data[ "hardware" ], disableCapture )
