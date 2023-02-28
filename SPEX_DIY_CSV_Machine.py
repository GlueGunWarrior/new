# Good Evening

import csv

class Product:

    code="0"
    size='0'
    components=[]
    contains=[]

    
    def __init__(self,productData,size,code,seqNum,QTY):
       
        self.varDicts=[]
        self.code=code
        self.size=size
        self.seqNum=seqNum
        self.QTY=QTY
        self.BoarderColour="099"
        
#-----------------------------------------------------------------------
        if len(self.size)==4 and self.size.isdigit(): 
            self.WIDTH=self.size[0:2]
            self.DH=self.size[2:4]
        elif len(self.size)>4 and self.size[len(self.size)-4:len(self.size)]:
            self.WIDTH=self.size[len(self.size)-4:len(self.size)-2]
            self.DH=self.size[len(self.size)-2:len(self.size)]
            self.size=self.size=f'{self.WIDTH}{self.DH}'

        else:
            print('product doent have valid chushion or backrest size')

#------------------------------------------------------------------------
        codeBreakDown=code.split("-")
        l=len(codeBreakDown)
        print(codeBreakDown)
        if "_" in codeBreakDown[l-1]:
            print(codeBreakDown[l-1].split("_")[0])
            self.BoarderColour=codeBreakDown[l-1].split("_")[1]
            codeBreakDown[l-1]=codeBreakDown[l-1].split("_")[0]

        candidate=None
        products=productData.getElementsByTagName("PRODUCT")
        for p in products:   #use product code to find pattern
            if l<1:
                break
            if codeBreakDown[0]!=p.getElementsByTagName("FIRST")[0].childNodes[0].data and  p.getElementsByTagName("FIRST")[0].childNodes[0].data!="ANY":
                continue
            candidate=p
            if l<2:
                break
            if codeBreakDown[1]!=p.getElementsByTagName("SECOND")[0].childNodes[0].data and  p.getElementsByTagName("SECOND")[0].childNodes[0].data!="ANY":
                print(codeBreakDown[1])
                candidate=None
                continue
            if l<3:
                break
            if codeBreakDown[2]!=p.getElementsByTagName("THIRD")[0].childNodes[0].data and  p.getElementsByTagName("THIRD")[0].childNodes[0].data!="ANY":
                candidate=None
                continue
            if l<4:
                codeBreakDown.append("NONE")   # CHECK THAT A THERE IS NOT SUPPOSED TO BE A FOURTH SECTION IE '-C' OR SOMETHING
            if codeBreakDown[3]!=p.getElementsByTagName("FORTH")[0].childNodes[0].data and  p.getElementsByTagName("FORTH")[0].childNodes[0].data!="ANY":
                candidate=None
                continue
            break   #COMPLETE MATCH 

        #print(candidate)
#------------------------------------------------------------------------
        self.label=f"{self.seqNum} \\n {codeBreakDown[0]} {codeBreakDown[2]} \\n {self.size}"

#-------------------------------------------------------------------------      
        if candidate==None:
            print(F"cant find {codeBreakDown}")
            return 
#-------------------------------------------------------------------------
        vd=self.assignVars(candidate)
        if vd["PATTERN"] != "NONE":
            print(vd["PATTERN"])
            self.varDicts.append(self.calcRules(candidate,vd))

#-------------------------------------------------------------------------        
        children = candidate.getElementsByTagName("CONTAINS")
        childProducts=[]
        children=self.gatherChildren(children,childProducts,products)
        
      
#-------------------------------------------------------------------------

        for c in children:
            if c is not None:
                childDict=self.assignVars(c)
                self.varDicts.append(self.calcRules(c,childDict))
   
   
    def assignVars(self,candidate):
        varDict={}
        vars = candidate.getElementsByTagName("VAR")
        if vars is not None:
            for var in vars:
                var=var.childNodes[0].data
                var=var.split('=')
                if len(var)==2:
                    varDict[var[0]]=var[1]
                else:
                    varDict[var[0]]='0'
                pat=candidate.getElementsByTagName("PATTERN")[0]
                try:
                    varDict["PATTERN"]=pat.childNodes[0].data
                except:
                    varDict["PATTERN"] = None   
            varDict['QTY']=self.QTY
            varDict['seqNum']=self.seqNum
            if 'WIDTH' in varDict:
                varDict['WIDTH']=self.WIDTH
            if 'LABEL' in varDict:
            
                varDict["LABEL"]=f'{self.label} \\n {varDict["LABEL"]}'
            else:
                varDict['LABEL']=self.label
            varDict['BOARDERCOLOUR']=self.BoarderColour
            if "HEIGHT" in varDict:
                varDict['HEIGHT']=self.DH
            elif "DEPTH" in varDict:
                varDict['DEPTH']=self.DH
            if "SIZE" in varDict:
                varDict["SIZE"]=self.size
           
                    
        return varDict
    def PSInputLine(self):
        #print(self.varDicts)
        return self.varDicts                                                         # function to return the CSV line
    def calcRules(self,candidate,varDict):   # use rule tables to set Variables
        rules= candidate.getElementsByTagName("RULE")
        if rules is not None:
            #try:
            for rule in rules:
                path=rule.getElementsByTagName('PATH')[0].childNodes[0].data   #Path of the CSV to look up
                give=rule.getElementsByTagName('GIVE')[0].childNodes[0].data   # Name of Value to look up needs to match one of the VARS
                get=rule.getElementsByTagName('GET')[0].childNodes[0].data     # name of Expected return value. need to match one of the VARS
                
                with open(path, mode='r') as csv_file:                          # open CSV to look up
                    reader=csv.DictReader(csv_file)                            
                    for row in reader:
                        if row[give]==varDict[give]:
                            varDict[get]=row[get]
                            break
                    else: print('csv didnt contain the goods')                  # :-(
            #print (varDict)
        #except:
            #print('rule Failed')
            return varDict
    def gatherChildren(self,children,childProducts,products):
        for c in children:
            
            for p in products:
                #print(p.getElementsByTagName("PATTERN"))
                if p.getElementsByTagName("PATTERN") == "NONE":

                    continue
                
                if p.getElementsByTagName("PATTERN")[0].childNodes[0].data==c.childNodes[0].data:
                    childProducts.append(p)                       # children list should now be XML product elements
                    
                    if p.getElementsByTagName("CONTAINS") is not None:
                        childProducts=self.gatherChildren(p.getElementsByTagName("CONTAINS"),childProducts,products)
                        
                    break

            else:
                print ("lost child "+c.childNodes[0].data) 
        return childProducts
                    


    