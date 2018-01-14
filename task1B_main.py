#classes and subclasses to import
import cv2
import numpy as np
import os

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape,size,count):
    #open csv file in append mode
    filep = open('results1B_eYRC#509.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + size + "-" + count
    #write to csv
    filep.write(datastr)

def colorOf(BGR = []):
    if ((BGR[0] <= 60 & BGR[0] >= 0) & (BGR[1] <= 60 & BGR[1] >= 0) & (BGR[2] <= 255 & BGR[2] >= 200)):
        return "red",1
    elif ((BGR[0] <= 60 & BGR[0] >= 0) & (BGR[1] <= 255 & BGR[1] >= 200) & (BGR[2] <= 255 & BGR[2] >= 200)):
        return "yellow",2
    elif (( BGR[0] >= 0 & BGR[0] <= 100) & (BGR[1] >= 120 & BGR[1] <= 180) & (BGR[2] == 255)):
        return "orange",3
    elif ((BGR[0] <= 60 & BGR[0] >= 0) & (BGR[1] <= 255 & BGR[1] >= 200) & (BGR[2] <= 60 & BGR[2] >= 0)):
        return "green",4
    elif((BGR[0] <= 255 & BGR[0] >= 200) & (BGR[1] <= 60 & BGR[1] >= 0) & (BGR[2] <= 60 & BGR[2] >= 0)):
        return "blue",5

def main(path):
    original=cv2.imread(path)
    
    file_list = os.listdir(os.getcwd()+"\Sample Images")#put in the sample file location
    area_list=[]
    for i in file_list :
        image=cv2.imread("Sample Images\\"+i)
        edged_image=cv2.Canny(image.copy(),150,150)
        _,contours_image,heirarchy = cv2.findContours(edged_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area_list.append(cv2.contourArea(contours_image[0]))


    if "test" in path:
        square = cv2.imread('square.jpeg')
        gray_square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
        ret, thresh_square = cv2.threshold(gray_square,180,255,1)
        _,contours_sqr,heirarchy = cv2.findContours(thresh_square.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt1 = contours_sqr[0]

        edged_image = cv2.Canny(original.copy(),150,150)
        _,contours,heirarchy = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        required_matrix=np.zeros((6,4,5)) #red-1,yellow-2,orange-3,green-4,blue-5
                        #small-1,large-2,medium-3
                        #triangle-1,rectangle-2,square-3,circle-4
        font = cv2.FONT_HERSHEY_SIMPLEX

        countour_xy=[]
        
        for j in range (0,len(contours),2):
            i=contours[j]
            approx = cv2.approxPolyDP(i,0.01*cv2.arcLength(i,True),True)
            x = len(approx)
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            size = "medium"
            x1=i[0][0][0]+1
            y1=i[0][0][1]+1
            
            color,d = colorOf(original[y1,x1])#d is the color index of the required matrix
            area = cv2.contourArea(i)
            if(cv2.contourArea(i)<3500):
                        x=x-1
        
            if x == 3:
                if (area >= area_list[6]):
                    size = "large"
                    required_matrix[d,3,1]+=1
                elif (area <= area_list[7]):
                    size = "small"
                    required_matrix[d,1,1]+=1
                else :required_matrix[d,2,1]+=1    
                cv2.putText(original,size+" "+str(color)+" triangle", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
                continue    
            elif x == 4:
                ret = cv2.matchShapes(i,cnt1,1,0.0)
                if ret < 0.05:
                    if (area >= area_list[4]):
                        size = "large"
                        required_matrix[d,3,3]+=1
                    elif (area <= area_list[5]):
                        size = "small"
                        required_matrix[d,1,3]+=1
                    else:required_matrix[d,2,3]+=1    
                    cv2.putText(original, size+" "+str(color)+" square", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
                else:
                    if (area >= area_list[2]):
                        size = "large"
                        required_matrix[d,3,2]+=1
                    elif (area <= area_list[3]):
                        size = "small"
                        required_matrix[d,1,2]+=1
                    else:required_matrix[d,2,2]+=1    
                    cv2.putText(original, size+" "+str(color)+" rectangle", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
                continue    
            elif x == 5:
                cv2.putText(original, size+" " +str(color)+" pentagon", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
                continue
            elif x >= 6:
                if (area >= area_list[0]):
                    size = "large"
                    required_matrix[d,3,4]+=1
                elif (area <= area_list[1]):
                    size = "small"
                    required_matrix[d,1,4]+=1
                else:
                    required_matrix[d,2,4]+=1    
                cv2.putText(original, size+" "+str(color)+" circle", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
                continue

        shape_List=["","Triangle","Rectangle","Square","Circle"]
        size_List=["","Small","Medium","Large"]
        col_List=["","Red","Yellow","Orange","Green","Blue"]

        for colInd in xrange(1,6):
            for sizeInd in xrange(1,4):
                for shapeInd in xrange(1,5):
                    if(required_matrix[colInd][sizeInd][shapeInd]>0):
                        writecsv(col_List[colInd],shape_List[shapeInd],size_List[sizeInd],str(required_matrix[colInd][sizeInd][shapeInd])[:-2])
                        
        cv2.imwrite(os.getcwd()+"\output"+path[len(path)-5:],original)
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = ["\\".join([mypath, f]) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles[:]:
        #Open the csv to write in append mode
        filep = open('results1B_eYRC#509.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp[2:])
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        main(fp)
        #open the csv
        filep = open('results1B_eYRC#509.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
