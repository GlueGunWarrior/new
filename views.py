from datetime import date
from flask import render_template, redirect, url_for,request
from . import app
import os
from pathlib import Path
import pandas as pd
import csv
import Go

MARKERPATH=(r"C:\Release manager\app\MARKERS")
DATAFOLDER="DATA"
RAWCSVPATH="RAWRELEASE.csv"
OUTPUTCSV="OUTPUT.CSV"
RELEASESUBFOLDERS=['FABRIC',"CUSHION FOAM",'ACCESSORIES','BACKREST FOAM']


@app.route("/",methods = ['POST', 'GET'])
def home():
    return houseKeeping("TEST")

@app.route("/working/",methods = ['POST', 'GET'])
@app.route("/working/<Release>",methods = ['POST', 'GET'])
def working(Release):
    
    release=Release

    if request.method == "POST":
        
        releaseDate=request.form["RELASEDATE"]
        
        if releaseDate != '':
            releaseDate=date.fromisoformat(releaseDate).strftime("%d-%m-%y %A")    #formats date  dd-mm-yy Wednesday Adams 
        release=releaseDate+request.form["ALTTEXT"]
     
    return houseKeeping(release)

@app.route("/create/")
@app.route("/create/<Release>",methods = ['POST', 'GET'])
def create(Release):
    
    release=Release

    if request.method=="POST":
        print(request.form)

    path=os.path.join(MARKERPATH,release)

    if not os.path.exists(path):
        os.makedirs(os.path.join(path,DATAFOLDER))
        with open(os.path.join(path,DATAFOLDER,release+RAWCSVPATH),'x'):
            banana='ripe'
        if request.method=="POST":
            print(request.form)
            if  len(request.form):
                for folder in RELEASESUBFOLDERS:
                    os.makedirs(os.path.join(path,folder))
        

    return houseKeeping(release)


@app.route("/SDIYM/<Release>",methods = ['POST', 'GET'])
def SDIYM(Release):

    release=Release
    RawCSVPath=os.path.join(MARKERPATH, release,DATAFOLDER,release+RAWCSVPATH)
    outputPath=os.path.join(MARKERPATH,release,DATAFOLDER,release+OUTPUTCSV)
    Go.main(PSOutputCSV=outputPath,cuttingListRaw=RawCSVPath)
    readyTolabel=os.path.exists(outputPath)
    print(readyTolabel)
    return houseKeeping(release)

@app.route("/LABEL/<Release>",methods = ['POST', 'GET'])
def Label (Release):

    release=Release
    ReleaseFolder=os.path.join(MARKERPATH, release,DATAFOLDER,release+RAWCSVPATH)
    CSVLabels=os.path.join(MARKERPATH,release,DATAFOLDER,release+OUTPUTCSV)
    Labels.main(PSOutputCSV=outputPath,cuttingListRaw=RawCSVPath)
    
    return houseKeeping(release)

def houseKeeping(release):


    foldersCreated=os.path.exists(os.path.join(MARKERPATH,release))
    readyTolabel=os.path.exists(os.path.join(MARKERPATH,release,DATAFOLDER,release+OUTPUTCSV))

    return render_template("home.html", Release=release, foldersCreated=foldersCreated,readyTolabel=readyTolabel)
