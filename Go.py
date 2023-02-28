
from SPEX_DIY_CSV_Machine import Product
import csv
import xml.dom.minidom


HeaderCSV=r"INPUT\Header.csv"
DOMTree = xml.dom.minidom.parse("INPUT\SPEX PRODUCTS.xml")
productData = DOMTree.documentElement
#cushion = Product(productData,"1613","1135")

def main(cuttingListRaw=r"INPUT\Book2.csv",PSOutputCSV=r"OUTPUT\PSOutputCSV.csv"):

    outputDicts=[]
    head=[]
    spex1ChangedFlag=False
    spex1Header=[]
    with open(cuttingListRaw, mode='r') as csv_file:
                reader=csv.DictReader(csv_file)

            # loading all the required parts from the CSV
                
                for row in reader:
                    p=Product(productData,row['style and dimensions'],row['pn'],QTY=row['quantity'],seqNum=row['part_of_sequence'])  # create all the product objects
                    outputDicts=outputDicts+(p.PSInputLine())              # collect all the lines 
                for l in outputDicts:  
                                                # scan through again to get all the Keys which will form the headers in the csv        
                    for k in l.keys():
                        if k not in head:
                            head.append(k)

    #with open(HeaderCSV,mode='w') as csv_file:
    
    #  writer=csv.DictWriter(csv_file,fieldnames=head)
    #  writer.writeheader()
    with open(HeaderCSV,mode='r') as csv_file:
    
        reader = csv.reader(csv_file,delimiter=',')
        for row in reader:
            spex1Header=row
            break
    #  writer.writeheader()

    for headerItem in head:
        if headerItem not in spex1Header:
            print(f"item not in header {headerItem}")
            spex1Header.append(headerItem)
            spex1ChangedFlag=True

    if spex1ChangedFlag:
        with open(HeaderCSV,mode='w') as csv_file:
            writer=csv.DictWriter(csv_file,fieldnames=spex1Header)
            writer.writeheader()

    with open(PSOutputCSV,mode='w') as csv_file:
    
        writer=csv.DictWriter(csv_file,fieldnames=spex1Header)
        writer.writeheader()
        
        for idx,line in enumerate(outputDicts):
            
            line["ID"]=str("{:.2f}".format(idx*.01+1.0))   # formating required as Label tool is comparing string not number
            writer.writerow(line)

if __name__=="__main__":
    main()