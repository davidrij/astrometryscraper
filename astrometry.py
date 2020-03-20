#Class to select random astrometry.net database entries, download the image and pass it on
import numpy as np
from astropy.io import fits
import csv
import time
import os

class Astrometry:
    """Class that loads the crawled database and downloads and outputs the images"""
    def __init__(self, databasecsv,waittime=0.1):
        self.databasecsv = databasecsv
        #Open database as dict
        self._database = open(self.databasecsv)
        self._reader = csv.DictReader(self._database)
        self.waittime = waittime #seconds, time for the program to wait for entry search

    def image_entry(self, FOV=None):
        """Method to return random database entry
        Args:
        -   FOV (deg): if set, the method will try to find an image with a radius that
            would correspond to this FOV if the image was square (with a margin of 2 degree
            for the FOV). Otherwise a random image will be returned.
        Returns:
        -"""
        #TODO: elaborate to set parameters such ra, dec. 
        #TODO: make sure there is still a spread between the returned images
        #TODO: find a better way to filter for FOV
        #TODO: make fail-safe (try-catch)
        #TODO: fix header missing endcard bug
        for entry in self._reader:
            if FOV is not None:
                    try:
                        if (FOV-2) <= 2*float(entry["radius"])/np.sqrt(2) and (FOV+2) >= 2*float(entry["radius"])/np.sqrt(2):
                            #download image
                            page = "http://nova.astrometry.net/new_fits_file/" + str(entry["jobnumber"])
                            os.system('wget -O tempimage_' + str(entry["jobnumber"])+ '.fits ' + str(page))
                            
                            image_file = 'tempimage_' + str(entry["jobnumber"])+ '.fits'
                            image_data = fits.getdata(image_file,ignore_missing_end=True)
                            
                            fovx = image_data.shape[0]*float(entry["pixscale"])/3600
                            fovy = image_data.shape[1]*float(entry["pixscale"])/3600
                            
                            if FOV-0.5 <= fovx <= FOV+0.5 and FOV-0.5 <= fovy <= FOV+0.5:
                                os.system('mv ' + image_file + ' images/image_' + str(entry["jobnumber"]) + '.fits')
                            else:
                                os.system('rm ' + image_file)
                    except:
                        print("Something is wrong with this image")
                    
                    time.sleep(self.waittime) #wait for waittime seconds in order to give the website some rest!


                    


astro = Astrometry('Astrometry_database_stable.csv')
astro.image_entry(FOV = 20)