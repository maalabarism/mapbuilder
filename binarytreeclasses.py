#from random import seed
#from random import randint

class Node:
    def __init__(self, data : str, string1 : str): #data is always coordinates ex. string "3,6", means row 3, col 6
        self.left = None
        self.right = None
        self.data = data
        self.string1 = string1
        self.colorMapList : list = []

    def insert(self, data2 : str, string2 : str): #data is always coordinates ex. string "3,6", means row 3, col 6
        if self.data == None:
            self.data = data2
            self.string = string2
        else:
            subStrList = data2.split(",")
            xRow2Insert = subStrList[0]
            yCol2Insert = subStrList[1]
            xRowInsertStr = xRow2Insert.strip()
            yColInsertStr = yCol2Insert.strip()
            xRowInsert = int(xRowInsertStr)
            yColInsert = int(yColInsertStr)

            selfDataStrList = self.data.split(",")
            xRow2 = selfDataStrList[0]
            yCol2 = selfDataStrList[1]
            xRowStr = xRow2.strip()
            yColStr = yCol2.strip()
            xRow = int(xRowStr)
            yCol = int(yColStr)

            if xRow == xRowInsert:
                if yColInsert > yCol:
                    if self.right == None:
                        self.right = Node(data2, string2)
                    else:
                        self.right.insert(data2, string2)
            elif xRowInsert > xRow:
                if self.left == None:
                    self.left = Node(data2, string2)
                else:
                    self.left.insert(data2, string2)

    def updateColorAtCoordinates(self, coordinates, color):
        subStrList = coordinates.split(",")
        xRow2Insert = subStrList[0]
        yCol2Insert = subStrList[1]
        xRowInsertStr = xRow2Insert.strip()
        yColInsertStr = yCol2Insert.strip()
        xRowInsert = int(xRowInsertStr) 
        yColInsert = int(yColInsertStr)

        selfDataStrList = self.data.split(",")
        xRow2 = selfDataStrList[0]
        yCol2 = selfDataStrList[1]
        xRowStr = xRow2.strip()
        yColStr = yCol2.strip()
        xRow = int(xRowStr)
        yCol = int(yColStr)

        if xRow == xRowInsert:
            if yColInsert == yCol:
                self.string1 = color
            elif yColInsert > yCol:
                self.right.updateColorAtCoordinates(coordinates, color)
        elif xRowInsert > xRow:
                self.left.updateColorAtCoordinates(coordinates, color)


    '''def performFillLogic(self, xPos2, yPos2, targetColor2, pxSizeIs0_2):
        selfDataStrList = self.data.split(",")
        xRow2 = selfDataStrList[0]
        yCol2 = selfDataStrList[1]
        xRowStr = xRow2.strip()
        yColStr = yCol2.strip()
        xRow = int(xRowStr)
        yCol = int(yColStr)

        if xPos2 == xRow:
            if yPos2 == yCol:
                self.performFillLogic2(self, xPos2, yPos2, targetColor2, pxSizeIs0_2)
            elif yPos2 > yCol:
                self.right.performFillLogic(self, xPos2, yPos2, targetColor2, pxSizeIs0_2)
        elif xPos2 > xRow:
            self.left.performFillLogic(self, xPos2, yPos2, targetColor2, pxSizeIs0_2)
    
    def performFillLogic2(self, xPos2, yPos2, targetColor2, pxSizeIs0_2):'''
        




'''if __name__ == "__main__":

    seed(1)

    for i in range(64):
        for j in range(32):
            str1 = str(i) + "," + str(j)
            print(str1)
            value = randint(0, 10)
            if i == 0 and j == 0:
                rootNode = Node(str1, str1)
            else:
                rootNode.insert(str1, str1)
    
    print("testing")
    print(rootNode.string1)
    print(rootNode.right.right.right.string1)
    print(rootNode.left.left.right.right.right.string1)'''

    #seems to be working so far c:


            


