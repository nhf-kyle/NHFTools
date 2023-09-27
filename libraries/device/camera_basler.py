#Version 23.01 [NOT STABLE, IN DEVELOPMENT] Library to manipulate Basler ACE cameras for 2D Machine Vision

import os
from pypylon import pylon
import cv2 as cv

class Camera:
    def __init__(self, path=None, save_flag=False):
        self.image = {}
        self.save_flag = save_flag
        self.set_image_path(path)
        #Initialize connection to camera
        try:
            self.connect()	
            #self.set_exposure(260000)
            self.connect_status = True
        except:
            self.connect_status = False
            
    #Set path and index for saving raw images
    def set_image_path(self,path):
        #Save to path if specified
        if path:
            self.path = path
        else:
            self.path = f'{os.getcwd()}\\images\\raw\\'
        #Determine index (for naming images) based on existing images in path
        image_list = [int(file.replace('.bmp','')) for file in os.listdir(self.path)]
        self.index = 0 if not image_list else max(image_list)

    #Connect to camera at specified address
    def connect(self):
        self.camera    = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat  = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        
    #Trigger camera and acquire image
    def grab_image(self):
        #Acquire Image
        self.camera.Open()
        self.camera.StartGrabbingMax(1)
        while self.camera.IsGrabbing():
            frame = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if frame.GrabSucceeded():
                #Convert raw image to openCV format
                converted_frame = self.converter.Convert(frame)
                self.image = converted_frame.GetArray()
                frame.Release()
        self.camera.Close()
        if self.save_flag:
            self.save_image()
        
    #Trigger camera and acquire video. Process each frame through pipeline [NOT TESTED]
    def grab_video(self, pipelines = None):
        #Acquire Image
        self.camera.Open()
        self.camera.StartGrabbing()
        while self.camera.IsGrabbing():
            frame = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if frame.GrabSucceeded():
                #Convert raw image to openCV format
                converted_frame = self.converter.Convert(frame)
                result = converted_frame.GetArray()
                if pipelines:
                    for process in pipelines:
                        result = process(result)
            frame.Release()
            if result:
                self.image = image
            self.camera.StopGrabbing()
        self.camera.Close()
        
    #Save openCV image to specified output directory
    def save_image(self):
        cv.imwrite('{path}{index}.bmp'.format(path = self.path, index = self.index), self.image)
        self.index = self.index + 1
        
    #Save raw image to specified output directory (before openCV conversion)
    def save_image_raw(self, frame):
        self.index = self.index + 1
        image = pylon.PylonImage()
        image.AttachGrabResultBuffer(frame)
        image.Save(pylon.ImageFileFormat_Bmp, f'{self.path}{self.index}.bmp')
        
    #Get value of a GeniCAM parameter
    def get_parameter(self, parameter):
        value = parameter.Value
        return value
        
    #Set value of a GeniCAM parameter
    def set_parameter(self, parameter, value):
        parameter.SetValue(value)
        
    #Exposure Control
    def get_exposure(self):
        return self.get_parameter(self.camera.ExposureTime)
        
    def set_exposure(self, value):
        self.set_parameter(self.camera.ExposureTime, value)
        
    #Gain Control
    def get_gain(self):
        return self.get_parameter(self.camera.Gain)
        
    def set_gain(self, value):
        self.set_parameter(self.camera.Gain, value)