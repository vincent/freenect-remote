#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import sys, time
import threading
import simplejson

from Xlib import X, display
import pymouse

class FreenectControlServer():

    def __init__(self):
        context = zmq.Context()
        self.subscriber = context.socket (zmq.SUB)
        self.subscriber.connect ("tcp://*:14444")
        self.subscriber.setsockopt (zmq.SUBSCRIBE, "event")

        d = display.Display()
        s = d.screen()
        root = s.root

        m = pymouse.PyMouse()
        width, height = m.screen_size()
        
        last_position = { 'x':0, 'y':0 }
        mouse_down = False
        while True:
            try:
                message = self.subscriber.recv()
                message = simplejson.loads(message)
            except:
                message = "undefined"
            
            print message
            
            if type(message).__name__=='str':
                pass

            elif message['type'] == "Unregister":
                mouse_down = False
        
            elif message['type'] == "HandClick":
                message['data'] = last_position
                x = width / 100 * (100 - int(message['data']['x']))
                y = height / 100 * int(message['data']['y'])
                
                if mouse_down:
                    m.release(x, y)
                else:
                    m.press(x, y)
                    
                mouse_down = not mouse_down
        
            elif message['type'] == "Move":
                x = width / 100 * (100 - int(message['data']['x']))
                y = height / 100 * int(message['data']['y'])
                
                #root.warp_pointer(x,y)
                #d.sync()
                
                last_position = message['data']
                m.move(x, y)
            
                

if __name__ == "__main__":
    s = FreenectControlServer()