#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:27:54 2020

@author: silasjimmy
"""

import os
import pickle
import cv2
import  numpy
import random

class ImageDataGen:
    def __init__(self, path, img_width=256, img_height=256):
        self.path = path
        self.img_width = img_width
        self.img_height = img_height
        self.category_names = {}
        
    def get_folder_names(self, path):
        '''
        Gets the list of names of the sub folders in the directory specified in the path.
        path (string): Path of the directory to get the name(s) of the subfolder(s).
        Returns the list of name(s) of the subfolder(s).
        '''
        return [os.path.basename(f.path) for f in os.scandir(path) if f.is_dir()]
    
    def to_pickle_file(self, filename, data):
        '''
        Creates a pickle object.
        filename (string): Name of the pickle object to create.
        data (tuple): Features and labels to be dumped to the pickle object.
        '''
        with open(filename, 'wb') as filename:
            pickle.dump(data, filename)
            
    def open_pickle_file(self, filename):
        '''
        Opens a pickle file.
        filename (string): Name of the file to open.
        Returns a tuple of features and labels of the data.
        '''
        with open(filename, 'rb') as pickle_in:
            data = pickle.load(pickle_in)
            return data
            
    def process_img(self, path, categories):
        '''
        Converts the images in the subfolders of path to arrays.
        path (string): Path of the folder with the images.
        categories (list): List of subfolder names in path.
        Returns a list of image data arrays.
        '''
        img_data_arrays = []
        
        for category in categories:
            category_path = os.path.join(path, category)
            class_number = categories.index(category)
            self.category_names[category] = class_number
            
            for img in os.listdir(category_path):
                img_array = cv2.imread(os.path.join(category_path, img))
                img_array = cv2.resize(img_array, (self.img_width, self.img_height))
                img_data_arrays.append([img_array, class_number])
                
        random.shuffle(img_data_arrays)
        
        return img_data_arrays
    
    def features_and_labels(self, image_data_arrays):
        '''
        Converts the list of image arrays to numpy arrays, and separates the data 
        to features and labels.
        image_data_arrays (list): list of the image arrays and labels.
        '''
        features, labels = [], []
    
        for image_data_array in image_data_arrays:
            features.append(image_data_array[0])
            labels.append(image_data_array[1])
                
        features = numpy.array(features)
        labels = numpy.array(labels)
            
        return features, labels
    
    def split_dataset(self):
        '''
        Splits the dataset to to train and test datasets.
        Returns a dictionary with the image arrays of each dataset.
        '''
        dataset_folders = self.get_folder_names(self.path)
        categories = self.get_folder_names(os.path.join(self.path, dataset_folders[0]))
        dataset_img_data = {}
        
        for folder in dataset_folders:
            folder_path = os.path.join(self.path, folder)
            img_data_arrays = self.process_img(folder_path, categories)
            features, labels = self.features_and_labels(img_data_arrays)
            dataset_img_data[folder] = (features, labels)
            
        return dataset_img_data
    
    def load_data(self):
        '''
        Loads the features and labels of the dataset.
        Returns two tuples with features and labels of each subfolder in the dataset folder.
        '''
        try:
            (x_train, y_train) = self.open_pickle_file('train')
            (x_test, y_test) = self.open_pickle_file('test')
         
            print('Dataset loaded successfully from the pickle objects.')

            return (x_train, y_train), (x_test, y_test)
        
        except:
            print('Loading dataset files...')
            
            dataset_img_data = self.split_dataset()
            
            x_train, y_train = dataset_img_data.get('train')
            x_test, y_test = dataset_img_data.get('test')
            
            print('Creating pickle objects for future faster dataset retrival...')
            
            self.to_pickle_file('train', (x_train, y_train))
            self.to_pickle_file('test', (x_test, y_test))
            
            print('Process finished successfully.')
            
            return (x_train, y_train), (x_test, y_test)
    
