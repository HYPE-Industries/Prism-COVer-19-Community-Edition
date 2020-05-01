# PRISM Security Suite - Protocol Response Interface for Systems Management
# Copyright (C) HYPE Industries Military Defense Division - All Rights Reserved (HYPE-MMD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, April 2020 (CORONA-VACATION)

import cv2
import imutils

face_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def blackScreen( frame ):
    frame = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY );
    frame = cv2.threshold( frame, 25, 255, cv2.THRESH_BINARY )[ 1 ];
    count = ( ( frame.shape[ 0 ] * frame.shape[ 1 ]  ) - cv2.countNonZero( frame ) );
    return True if ( int( ( frame.shape[ 0 ] * frame.shape[ 1 ] ) * 0.90 ) < count ) else False;


def faces( frame ):
    return face_cascade.detectMultiScale( cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY ), 1.3, 5 );