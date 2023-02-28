import sys

import re
from pathlib import Path
import os

class Marker:

    def __init__(self, p):
        self.path = p                   
        p=os.path.split(p)
        self.name=p[1].split('.')    # Seperate File Name from Path and Extension
        if self.name[1]=='CUT':
            self.name=self.name[0]+" CUT"
        else:
            self.name=self.name[0]
        self.materialList={
        'CODRA':1,'LYCRA':2,'LOOP':3,'SPACER':4,'SPEXTEX':5,'PALMHIVE LAYERED':6,'PALMHIVE':7,'RED LYCRA':9,'MERINO':10}
        self.rank=20

    def calcRank(self):
        split=self.name.split()
        if len(split)>1 and split[1]=="PALMHIVE" and split[0] !='GLUED':
            self.rank=8
        for key in self.materialList:        # looping through the list of materials we are looking for
            if key == self.name:
                self.rank=self.materialList[key]      # exact match no change required
                break
        
            numM=re.match(r'('+key+r')\s+[0-9]',self.name) # will match lycra 1 lyrca 2 ect
            if numM is not None:
                
                self.rank=self.materialList[key]
                break
    


    def getDiffDims(self):
        with open(self.path,'r') as reader: 

            lines=list(reader.readlines()) #  reads the whole file to memory
        
        ext=str(self.path).split('.')[1] # getting the file type .cut or .txt
        px=re.compile(r'.*?X(\d*)',re.I) # 
        py=re.compile(r'.*?Y(\d*)',re.I)  # this will generate a match for every point...
        nP=re.compile(r'.*N(\d*)\*',re.I)
        self.calcRank()
        maxY=0
        maxX=0
        pieces=0
            
        resultX=None
        for line in list(lines):    
            if 'QX' in line:           # the QX is sometimes larger than the marker not sure why
                
                break                   # thats kinda Rough 

            resultY=py.findall(line)   # find all will give an array of all the matches
            resultX=px.findall(line)  
            resultNP=nP.match(line)
            if resultNP is not None:
                #print (resultNP.groups(1)[0])
                pieces=max(pieces,int(resultNP.groups(1)[0]))
            for resy in resultY:       # iterating though all tha matches on a line to find the highst Y value
                    
                try:                   # the try is there becaue is seems  to match '' sometimes not sure why
                    if int(resy)>maxY:
                        maxY=int(resy)
                except:
                    pass
                  
            for resx in resultX:     # iterating though all tha matches on a line to find the highst x value
                    
                try:                #the try is there becaue is seems  to match '' sometimes not sure why
                    if int(resx)>maxX:
                        maxX=int(resx)
                except:
                    pass
                   
           
               
        if resultX is not None or resultX!='': 
            if ext=="CUT":
                self.length=float(maxX)/100   # the cut flile is running in hundredths cm
                self.width=float(maxY)/100
                
            else: 
                self.length=float(maxX)*0.0254   # the txt flile is running in hundredths of inches (Sigh, Americans)
                self.width=float(maxY)*0.0254  
            self.np=pieces                 
            return [self.name,'L='+str(int(self.length))+ ' W= '+str(round(self.width))+" N="+str(pieces),self.rank] # the double cast remove the decimals
            jellybeans=5
        else: return ([self.name,'ERROR',self.rank])                       # time to do it the old fashioned way

    
                
               
     

