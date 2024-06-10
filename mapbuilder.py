
import wx
import wx.lib.scrolledpanel as scrolled
#import wx.lib.inspection
import wx.lib.statbmp
import base64
from io import BytesIO
import os
import re
import math
from binarytreeclasses import Node
#from binarytree import Node
#import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#global variables:
doesStaticMapExist = False
doesStaticImgBlockExist = False
isConfigSet = False
isConfigSet2 = False
isSelectedImageSet = False
drawBool = False
#drawBool2 = False
isThereMap = False
isThereImgBlock = False
drawLineBool = False
destroyCreateBlockWindow = False
eraseBackground = False
leftColorTrue = False
notifySaveProjectForMap = False
notifySaveProjectForMap2 = False
notifySaveProjectForImgBlock = False
returnFromFrameClass = False
isProjectSaved = False
#globalBmp : wx.Bitmap = None

class windowClass(wx.Frame):

    def __init__(self, *args, **kwargs): #arguments and keyword arguments
        super(windowClass, self).__init__(*args, **kwargs)

        self.undo_list2 : list = []
        self.redo_list2 : list = []
        self.undo_list_index2 = 0
        self.redo_list_index2 = 0

        self.counter = 0
        self.counter2 = 0
        self.basicGUI()

    def basicGUI(self):
        #self.panel = wx.Panel(self)
        self.panel = TestPanel(self)    
        self.log1 = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(10, 0), size=(600,50), style = wx.TE_MULTILINE | wx.TE_READONLY)
        #ADD LOG2 TO BOX SIZER
        self.panel.addToBoxSizerHbox(self.log1)
        self.panel.setSizerAndScrolling()

        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        editButton = wx.Menu()
        helpButton = wx.Menu()

        openProjectItem = wx.MenuItem(fileButton, wx.ID_ANY, 'Open project\tCtrl+O')
        saveFileItem = wx.MenuItem(fileButton, wx.ID_SAVE, 'Save map\tCtrl+I')
        saveProjectItem = wx.MenuItem(fileButton, wx.ID_ANY, 'Save project\tCtrl+S')
        selectImageItem = wx.MenuItem(fileButton, wx.ID_FILE, 'Select image block\tCtrl+E')
        createImageItem = wx.MenuItem(fileButton, wx.ID_ANY, 'Create image block\tCtrl+B')
        configItem = wx.MenuItem(fileButton, wx.ID_ANY, 'New Project\tCtrl+N')
        exitItem = wx.MenuItem(fileButton, wx.ID_EXIT, 'Quit\tCtrl+Q')

        redoItem = wx.MenuItem(editButton, wx.ID_ANY, 'Redo\tCtrl+Y')
        undoItem = wx.MenuItem(editButton, wx.ID_ANY, 'Undo\tCtrl+Z')
        
        helpItem = wx.MenuItem(helpButton, wx.ID_ANY, 'Help')

        fileButton.Append(openProjectItem)
        fileButton.Append(saveFileItem)
        fileButton.Append(saveProjectItem)
        fileButton.Append(selectImageItem)
        fileButton.Append(createImageItem)
        fileButton.Append(configItem)
        fileButton.Append(exitItem)

        editButton.Append(redoItem)
        editButton.Append(undoItem)

        helpButton.Append(helpItem)

        menuBar.Append(fileButton, '&File')
        menuBar.Append(editButton, '&Edit')
        menuBar.Append(helpButton, '&Help')
        
        self.staticbitmap3 = wx.StaticBitmap(self.panel, pos=(10, 60))#this function has position, it is for selected image displayed.
        self.staticbitmap3.Hide()
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OpenProject, openProjectItem)
        self.Bind(wx.EVT_MENU, self.SaveFile, saveFileItem)
        self.Bind(wx.EVT_MENU, self.SaveProject, saveProjectItem)
        self.Bind(wx.EVT_MENU, self.SelectImageFile, selectImageItem)
        self.Bind(wx.EVT_MENU, self.CreateImageFile, createImageItem)
        self.Bind(wx.EVT_MENU, self.Config, configItem)
        self.Bind(wx.EVT_MENU, self.Quit, exitItem)
        self.Bind(wx.EVT_MENU, self.ShowHelp, helpItem)

        self.Bind(wx.EVT_MENU, self.editRedo, redoItem)
        self.Bind(wx.EVT_MENU, self.editUndo, undoItem)

        self.Bind(wx.EVT_CLOSE, self.Quit, self)
        #self.Bind(wx.EVT_WINDOW_DESTROY, self.Quit, self)
        
        self.SetTitle('Simple Map Builder')
        
        self.SetSize(wx.Size(1000, 1000))
        self.Centre()

        #icon = wx.Icon('C:\\Users\\change\\source\\Python\\mapbuilder\\MB_ICON.ico', wx.BITMAP_TYPE_ANY)
        icon = wx.Icon(resource_path('./MB_ICON.ico'), wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        self.Show(True)
        self.Maximize(True)
        
    def CreateImageFile(self, e):
        app2 = wx.App()
        windowCreateImgBlock(None)
        app2.MainLoop()

    def SelectImageFile(self, e):
        openFileDialog = wx.FileDialog(self, "Open PNG file", wildcard="PNG files (*.png)|*.png", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        pathname = openFileDialog.GetPath()
        self.SelectedImagePathName = pathname

        global isSelectedImageSet

        if isSelectedImageSet == False:
            self.log2 = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(620, 0), size=(190, 50), style = wx.TE_MULTILINE | wx.VSCROLL | wx.TE_READONLY)
            self.log2.AppendText("Selected image is: ")
            self.panel.addToBoxSizerHbox(self.log2)
            isSelectedImageSet = True

        if self.counter == 0:
            self.staticbitmap = wx.StaticBitmap(self.panel, pos=(820, 0))#this function has position, it is for selected image displayed.#used to be self, but is now self.panel
            self.staticbitmap.SetBitmap(wx.Bitmap(pathname))
        else:
            self.staticbitmap.SetBitmap(wx.Bitmap(pathname))
        
        global notifySaveProjectForMap2
        notifySaveProjectForMap2 = True
        
        #ADD staticbitmap TO BOX SIZER
        self.panel.addToBoxSizerHbox(self.staticbitmap)

        
        self.select_imageButton = wx.Button(self.panel, label="Select new image block", pos=(840,0))#pos=(240,240))
        self.Bind(wx.EVT_BUTTON, self.SelectImageFile, self.select_imageButton)
        
        self.panel.addToBoxSizerHbox(self.select_imageButton)

        self.panel.setupScrolling()

        self.counter += 1

        openFileDialog.Destroy()
        


    def OpenProject(self, e):
        openFileDialog = wx.FileDialog(self, "Open SMP file", wildcard="SMP files (*.smp)|*.smp", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        pathname = openFileDialog.GetPath()
        pathname2 = "C:\\Users\\change\\source\\Python\\mapbuilder\\test2.smp"
        
        image_file = open(pathname, "r")
        self.result_x_dir = image_file.readlines()[0]
        self.result_x_dir = self.result_x_dir.replace("\n", "")
        image_file.close()
        
        image_file = open(pathname, "r")
        self.result_y_dir = image_file.readlines()[1]
        self.result_y_dir = self.result_y_dir.replace("\n", "")
        image_file.close()

        image_file = open(pathname, "r")
        self.x_totalSize = image_file.readlines()[2]
        self.x_totalSize = self.x_totalSize.replace("\n", "")
        image_file.close()

        image_file = open(pathname, "r")
        self.y_totalSize = image_file.readlines()[3]
        self.y_totalSize = self.y_totalSize.replace("\n", "")
        image_file.close()

        print("pathname: " + pathname)
        image_file2 = open(pathname, "r")
        list1 = image_file2.readlines()
        list1_len = len(list1)
        image_file2.close()

        image_file2 = open(pathname, "r")
        listfinal = image_file2.readlines()[4:list1_len]
        image_file2.close()

        str1 : str = ""
        for x in listfinal:
                str1 += x

        fp = open(pathname2, "w")
        fp.write(str1)
        fp.close()

        fp2 = open(pathname2, "rb")
        decodedImgData = base64.b64decode(fp2.read())
        fp2.close()

        os.remove(pathname2)

        bio = BytesIO(decodedImgData)
        img = wx.Image(bio)
        
        if not img.IsOk():
            raise ValueError("this is a bad/corrupt image")

        bitmap = img.ConvertToBitmap()

        self.bitmapForMap = wx.Bitmap(width=int(self.x_totalSize), height=int(self.y_totalSize))

        dc = wx.MemoryDC(self.bitmapForMap)
        dc.DrawBitmap(bitmap, x=0, y=0)
        
        try:
            self.staticbitmap2.SetBitmap(self.bitmapForMap)
            self.staticbitmap2.Refresh()
        except:
            global doesStaticMapExist
            if doesStaticMapExist:
                self.staticbitmap2.Destroy()
                self.staticbitmap2 = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
            else:
                self.staticbitmap2 = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
                doesStaticMapExist = True
            
            self.staticbitmap2.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
            self.staticbitmap2.Bind(wx.EVT_MOUSE_EVENTS, self.mouse_events)
            self.staticbitmap2.Bind(wx.EVT_LEAVE_WINDOW, self.mouse_leaveWindow)
            self.staticbitmap2.Bind(wx.EVT_LEFT_UP, self.on_release)

            self.staticbitmap2.SetBitmap(self.bitmapForMap)
            self.staticbitmap2.Refresh()

            bmp = self.staticbitmap2.GetBitmap()
            self.staticbitmap3.SetBitmap(bmp)
            self.staticbitmap3.Refresh()
            self.undo_list2.append(self.staticbitmap3.GetBitmap())

        global isConfigSet
        if isConfigSet == False:
            self.panel.addToBoxSizerVbox(self.staticbitmap2)
            self.panel.setupScrolling()
            isConfigSet = True
        else:
            self.panel.vbox.Detach(self.staticbitmap2)
            self.panel.addToBoxSizerVbox(self.staticbitmap2)
            self.panel.setupScrolling()
        
        global isThereMap
        isThereMap = True
        

    def SaveFile(self, event):
        global isThereMap
        
        if isThereMap == False:
            print("error there is no active img block.")
            dlg = ErrorDialog(parent = self.panel, option=0)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            defaultpath = '.'
            
            openFileDialog = wx.FileDialog(self, message="Save file as...", defaultDir=defaultpath, wildcard="PNG files (*.png)|*.png")
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # save the current contents in the file
            pathname = openFileDialog.GetPath()
            savedImageBitmap : wx.Bitmap = self.staticbitmap2.GetBitmap()
            savedImage : wx.Image = savedImageBitmap.ConvertToImage()
            savedImage.SaveFile(pathname, type=wx.BITMAP_TYPE_PNG)
            openFileDialog.Destroy()

    def SaveProject(self, event):
        global isThereMap
        global isProjectSaved
        if isThereMap == False:
            print("error there is no active img block.")
            dlg = ErrorDialog(parent = self.panel, option=0)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            defaultpath = '.'

            openFileDialog = wx.FileDialog(self, message="Save project as...", defaultDir=defaultpath, wildcard="SMP files (*.smp)|*.smp", style=wx.FD_SAVE)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # save the current contents in the file
            pathname = openFileDialog.GetPath()
            savedImageBitmap : wx.Bitmap = self.staticbitmap2.GetBitmap()
            savedImage : wx.Image = savedImageBitmap.ConvertToImage()
            savedImage.SaveFile(pathname, type=wx.BITMAP_TYPE_PNG)
            
            with open(pathname, "rb") as image_file:
                data = base64.b64encode(image_file.read())

            #f = open("C:\\Users\\change\\source\\Python\\mapbuilder\\test.smp", "w")
            f = open(pathname, "w")
            str1 = str(self.result_x_dir) + "\n"
            str2 = str(self.result_y_dir) + "\n"
            str3 = str(self.x_totalSize) + "\n"
            str4 = str(self.y_totalSize) + "\n"
            f.write(str1)
            f.write(str2)
            f.write(str3)
            f.write(str4)
            datastr = data.decode("utf-8")
            f.write(datastr)
            
            #os.remove(pathname)
            isProjectSaved = True
            openFileDialog.Destroy()

    def Config(self, e):
        dlg = GetData(parent = self.panel)
        dlg.ShowModal()
        if dlg.result_x_dir:
            if dlg.isDataThere == True:
                self.log1.AppendText("x-dir(px): "+ dlg.result_x_dir + " y-dir(px): "+ dlg.result_y_dir +" x-dir total size(px): " 
                + dlg.x_totalSize + " y-dir total size(px): " + dlg.y_totalSize + "\n")
                self.result_x_dir = dlg.result_x_dir
                self.result_y_dir = dlg.result_y_dir
                self.x_totalSize = dlg.x_totalSize
                self.y_totalSize = dlg.y_totalSize
        
        if dlg.isDataThere:
            self.displayMap(self)
            bmp = self.staticbitmap2.GetBitmap()
            self.staticbitmap3.SetBitmap(bmp)
            self.staticbitmap3.Refresh()
            self.undo_list2.append(self.staticbitmap3.GetBitmap())
        
        #self.log2 = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(0, 60), size=(int(dlg.x_totalSize), int(dlg.y_totalSize)), style = wx.TE_MULTILINE | wx.VSCROLL)
        dlg.Destroy()

    def displayMap(self, e):
        self.xintervals = int((int(self.x_totalSize))/(int(self.result_x_dir)))
        self.yintervals = int((int(self.y_totalSize))/(int(self.result_y_dir)))
        print(f"xintervals: {self.xintervals} and yintervals: {self.yintervals}")
        self.map_2d_arr = [[0 for x in range(self.xintervals)] for y in range(self.yintervals)]
        print(self.map_2d_arr)
        
        self.bitmapForMap = wx.Bitmap(width=int(self.x_totalSize), height=int(self.y_totalSize))
        
        global doesStaticMapExist
        if doesStaticMapExist:
            self.staticbitmap2.Destroy()
            self.staticbitmap2 = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
        else:
            self.staticbitmap2 = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
            doesStaticMapExist = True
        
        self.staticbitmap2.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
        self.staticbitmap2.Bind(wx.EVT_MOUSE_EVENTS, self.mouse_events)
        self.staticbitmap2.Bind(wx.EVT_LEAVE_WINDOW, self.mouse_leaveWindow)
        self.staticbitmap2.Bind(wx.EVT_LEFT_UP, self.on_release)

        dc = wx.MemoryDC(self.bitmapForMap)
        dc.SetBrush(wx.Brush('#E5CCFF'))
        dc.DrawRectangle(0, 0, width=int(self.x_totalSize), height=int(self.y_totalSize))
        for x in range(self.xintervals):
            for y in range(self.yintervals):
                 dc.DrawRectangle((x*(int(self.result_x_dir))), (y*(int(self.result_y_dir))), width=int(self.result_x_dir), height=int(self.result_y_dir))
        self.staticbitmap2.SetBitmap(self.bitmapForMap)

        #ADD staticbitmap2 TO BOX SIZER
        global isConfigSet
        if isConfigSet == False:
            self.panel.addToBoxSizerVbox(self.staticbitmap2)
            self.panel.setupScrolling()
            isConfigSet = True
        else:
            self.panel.vbox.Detach(self.staticbitmap2)
            self.panel.addToBoxSizerVbox(self.staticbitmap2)
            self.panel.setupScrolling()

        self.staticbitmap2.Refresh()
        self.staticbitmap2.SetBitmap(self.bitmapForMap)
        self.staticbitmap2.Refresh()

        global isThereMap
        isThereMap = True

        
    def on_clic(self, event : wx.MouseEvent):
        global notifySaveProjectForMap
        if notifySaveProjectForMap2 == True:
            notifySaveProjectForMap = True
        x, y = event.GetPosition()
        print(f"hi x: {x} y: {y}\n")

        self.xintervals = int((int(self.x_totalSize))/(int(self.result_x_dir)))
        self.yintervals = int((int(self.y_totalSize))/(int(self.result_y_dir)))
        xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, 
                                           arg1=int(self.result_x_dir), arg2= int(self.result_y_dir))

        selectedImageFile = wx.Bitmap(self.SelectedImagePathName)
        print(self.SelectedImagePathName)
        dc = wx.MemoryDC(self.bitmapForMap)
        #dc.SetPen(wx.Pen("white",style=wx.TRANSPARENT))
        dc.SetPen(wx.Pen("white", style=wx.TRANSPARENT))
        dc.DrawRectangle(x=(xVal*int(self.result_x_dir)), y=(yVal*int(self.result_y_dir)), width=int(self.result_x_dir), height=int(self.result_y_dir))
        dc.DrawBitmap(selectedImageFile, x=(xVal*int(self.result_x_dir)), y=(yVal*int(self.result_y_dir)))
        self.staticbitmap2.SetBitmap(self.bitmapForMap)
        global drawBool
        drawBool = True
        event.Skip()


    def mouse_events(self, event : wx.MouseEvent):
        if drawBool == True:
            x, y = event.GetPosition()
            print(f"hi x: {x} y: {y}\n")

            self.xintervals = int((int(self.x_totalSize))/(int(self.result_x_dir)))
            self.yintervals = int((int(self.y_totalSize))/(int(self.result_y_dir)))

            xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, 
                                           arg1=int(self.result_x_dir), arg2= int(self.result_y_dir))

            selectedImageFile = wx.Bitmap(self.SelectedImagePathName)
            print(self.SelectedImagePathName)
            dc = wx.MemoryDC(self.bitmapForMap)
            #dc.SetPen(wx.Pen("white",style=wx.TRANSPARENT))
            dc.SetPen(wx.Pen("white", style=wx.TRANSPARENT))
            dc.DrawRectangle(x=(xVal*int(self.result_x_dir)), y=(yVal*int(self.result_y_dir)), width=int(self.result_x_dir), height=int(self.result_y_dir))
            dc.DrawBitmap(selectedImageFile, x=(xVal*int(self.result_x_dir)), y=(yVal*int(self.result_y_dir)))
            self.staticbitmap2.SetBitmap(self.bitmapForMap)

        event.Skip()

    def mouse_leaveWindow(self, event2 : wx.EVT_LEAVE_WINDOW):
        self.on_release(event=event2)

    def on_release(self, event : wx.MouseEvent):
        global drawBool
        print("herehere\n")
        #self.staticbitmap2.SetBitmap(self.bitmapForMap)
        self.staticbitmap2.Refresh()
        
        
        if drawBool:
            if len(self.redo_list2) > 0:
                self.redo_list2.clear()
            bmp = self.staticbitmap2.GetBitmap()
            self.staticbitmap3.SetBitmap(bmp)
            self.staticbitmap3.Refresh()
            self.undo_list2.append(self.staticbitmap3.GetBitmap())
            self.undo_list_index2 += 1
        
        drawBool = False
        event.Skip()
    
    def editRedo(self, e):
        if len(self.redo_list2) > 0:
            bmp = self.redo_list2.pop()

            self.undo_list2.append(bmp)
            self.undo_list_index2 += 1

            sizeNeeded : wx.Size = wx.Size(int(self.x_totalSize), int(self.y_totalSize))
            wx.Bitmap.Rescale(bmp, sizeNeeded)

            
            self.staticbitmap3.SetBitmap(bmp)
            self.staticbitmap3.Refresh()
            bmpbmp = self.staticbitmap3.GetBitmap()
            self.staticbitmap2.SetBitmap(bmpbmp)

            self.bitmapForMap = self.staticbitmap2.GetBitmap()

        print("editRedo")
    
    def editUndo(self, e):
        if len(self.undo_list2) > 1:
            removedItem = self.undo_list2.pop(self.undo_list_index2)

            self.redo_list2.append(removedItem)

            self.undo_list_index2 -= 1
            tempBmp : wx.Bitmap = self.undo_list2[self.undo_list_index2]

            sizeNeeded : wx.Size = wx.Size(int(self.x_totalSize), int(self.y_totalSize))
            
            wx.Bitmap.Rescale(tempBmp, sizeNeeded)

            print("editUndo")
            self.staticbitmap3.SetBitmap(tempBmp)
            self.staticbitmap3.Refresh()
            bmpbmp = self.staticbitmap3.GetBitmap()
            self.staticbitmap2.SetBitmap(bmpbmp)

            self.bitmapForMap = self.staticbitmap2.GetBitmap()

    def ShowHelp(self, e):
        dlg = ShowHelpDialog(parent = self.panel)
        dlg.ShowModal()
        dlg.Destroy()

    def Quit(self, e):
        global isProjectSaved
        global notifySaveProjectForMap
        if notifySaveProjectForMap == True and isProjectSaved == False:
            print("areyousure?\n")
            dialog = wx.MessageDialog(self, "Do you want to save project before quitting?", "Save Project Before Quitting", wx.YES_NO | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_INFORMATION)
            answer = dialog.ShowModal()
            dialog.Destroy()
            if answer == wx.ID_YES:
                # Do something for the "Yes" button press
                self.SaveProject(e)
                self.Destroy()
            elif answer == wx.ID_NO:
                # Do something for the "No" button press
                isProjectSaved = False
                self.Destroy()
                pass
            else:
                # Do nothing for the "Cancel" button press
                return
        notifySaveProjectForMap = False
        isProjectSaved = False
        self.Destroy()


class windowCreateImgBlock(wx.Frame):

    def __init__(self, *args, **kwargs): #arguments and keyword arguments
        super(windowCreateImgBlock, self).__init__(*args, **kwargs)

        defaultColor = wx.Colour()
        defaultColor2 = wx.Colour()
        defaultColor.Set("#33FFCB")
        defaultColor2.Set("#D329E3")
        global doesStaticImgBlockExist
        doesStaticImgBlockExist = False

        self.undo_list : list = []
        self.redo_list : list = []
        self.undo_list_index = 0
        self.redo_list_index = 0

        self.magnifyVal : int = 0 
        self.realMagnifyVal : int = 1
        self.magnifyValStr : str ="0" #magnifyVal str is 0 when strVal is 1

        self.selectedColor : wx.Colour = defaultColor
        self.selectedColorRight : wx.Colour = defaultColor2
        self.tempColor : wx.Colour = defaultColor
        self.tempColor2 : wx.Colour = defaultColor

        self.drawingMode : str = "" # possibilities are: Painting Mode and Matrix Mode
        self.drawingAction : str = "Draw" # possibilities are: fill, draw, line ,default is "Draw"

        self.pos1Line = None
        self.pos2Line = None

        self.basicGUI()
        
        '''if(self.drawingMode == "Painting Mode"): #Check drawing mode and init variables.
            self.staticbitmap.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
            self.staticbitmap.Bind(wx.EVT_RIGHT_DOWN, self.on_clic)
            self.staticbitmap.Bind(wx.EVT_MOUSE_EVENTS, self.mouse_events)
            self.staticbitmap.Bind(wx.EVT_LEAVE_WINDOW, self.mouse_leaveWindow)
            self.staticbitmap.Bind(wx.EVT_LEFT_UP, self.on_release)
            self.staticbitmap.Bind(wx.EVT_RIGHT_UP, self.on_release)
        else: #this is for matrix mode
            self.staticbitmap.Bind(wx.EVT_LEFT_DOWN, self.on_clicMatrix)
            self.staticbitmap.Bind(wx.EVT_RIGHT_DOWN, self.on_clicMatrix)
            self.staticbitmap.Bind(wx.EVT_MOUSE_EVENTS, self.mouse_eventsMatrix)
            self.staticbitmap.Bind(wx.EVT_LEAVE_WINDOW, self.mouse_leaveWindow)
            self.staticbitmap.Bind(wx.EVT_LEFT_UP, self.on_releaseMatrix)
            self.staticbitmap.Bind(wx.EVT_RIGHT_UP, self.on_releaseMatrix)'''
        
        self.magnifyInput = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(840, 0), size=(30,30), value=self.magnifyValStr)
        #self.magnifyInput2 = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(840, 0), size=(50,30), value=defaultMagnifySize2, style = wx.TE_MULTILINE | wx.TE_READONLY)

        self.panel.addToBoxSizerVHbox(self.magnifyInput)
        #self.panel.addToBoxSizerVHbox(self.magnifyInput2)
        self.panel.setupScrolling()

        ##############ADDING TWO BUTTONS WITH BITMAP IMGS inside a vertical boxsizer, then added to self.panel specified box sizer.###########
        self.bmpButton1 = wx.BitmapButton(self.panel, id=wx.ID_ANY, bitmap=wx.Bitmap(resource_path('./buttonup2.png')), pos=(0, 0), size=(32, 16))
        self.bmpButton2 = wx.BitmapButton(self.panel, id=wx.ID_ANY, bitmap=wx.Bitmap(resource_path('./buttondown.png')), pos=(0, 0), size=(32, 16))
        #self.bmpButton1 = wx.BitmapButton(self.panel, id=wx.ID_ANY, bitmap=wx.Bitmap('./buttonup2.png'), pos=(0, 0), size=(32, 16))
        #self.bmpButton2 = wx.BitmapButton(self.panel, id=wx.ID_ANY, bitmap=wx.Bitmap('./buttondown.png'), pos=(0, 0), size=(32, 16))
        self.Bind(wx.EVT_BUTTON, self.bmpButton1Func, self.bmpButton1)
        self.Bind(wx.EVT_BUTTON, self.bmpButton2Func, self.bmpButton2)
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)
        self.boxSizer.Add(self.bmpButton1)
        self.boxSizer.Add(self.bmpButton2)
        self.panel.addToBoxSizerVHbox(self.boxSizer)
        self.panel.setupScrolling()
        ############################################################
        
        self.drawingActionList = ["Draw", "Line", "Fill"]
        self.drawingActionRadioBox : wx.RadioBox = wx.RadioBox(self.panel, pos = (0,0), choices = self.drawingActionList, majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        self.Bind(wx.EVT_RADIOBOX, self.onDrawingActionChange, self.drawingActionRadioBox)
        self.panel.addToBoxSizerVHbox(self.drawingActionRadioBox)
        self.panel.setupScrolling()
        ##self.lineCheckBox = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Line", pos=(0, 0), style=0, name="lineCheckbox")
        #self.Bind(wx.EVT_CHECKBOX, self.onEraseCheckbox, self.eraseCheckbox)
        #self.panel.addToBoxSizerVHbox(self.lineCheckBox)
        #self.panel.setupScrolling()
        self.getDrawingModeDialog(self)
        global returnFromFrameClass
        if returnFromFrameClass == True:
            returnFromFrameClass = False
            return
        
        global destroyCreateBlockWindow
        if destroyCreateBlockWindow:
            #destroy window
            destroyCreateBlockWindow = False
            self.Destroy()
        else:
            #if(self.drawingMode == "Painting Mode"):
            self.getDialog2(self)
            if destroyCreateBlockWindow:
                #destroy window
                destroyCreateBlockWindow = False
                self.Destroy()
            '''else:
                #self.getDialog(self)
                self.getDialog2(self)
                if destroyCreateBlockWindow:
                    #destroy window
                    destroyCreateBlockWindow = False
                    self.Destroy()'''

        global isConfigSet2
        isConfigSet2 = True

        self.Show(True)
        self.Maximize(True)
        

    def basicGUI(self):
        #self.panel = wx.Panel(self)
        self.panel = TestPanel(self)
        self.log1 = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(10, 0), size=(600,50), style = wx.TE_MULTILINE | wx.TE_READONLY)
        #ADD LOG2 TO BOX SIZER
        self.panel.addToBoxSizerHbox(self.log1)
        self.panel.setSizerAndScrolling()
        
        #self.staticbitmap = wx.StaticBitmap(self.panel, pos=(10, 60))#this function has position, it is for selected image displayed.
        #self.staticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60))
        #self.genstaticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=-1, pos=(10, 60))

        self.tempStaticBitmap = wx.StaticBitmap(self.panel, pos=(10, 60))#this function has position, it is for selected image displayed.
        self.tempBitmap = wx.Bitmap()

        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        editButton = wx.Menu()

        saveImageItem = wx.MenuItem(fileButton, wx.ID_SAVE, 'Save image\tCtrl+I')
        saveBlockProject = wx.MenuItem(fileButton, wx.ID_ANY, 'Save create block project\tCtrl+S')
        openBlockProject = wx.MenuItem(fileButton, wx.ID_ANY, 'Open block project\tCtrl+O')
        exitItem = wx.MenuItem(fileButton, wx.ID_EXIT, 'Quit\tCtrl+Q')

        redoItem = wx.MenuItem(editButton, wx.ID_ANY, 'Redo\tCtrl+Y')
        undoItem = wx.MenuItem(editButton, wx.ID_ANY, 'Undo\tCtrl+Z')
        
        fileButton.Append(saveImageItem)
        fileButton.Append(saveBlockProject)
        fileButton.Append(openBlockProject)
        fileButton.Append(exitItem)

        editButton.Append(redoItem)
        editButton.Append(undoItem)

        menuBar.Append(fileButton, '&File')

        menuBar.Append(editButton, '&Edit')
        
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.SaveFile, saveImageItem)
        self.Bind(wx.EVT_MENU, self.SaveProject, saveBlockProject)
        self.Bind(wx.EVT_MENU, self.OpenProject, openBlockProject)
        self.Bind(wx.EVT_MENU, self.Quit, exitItem)
        self.Bind(wx.EVT_CLOSE, self.Quit, exitItem)

        self.Bind(wx.EVT_MENU, self.editRedo, redoItem)
        self.Bind(wx.EVT_MENU, self.editUndo, undoItem)

        #self.Bind(wx.EVT_WINDOW_DESTROY, self.Quit, self)
        self.Bind(wx.EVT_CLOSE, self.Quit, self)

        self.SetTitle('Create Image Block')
        
        self.SetSize(wx.Size(1000, 1000))
        self.Centre()

        #icon = wx.Icon('C:\\Users\\change\\source\\Python\\mapbuilder\\MB_ICON.ico', wx.BITMAP_TYPE_ANY)
        icon = wx.Icon(resource_path('./MB_ICON.ico'), wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        
        ######################################### ME TRYING TO ADD A BUTTON 
        self.select_colorButton = wx.Button(self.panel, label="Select color", pos=(840,0))#pos=(240,240))
        self.Bind(wx.EVT_BUTTON, self.SelectNewColour, self.select_colorButton)
        self.panel.addToBoxSizerHbox(self.select_colorButton)
        self.panel.setupScrolling()

        self.selectedColorsTxt = wx.StaticText(self.panel, label="Selected colors:", pos=(0,0))
        self.panel.addToBoxSizerHbox(self.selectedColorsTxt)
        self.panel.setupScrolling()

        
        colorBmpSize = wx.Size(20, 20)
        bmp1 = wx.Bitmap(sz=colorBmpSize)
        bmp2 = wx.Bitmap(sz=colorBmpSize)
        dc1 = wx.MemoryDC(bmp1)
        dc2 = wx.MemoryDC(bmp2)
        dc1.SetBrush(wx.Brush(self.selectedColor))
        dc1.DrawRectangle(0, 0, width=20, height=20)
        dc2.SetBrush(wx.Brush(self.selectedColorRight))
        dc2.DrawRectangle(0, 0, width=20, height=20)
        
        self.color1Bmp = wx.StaticBitmap(self.panel, id=wx.ID_ANY, bitmap=bmp1, pos=(0,0), size=colorBmpSize, style=0, name="leftclickcolorbmp")
        self.panel.addToBoxSizerHbox(self.color1Bmp)
        self.panel.setupScrolling()

        self.color2Bmp = wx.StaticBitmap(self.panel, id=wx.ID_ANY, bitmap=bmp2, pos=(0,0), size=colorBmpSize, style=0, name="rightclickcolorbmp")
        self.panel.addToBoxSizerHbox(self.color2Bmp)
        self.panel.setupScrolling()

        self.eraseCheckbox = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Erase", pos=(820, 0), style=0, name="eraseCheckbox")
        self.Bind(wx.EVT_CHECKBOX, self.onEraseCheckbox, self.eraseCheckbox)
        self.panel.addToBoxSizerHbox(self.eraseCheckbox)
        self.panel.setupScrolling()

        self.magnifyText = wx.StaticText(self.panel, label="Magnify(x2^n):", pos=(0,0))
        self.panel.setAddToBoxSizerVbox(self.magnifyText)
        self.panel.setupScrolling()
    
        '''self.changeMagnifyButton = wx.Button(self.panel, label="Change", pos=(0,0))#pos=(240,240))
        self.Bind(wx.EVT_BUTTON, self.onChangeMagnify, self.changeMagnifyButton)
        self.panel.addToBoxSizerVHbox(self.changeMagnifyButton)
        self.panel.setupScrolling()'''
        ##########################################

    def getDrawingModeDialog(self, e):
        dlg = GetModeData(parent = self.panel)
        dlg.ShowModal()
        global destroyCreateBlockWindow

        if destroyCreateBlockWindow == False:
            if hasattr(dlg, 'isDataThere'):
                if dlg.isDataThere == True:
                    self.drawingMode = dlg.drawingMode # 2 options: drawing mode or matrix mode.
                    print(self.drawingMode)
                else:
                    self.log1.AppendText("No input found\n")
               
    def getDialog2(self, e):
        dlg = GetData2(parent = self.panel)
        dlg.ShowModal()
        if dlg.isDataThere == True:
            self.log1.AppendText(" x-dir total size(px): " + dlg.x_totalSize + " y-dir total size(px): " + dlg.y_totalSize + "\n")
            self.x_totalSize = int(dlg.x_totalSize)
            self.y_totalSize = int(dlg.y_totalSize)

            if(self.drawingMode == "Painting Mode"):
                self.displayMap2(self)
                self.initGenStaticBitmapBindings(self)
                bmp = self.staticbitmap.GetBitmap()
                self.staticbitmap2.SetBitmap(bmp)
                self.staticbitmap2.Refresh()
                self.undo_list.append(self.staticbitmap2.GetBitmap())
                print("undo list1:\n")
                print(self.undo_list)
                dlg.Destroy()
            else:
                self.displayMapForMatrix(self)
                self.initGenStaticBitmapBindings(self)
                bmp = self.staticbitmap.GetBitmap()
                self.staticbitmap2.SetBitmap(bmp)
                self.staticbitmap2.Refresh()
                self.undo_list.append(self.staticbitmap2.GetBitmap())
                print("undo list1:\n")
                print(self.undo_list)
                dlg.Destroy()
            
        else:
            global destroyCreateBlockWindow
            destroyCreateBlockWindow = True
        
    def initGenStaticBitmapBindings(self, e):
        if(self.drawingMode == "Painting Mode"): #Check drawing mode and init variables.
            self.staticbitmap.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
            self.staticbitmap.Bind(wx.EVT_RIGHT_DOWN, self.on_clic)
            self.staticbitmap.Bind(wx.EVT_MOUSE_EVENTS, self.mouse_events)
            self.staticbitmap.Bind(wx.EVT_LEAVE_WINDOW, self.mouse_leaveWindow)
            self.staticbitmap.Bind(wx.EVT_LEFT_UP, self.on_release)
            self.staticbitmap.Bind(wx.EVT_RIGHT_UP, self.on_release)
            self.staticbitmap.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackGround)
        else: #this is for matrix mode
            self.staticbitmap.Bind(wx.EVT_LEFT_DOWN, self.on_clicMatrix)
            self.staticbitmap.Bind(wx.EVT_RIGHT_DOWN, self.on_clicMatrix)
            self.staticbitmap.Bind(wx.EVT_MOUSE_EVENTS, self.mouse_eventsMatrix)
            self.staticbitmap.Bind(wx.EVT_LEAVE_WINDOW, self.mouse_leaveWindow)
            self.staticbitmap.Bind(wx.EVT_LEFT_UP, self.on_releaseMatrix)
            self.staticbitmap.Bind(wx.EVT_RIGHT_UP, self.on_releaseMatrix)
            self.staticbitmap.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackGround)

    def onEraseBackGround(self, event : wx.EVT_ERASE_BACKGROUND):
        global eraseBackground
        if eraseBackground:
            print("erasingBackground!\n")
            eraseBackground = False

    def displayMap2(self, e): #This is for Painting Mode
        self.bitmapForMap = wx.Bitmap(width=int(self.x_totalSize), height=int(self.y_totalSize))
        dc = wx.MemoryDC(self.bitmapForMap)
        dc.SetBrush(wx.Brush('#FFFFFF'))
        dc.DrawRectangle(0, 0, width=int(self.x_totalSize), height=int(self.y_totalSize))

        self.colorMap2DArr = [['h' for x in range(int(self.y_totalSize))] for y in range(int(self.x_totalSize))]
        self.colorMap2DArrDrawModeandMagnNEW = [['h' for x in range(int(self.y_totalSize))] for y in range(int(self.x_totalSize))]
        self.colorMap2DArrDrawModeandMagnOLD = [['h' for x in range(int(self.y_totalSize))] for y in range(int(self.x_totalSize))]
        self.initColorMap2DArr(val1=int(self.x_totalSize), val2=int(self.y_totalSize), color="#FFFFFF")
        self.initColorMap2DArrDrawModeAndMagnify(val1=int(self.x_totalSize), val2=int(self.y_totalSize), color="#FFFFFF")

        self.rootNode = Node(data="0,0", string1="#FFFFFF")
        self.initColorMapBinTree(val1=int(self.x_totalSize), val2=int(self.y_totalSize), color="#FFFFFF")

        print(self.colorMap2DArr)
        print("1**1")

        global doesStaticImgBlockExist
        if doesStaticImgBlockExist:
            self.staticbitmap.Destroy()
            self.staticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
        else:
            self.staticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
            doesStaticImgBlockExist = True
        self.staticbitmap2 = wx.StaticBitmap(self.panel, pos=(10, 60))#this function has position, it is for selected image displayed.
        self.staticbitmap2.Hide()
        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap2.SetBitmap(self.bitmapForMap)

        #self.panel.addToBoxSizerVbox(self.staticbitmap)
        self.panel.addToBoxSizerVBoxCentre(self.staticbitmap)
        self.panel.setupScrolling()

        self.staticbitmap.Refresh()
        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap.Refresh()

        global isThereImgBlock
        isThereImgBlock = True

    def displayMapForMatrix(self, e):

        self.xintervals = int(self.x_totalSize)
        self.yintervals = int(self.y_totalSize)
        print(f"self.xintervals: {self.xintervals} self.yintervals: {self.yintervals}\n")

        self.colorMap2DArr = [['h' for x in range(self.yintervals)] for y in range(self.xintervals)]
        #self.initColorMap2DArr(val1=self.xintervals, val2=self.yintervals, color="#E5CCFF")
        self.initColorMap2DArr(val1=int(self.xintervals), val2=int(self.yintervals), color="#E5CCFF")

        self.rootNode = Node(data="0,0", string1="#E5CCFF")
        self.initColorMapBinTree(val1=int(self.xintervals), val2=int(self.yintervals), color="#E5CCFF")

        
        print("after func: ")
        print(self.colorMap2DArr)
        print("2**2")

        print(f"xintervals: {self.xintervals} and yintervals: {self.yintervals}")
        self.map_2d_arr = [[0 for x in range(self.xintervals)] for y in range(self.yintervals)]
        print(self.map_2d_arr)
        
        pxSize : int = int(self.magnifyVal)
        if pxSize == 0:
            pxSize += 1

        initialWidth : int =  int(self.x_totalSize) * pxSize
        initialHeight : int = int(self.y_totalSize) * pxSize

        self.bitmapForMap = wx.Bitmap(width=initialWidth, height=initialHeight)
        dc = wx.MemoryDC(self.bitmapForMap)
        dc.SetBrush(wx.Brush('#E5CCFF'))
        dc.DrawRectangle(0, 0, width=initialWidth, height=initialHeight)
        for x in range(self.xintervals):
            for y in range(self.yintervals):
                 dc.DrawRectangle(x * pxSize, y * pxSize, width = pxSize, height = pxSize)
        
        global doesStaticImgBlockExist
        if doesStaticImgBlockExist:
            self.staticbitmap.Destroy()
            self.staticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
        else:
            self.staticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=self.bitmapForMap)
            doesStaticImgBlockExist = True
        self.staticbitmap2 = wx.StaticBitmap(self.panel, pos=(10, 60))#this function has position, it is for selected image displayed.
        self.staticbitmap2.Hide()
        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap2.SetBitmap(self.bitmapForMap)

        #self.panel.vbox.Detach(self.staticbitmap2)
        #self.panel.addToBoxSizerVbox(self.staticbitmap)
        self.panel.addToBoxSizerVBoxCentre(self.staticbitmap)
        self.panel.setupScrolling()

        self.staticbitmap.Refresh()
        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap.Refresh()

        global isThereImgBlock
        isThereImgBlock = True

    def SaveFile(self, event):
        global isThereImgBlock
        
        if isThereImgBlock == False:
            print("error there is no active img block.")
            dlg = ErrorDialog(parent = self.panel, option=3)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            defaultpath = '.'
            
            openFileDialog = wx.FileDialog(self, message="Save file as...", defaultDir=defaultpath, wildcard="PNG files (*.png)|*.png")
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # save the current contents in the file
            #if self.magnifyVal > 1 then must rescale to x1 and then save file as png, for both drawing modes.

            pathname = openFileDialog.GetPath()
            savedImageBitmap : wx.Bitmap = self.staticbitmap.GetBitmap()

            sizeNeeded : wx.Size = wx.Size(int(self.x_totalSize), int(self.y_totalSize))

            wx.Bitmap.Rescale(savedImageBitmap, sizeNeeded)
            #image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)

            savedImage : wx.Image = savedImageBitmap.ConvertToImage()
            
            savedImage.SaveFile(pathname, type=wx.BITMAP_TYPE_PNG)
            openFileDialog.Destroy()

    def SaveProject(self, event):
        global isThereImgBlock
        global isProjectSaved
        if isThereImgBlock == False:
            print("error there is no active img block.")
            dlg = ErrorDialog(parent = self.panel, option=3)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            defaultpath = '.'

            openFileDialog = wx.FileDialog(self, message="Save project as...", defaultDir=defaultpath, wildcard="SMB files (*.smb)|*.smb", style=wx.FD_SAVE)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # save the current contents in the file
            pathname = openFileDialog.GetPath()
            savedImageBitmap : wx.Bitmap = self.staticbitmap.GetBitmap()
        
            #############################################################################################NEWSTUFF
            sizeNeeded : wx.Size = wx.Size(int(self.x_totalSize), int(self.y_totalSize))
            wx.Bitmap.Rescale(savedImageBitmap, sizeNeeded)
            #############################################################################################

            savedImage : wx.Image = savedImageBitmap.ConvertToImage()
            savedImage.SaveFile(pathname, type=wx.BITMAP_TYPE_PNG)

            with open(pathname, "rb") as image_file:
                data = base64.b64encode(image_file.read())

            f = open(pathname, "w")
            str1 = str(self.x_totalSize) + "\n"
            str2 = str(self.y_totalSize) + "\n"
            f.write(str1)
            f.write(str2)
            datastr = data.decode("utf-8")
            f.write(datastr)
            
            isProjectSaved = True
            openFileDialog.Destroy()

    def OpenProject(self, e):
            openFileDialog = wx.FileDialog(self, "Open SMB file", wildcard="SMB files (*.smb)|*.smb", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = openFileDialog.GetPath()
            pathname2 = "C:\\Users\\change\\source\\Python\\mapbuilder\\test2.smp"

            #if self.drawingMode == "Painting Mode":
            image_file = open(pathname, "r")
            self.x_totalSize = image_file.readlines()[0]
            self.x_totalSize = self.x_totalSize.replace("\n", "")
            image_file.close()

            image_file = open(pathname, "r")
            self.y_totalSize = image_file.readlines()[1]
            self.y_totalSize = self.y_totalSize.replace("\n", "")
            image_file.close()

            print("pathname: " + pathname)
            image_file2 = open(pathname, "r")
            list1 = image_file2.readlines()
            list1_len = len(list1)
            image_file2.close()

            image_file2 = open(pathname, "r")
            listfinal = image_file2.readlines()[2:list1_len]
            image_file2.close()

            str1 : str = ""
            for x in listfinal:
                    str1 += x

            fp = open(pathname2, "w")
            fp.write(str1)
            fp.close()

            fp2 = open(pathname2, "rb")
            decodedImgData = base64.b64decode(fp2.read())
            fp2.close()

            os.remove(pathname2)

            bio = BytesIO(decodedImgData)
            img = wx.Image(bio)
            
            if not img.IsOk():
                raise ValueError("this is a bad/corrupt image")

            bitmap = img.ConvertToBitmap()

            self.bitmapForMap = wx.Bitmap(width=int(self.x_totalSize), height=int(self.y_totalSize))
            dc = wx.MemoryDC(self.bitmapForMap)
            dc.DrawBitmap(bitmap, x=0, y=0)
            
            self.staticbitmap.SetBitmap(self.bitmapForMap)
            self.staticbitmap.Refresh()
            ###############################ADD STUFF FOR RESETTING MAGNIFY
            self.magnifyVal = 0
            self.realMagnifyVal = 2 ** self.magnifyVal
            self.magnifyInput.Clear()
            self.magnifyInput.AppendText(str(self.magnifyVal))
            #self.onChangeMagnify()

            global isConfigSet2
            if isConfigSet2 == False:
                self.panel.addToBoxSizerVbox(self.staticbitmap)
                self.panel.setupScrolling()
                isConfigSet2 = True
            else:
                self.panel.vbox.Detach(self.staticbitmap)
                self.panel.addToBoxSizerVbox(self.staticbitmap)
                self.panel.setupScrolling()
            
            global isThereImgBlock
            isThereImgBlock = True

    # Some function for redrawing using the given colour. Ideally, it
    # shouldn't do anything if the colour is the same as the one used
    # before.
    #def Redraw(self, colour):
        #self.log1.AppendText("redraw")

    def OnColourChanged(self, event : wx.EVT_COLOUR_CHANGED):
        self.tempColor : wx.Colour = event.GetColour() #is of wx.Colour type
        str1 = "Selected color: " + self.tempColor.GetAsString(flags=wx.C2S_CSS_SYNTAX)
        self.log1.Clear()
        self.log1.AppendText(str1)

    def SelectNewColour(self, e):
        data = wx.ColourData()
        color1 = wx.Colour()
        color1.Set("#33FFCB")
        data.SetColour(color1)
        dlg = wx.ColourDialog(self, data)
        dlg.Center()
        dlg.Show()
        dlg.Bind(wx.EVT_COLOUR_CHANGED, self.OnColourChanged)
        if (dlg.ShowModal() == wx.ID_OK):
            #color : wx.Colour = data.GetColour() #is of wx.Colour type
            self.selectedColorRight = self.selectedColor
            self.selectedColor = self.tempColor

            colorBmpSize = wx.Size(20, 20)
            bmp1 = wx.Bitmap(sz=colorBmpSize)
            bmp2 = wx.Bitmap(sz=colorBmpSize)
            dc1 = wx.MemoryDC(bmp1)
            dc2 = wx.MemoryDC(bmp2)
            dc1.SetBrush(wx.Brush(self.selectedColor))
            dc1.DrawRectangle(0, 0, width=20, height=20)
            dc2.SetBrush(wx.Brush(self.selectedColorRight))
            dc2.DrawRectangle(0, 0, width=20, height=20)
            self.color1Bmp.SetBitmap(bmp1)
            self.color2Bmp.SetBitmap(bmp2)
            self.color1Bmp.Refresh()
            self.color2Bmp.Refresh()
            # Colour did change.
        else:
            self.log1.Clear()
            self.log1.AppendText("\nNo color change.")
            self.tempColor = color1
            # Colour didn't change.

        # This call is unnecessary under platforms generating
        # wx.EVT_COLOUR_CHANGED if the dialog was accepted and unnecessary
        # under the platforms not generating this event if it was cancelled,
        # so we could check for the different cases explicitly to avoid it,
        # but it's simpler to just always call it.
        #self.Redraw(data.GetColour())

    def on_clic(self, event : wx.MouseEvent):
        global notifySaveProjectForImgBlock
        notifySaveProjectForImgBlock = True
        global isProjectSaved
        isProjectSaved = False

        x, y = event.GetPosition()
        print(f"hi2 x: {x} y: {y}\n")
        selectedColor = self.getColorLeftRightClick(evt=event)
        selectedColorStr = selectedColor.GetAsString(flags=wx.C2S_HTML_SYNTAX)
        pxSize2 = self.realMagnifyVal
        
        dc = wx.MemoryDC(self.bitmapForMap)
        if(self.magnifyVal > 0):
        #For when self.MagnifyVal > 1, then need to draw a rectangle which would be the same as a point for a rescaled bitmap.
            match self.drawingAction:
                case "Fill":
                    #xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2= pxSize2)
                    self.performFill_flood_fill(xPos=x, yPos=y, targetColor=selectedColorStr, pxSizeIs0=False, isDrawingModeAndMagnified=True)
                case _:
                    width2 = self.realMagnifyVal
                    height2 = self.realMagnifyVal
                    #dc.SetBrush(wx.Brush('#FFFFFF'))
                    dc.SetBrush(wx.Brush(selectedColor))
                    dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                    dc.DrawRectangle(x, y, width2, height2)
        else:
            match self.drawingAction:
                case "Fill":
                    self.performFill_flood_fill(xPos=x, yPos=y, targetColor=selectedColorStr, pxSizeIs0=True, isDrawingModeAndMagnified=False)
                case _:
                    dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                    point = wx.Point(x, y)
                    dc.DrawPoint(point)
                    self.updateColorMap2DArr(val1=x, val2=y, color=selectedColorStr)
                    self.initColorMap2DArrDrawModeandMagnOLD(val1=x, val2=y, color=selectedColorStr)
                    self.updateColorMapBinTree(val1=x, val2=y, color2=selectedColorStr)

        
        dc.SelectObject(wx.NullBitmap)
        #dc = wx.MemoryDC(self.bitmapForMap)
        #dc.SetPen(wx.Pen(self.selectedColor, style=wx.PENSTYLE_SOLID))
        #dc = wx.PaintDC(self)
        #dc.DrawBitmap(self.bitmapForMap, wx.Point(x, y))
        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap.Refresh()

        global drawBool
        drawBool = True
        event.Skip()

    def mouse_events(self, event : wx.MouseEvent):
        '''x2, y2 = event.GetPosition()
        self.log1.Clear()
        self.log1.AppendText(f"x:{x2} y:{y2}\n")'''
        global leftColorTrue
        if leftColorTrue == True:
            selectedColor = self.selectedColor
        else:
            selectedColor = self.selectedColorRight

        if drawBool == True:
            x, y = event.GetPosition()
            print(f"hi2 x: {x} y: {y}\n")
            
            dc = wx.MemoryDC(self.bitmapForMap)
            if(self.magnifyVal > 0):
            #For when self.MagnifyVal > 1, then need to draw a rectangle which would be the same as a point for a rescaled bitmap.
                width2 = self.realMagnifyVal
                height2 = self.realMagnifyVal
                #dc.SetBrush(wx.Brush('#FFFFFF'))
                dc.SetBrush(wx.Brush(selectedColor))
                dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                dc.DrawRectangle(x, y, width2, height2)
            else:
                dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                point = wx.Point(x, y)
                dc.DrawPoint(point)
                self.updateColorMap2DArr(val1=x, val2=y, color=selectedColor)
                self.updateColorMapBinTree(val1=x, val2=y, color2=selectedColor)
            
            dc.SelectObject(wx.NullBitmap)
            #dc.SetPen(wx.Pen(self.selectedColor, style=wx.PENSTYLE_SOLID))
            #dc.DrawBitmap(self.bitmapForMap, wx.Point(x, y))
            self.staticbitmap.SetBitmap(self.bitmapForMap)

        event.Skip()

    def on_release(self, event : wx.MouseEvent):
        '''global drawBool2
        drawBool2 = False
        print("herehere2\n")
        self.staticbitmap.Refresh()
        event.Skip()'''
        self.onReleaseFunc(event2=event, option=0)

    def on_clicMatrix(self, event : wx.MouseEvent):
        global notifySaveProjectForImgBlock
        notifySaveProjectForImgBlock = True
        global isProjectSaved
        isProjectSaved = False

        selectedColor = self.getColorLeftRightClick(evt=event)
        selectedColorStr = selectedColor.GetAsString(flags=wx.C2S_HTML_SYNTAX)
        x, y = event.GetPosition()
        
        dc = wx.MemoryDC(self.bitmapForMap)

        print(f"hi x: {x} y: {y} two\n")
        #pxSize : int = self.matrixModePxSize
        pxSize : int = self.magnifyVal
        pxSize2 : int = self.realMagnifyVal

        if pxSize == 0:
            dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
            match self.drawingAction:
                case "Draw":
                    print(f"draw1 ({x}, {y})\n")
                    point = wx.Point(x, y)
                    dc.DrawPoint(point)
                    self.updateColorMap2DArr(val1=x, val2=y, color=selectedColorStr)
                    self.updateColorMapBinTree(val1=x, val2=y, color2=selectedColorStr)
                    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH") #this is for testing 
                    print(self.rootNode.data)
                    print(self.rootNode.string1)
                    print(self.rootNode.right.data)
                    print(self.rootNode.right.string1)
                    print(self.rootNode.left.data)
                    print(self.rootNode.left.string1)
                    print("draw\n")
                case "Line":
                    print("line\n")
                case "Fill":
                    print("fill\n")
                    self.performFill_flood_fill(xPos=x, yPos=y, targetColor=selectedColorStr, pxSizeIs0=True, isDrawingModeAndMagnified=False)
                    print("performfillfinished")
                    '''self.performFillForMatrix(xPos=x, yPos=y, targetColor=selectedColorStr, pxSizeIs0=True)'''
        else:
            match self.drawingAction:
                case "Draw":
                    self.xintervals = int(self.x_totalSize)
                    self.yintervals = int(self.y_totalSize)

                    xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2= pxSize2)

                    dc.SetBrush(wx.Brush(selectedColor))
                    dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                    dc.DrawRectangle(x=(xVal*pxSize2), y=(yVal*pxSize2), width=pxSize2, height=pxSize2)
                    print(f"xVal:{xVal}, yVal:{yVal})\n")
                    self.updateColorMap2DArr(val1=xVal, val2=yVal, color=selectedColorStr)
                    self.updateColorMapBinTree(val1=xVal, val2=yVal, color2=selectedColorStr)
                    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH") #this is for testing 
                    print(self.rootNode.data)
                    print(self.rootNode.string1)
                    print(self.rootNode.right.data)
                    print(self.rootNode.right.string1)
                    print(self.rootNode.left.data)
                    print(self.rootNode.left.string1)

                    val1 = (xVal*pxSize2)
                    val2 = (yVal*pxSize2)
                    print(f"draw rect ({val1}, {val2})\n")
                case "Line":
                    print("line\n")
                case "Fill":
                    print("fill\n")
                    xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2= pxSize2)
                    self.performFill_flood_fill(xPos=xVal, yPos=yVal, targetColor=selectedColorStr, pxSizeIs0=False, isDrawingModeAndMagnified=False)
                    print("performfillfinished2")
                    '''self.xintervals = int(self.x_totalSize)
                    self.yintervals = int(self.y_totalSize)
                    xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2= pxSize2)
                    self.performFillForMatrix(xPos=xVal, yPos=yVal, targetColor=selectedColorStr, pxSizeIs0=False)'''
        
        dc.SelectObject(wx.NullBitmap)
            
        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap.Refresh()
        global drawBool
        drawBool = True
        event.Skip()


    def mouse_eventsMatrix(self, event : wx.MouseEvent):
        '''x2, y2 = event.GetPosition()
        self.log1.Clear()
        self.log1.AppendText(f"x:{x2} y:{y2}\n")'''
        global leftColorTrue
        if leftColorTrue == True:
            selectedColor = self.selectedColor
        else:
            selectedColor = self.selectedColorRight

        selectedColorStr = selectedColor.GetAsString(flags=wx.C2S_HTML_SYNTAX)

        if drawBool == True:
            x, y = event.GetPosition()
            print(f"hi x: {x} y: {y}\n")

            self.xintervals = int(self.x_totalSize)
            self.yintervals = int(self.y_totalSize)

            pxSize : int = self.magnifyVal
            pxSize2 : int = self.realMagnifyVal
            #pxSize : int = self.matrixModePxSize

            dc = wx.MemoryDC(self.bitmapForMap)


            if pxSize == 0:
                dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                match self.drawingAction:
                    case "Draw":
                        point = wx.Point(x, y)
                        dc.DrawPoint(point)
                        self.updateColorMap2DArr(val1=x, val2=y, color=selectedColorStr)
                        self.updateColorMapBinTree(val1=x, val2=y, color2=selectedColorStr)
                        print("draw2\n")
                    case "Line":
                        print("line2\n")
                    case "Fill":
                        print("fill2\n")
            else:
                match self.drawingAction:
                    case "Draw":
                        xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2= pxSize2)
                        dc.SetBrush(wx.Brush(selectedColor))
                        dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                        dc.DrawRectangle(x=(xVal*pxSize2), y=(yVal*pxSize2), width=pxSize2, height=pxSize2)
                        self.updateColorMap2DArr(val1=xVal, val2=yVal, color=selectedColorStr)
                        self.updateColorMapBinTree(val1=xVal, val2=yVal, color2=selectedColorStr)
                        print(f"xVal:{xVal}, yVal:{yVal})\n")
                        print("draw2\n")
                    case "Line":
                        print("line2\n")
                    case "Fill":
                        print("fill2\n")      
            dc.SelectObject(wx.NullBitmap)
            
            self.staticbitmap.SetBitmap(self.bitmapForMap)
            self.staticbitmap.Refresh()
        event.Skip()

    def on_releaseMatrix(self, event : wx.MouseEvent):
        self.onReleaseFunc(event2=event, option=1)
        print("resultingmap:\n")
        print(self.colorMap2DArr)
        print("release")

    def mouse_leaveWindow(self, event : wx.EVT_LEAVE_WINDOW):
        global drawBool

        global leftColorTrue
        leftColorTrue = False

        if drawBool:
            if len(self.redo_list) > 0:
                self.redo_list.clear()

            bmp = self.staticbitmap.GetBitmap()
            self.staticbitmap2.SetBitmap(bmp)
            self.staticbitmap2.Refresh()
            self.undo_list.append(self.staticbitmap2.GetBitmap())
            self.undo_list_index += 1

            print(self.undo_list)
            print(self.undo_list_index)
        
        drawBool = False

        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap2.SetBitmap(self.bitmapForMap)
        self.staticbitmap.Refresh()
        self.staticbitmap2.Refresh()
        event.Skip()

        print("out of bounds!")

    def onEraseCheckbox(self, event : wx.EVT_CHECKBOX):
        if event.IsChecked():
            print("hi1")
            self.tempColor2 = self.selectedColor
            color1 = wx.Colour()
            color1.Set("#FFFFFF")
            self.selectedColor = color1
        else:
            print("hi2")
            self.selectedColor = self.tempColor2
    
    def bmpButton1Func(self, event : wx.EVT_BUTTON):#this is for magnify up
        print("here1")
        
        self.magnifyVal += 1
        self.realMagnifyVal = 2 ** self.magnifyVal
        self.magnifyInput.Clear()
        self.magnifyInput.AppendText(str(self.magnifyVal))
        
        print(self.magnifyVal)
        print(self.realMagnifyVal)
        
        #self.updateDrawModeMagnified2DColorMap(magnifiedUp=True)
        self.onChangeMagnify()
        if self.drawingMode == "Painting Mode":
                self.updateDrawModeMagnified2DColorMap(magnifiedUp=True)

    def bmpButton2Func(self, event : wx.EVT_BUTTON):#this is for magnify down
        print("here2")
        
        if self.magnifyVal > 0:
            self.magnifyVal -= 1
            self.realMagnifyVal = 2 ** self.magnifyVal
            self.magnifyInput.Clear()
            self.magnifyInput.AppendText(str(self.magnifyVal))
            #self.updateDrawModeMagnified2DColorMap(magnifiedUp=False)

        print(self.magnifyVal)
        print(self.realMagnifyVal)

        self.onChangeMagnify()
        if self.magnifyVal > 0:
            if self.drawingMode == "Painting Mode":
                self.updateDrawModeMagnified2DColorMap(magnifiedUp=False)

    def onChangeMagnify(self):
        #self.magnifyVal = self.magnifyInput.GetValue()
        print(self.magnifyVal)

        tempBitmap2 : wx.Bitmap = self.staticbitmap.GetBitmap()

        str1 = "val1: " + str(self.realMagnifyVal * int(self.x_totalSize)) + " val2: " + str(self.realMagnifyVal * int(self.y_totalSize))
        print(str1)
        sizeNeeded : wx.Size = wx.Size(self.realMagnifyVal * int(self.x_totalSize), self.realMagnifyVal * int(self.y_totalSize))

        wx.Bitmap.Rescale(tempBitmap2, sizeNeeded)

        self.staticbitmap.SetBitmap(tempBitmap2)
        self.staticbitmap2.SetBitmap(tempBitmap2)
        self.bitmapForMap = tempBitmap2
        self.staticbitmap.Refresh()
        self.staticbitmap2.Refresh()
        self.panel.SetupScrolling()

        #if self.drawingMode == "Matrix Mode":
            #self.matrixModePxSize = int(self.magnifyInput.GetValue())
    
    def onDrawingActionChange(self, event : wx.EVT_RADIOBUTTON): 
        index1 : int = self.drawingActionRadioBox.GetSelection()
        tempResult: str = self.drawingActionList[index1]
        self.drawingAction = tempResult
        print(tempResult)

    def onReleaseFunc(self, event2 : wx.MouseEvent, option : int): #option == 1 is matrix, option == 0 is drawing mode
        selectedColor = self.getColorLeftRightClick(evt=event2)
        global drawBool
        match self.drawingAction:
            case "Draw":
                print("draw3\n")
            case "Line":
                global drawLineBool
                if drawLineBool == False:
                    pxSize : int = self.magnifyVal
                    if pxSize == 0:
                        self.pos1Line = event2.GetPosition()
                        x, y = event2.GetPosition()
                        dc = wx.MemoryDC(self.bitmapForMap)
                        dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                        point = wx.Point(x, y)
                        dc.DrawPoint(point)
                        dc.SelectObject(wx.NullBitmap)
                    else:
                        self.pos1Line = event2.GetPosition()
                        self.xintervals = int(self.x_totalSize)
                        self.yintervals = int(self.y_totalSize)
                        x, y = event2.GetPosition()
                        pxSize2 : int = self.realMagnifyVal
                        dc = wx.MemoryDC(self.bitmapForMap)

                        xVal, yVal = getCoordinatesFromBmp(x1=x, y1=y, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2=pxSize2)

                        dc.SetBrush(wx.Brush(selectedColor))
                        dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                        dc.DrawRectangle(x=(xVal*pxSize2), y=(yVal*pxSize2), width=pxSize2, height=pxSize2)
                        dc.SelectObject(wx.NullBitmap)
                        '''self.pos1Line = event2.GetPosition()
                        x, y = event2.GetPosition()
                        dc = wx.MemoryDC(self.bitmapForMap)
                        dc.SetPen(wx.Pen(self.selectedColor, style=wx.PENSTYLE_SOLID))
                        point = wx.Point(x, y)
                        dc.DrawPoint(point)'''
                    drawLineBool = True
                else:
                    pxSize : int = self.magnifyVal
                    if pxSize == 0:
                        self.pos2Line = event2.GetPosition()
                        dc = wx.MemoryDC(self.bitmapForMap)
                        dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
                        dc.DrawLine(self.pos1Line[0], self.pos1Line[1], self.pos2Line[0], self.pos2Line[1])
                        dc.SelectObject(wx.NullBitmap)
                    else:
                        self.pos2Line = event2.GetPosition()
                        self.DrawLineForMagnifiedBmp(pos1=self.pos1Line, pos2=self.pos2Line, option2=option)
                    drawLineBool = False
                
                self.staticbitmap.SetBitmap(self.bitmapForMap)
                self.staticbitmap2.SetBitmap(self.bitmapForMap)
                print("line3\n")
            case "Fill":
                '''pxSize : int = self.magnifyVal
                if pxSize == 0:
                    x, y = event2.GetPosition()
                    self.performFill_flood_fill(xPos=x, yPos=y, targetColor=selectedColor, pxSizeIs0=True)'''
                print("fill3\n")
        
        global leftColorTrue
        leftColorTrue = False

        if len(self.redo_list) > 0:
            self.redo_list.clear()

        bmp = self.staticbitmap.GetBitmap()
        self.staticbitmap2.SetBitmap(bmp)
        self.staticbitmap2.Refresh()
        self.undo_list.append(self.staticbitmap2.GetBitmap())
        self.undo_list_index += 1

        print(self.undo_list)
        print(self.undo_list_index)

        drawBool = False
        print("herehere\n")
        self.staticbitmap.SetBitmap(self.bitmapForMap)
        self.staticbitmap2.SetBitmap(self.bitmapForMap)
        self.staticbitmap.Refresh()
        self.staticbitmap2.Refresh()
        event2.Skip()

    def DrawLineForMagnifiedBmp(self, pos1, pos2, option2):
        print("pos1: " + str(pos1[0]) + " " + str(pos1[1]) + " pos2: " + str(pos2[0]) + " " + str(pos2[1]) + "\n")
        diffArr  = [0] * 2
        diffArrAbs = [0] * 2
        slopeArr  = [0] * 2
        diffArr[0] = pos2[0] - pos1[0]
        diffArr[1] = pos2[1] - pos1[1]
        diffArrAbs[0] = abs(diffArr[0])
        diffArrAbs[1] = abs(diffArr[1])
        slopeArr[0] = pos2[0] / pos1[0]
        slopeArr[1] = pos2[1] / pos1[1]
        if diffArr[0] == 0:
            diffArr[0] = 1
        if diffArr[1] == 0:
            diffArr[1] = 1
        ySlope = diffArr[1] / diffArr[0] #slope = rise/run
        xSlope = diffArr[0] / diffArr[1] #slope = run/rise
        print("diffArr:\n")
        print(diffArr)
        print("diffArr[0]: " + str(diffArr[0]) + "\n")
        print("diffArr[1]: " + str(diffArr[1]) + "\n")
        print("slopeArr:\n")
        print(slopeArr)
        print("xSlope:\n")
        print(xSlope)
        print("ySlope:\n")
        print(ySlope)
        
        xvalue2 = pos1[0]
        xvalue3 = pos2[0]
        yvalue2 = pos1[1]
        yvalue3 = pos2[1]
        pxSize : int = self.realMagnifyVal
        self.xintervals = int(self.x_totalSize)
        self.yintervals = int(self.y_totalSize)

        if diffArr[0] > 0 and  diffArr[1] > 0:
            if diffArrAbs[0] > diffArrAbs[1]:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos1[0], pos_2=pos2[0], slope=ySlope, pxSize2=pxSize, value2=yvalue2, option=0, option3=option2)
            else:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos1[1], pos_2=pos2[1], slope=xSlope, pxSize2=pxSize, value2=xvalue2, option=1, option3=option2)
        elif diffArr[0] < 0 and  diffArr[1] > 0:
            if diffArrAbs[0] > diffArrAbs[1]:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos2[0], pos_2=pos1[0], slope=ySlope, pxSize2=pxSize, value2=yvalue3, option=0, option3=option2)
            else:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos1[1], pos_2=pos2[1], slope=xSlope, pxSize2=pxSize, value2=xvalue2, option=1, option3=option2)
        elif diffArr[0] > 0 and  diffArr[1] < 0:
            if diffArrAbs[0] > diffArrAbs[1]:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos1[0], pos_2=pos2[0], slope=ySlope, pxSize2=pxSize, value2=yvalue2, option=0, option3=option2)
            else:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos2[1], pos_2=pos1[1], slope=xSlope, pxSize2=pxSize, value2=xvalue3, option=1, option3=option2)
        else:
            if diffArrAbs[0] > diffArrAbs[1]:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos2[0], pos_2=pos1[0], slope=ySlope, pxSize2=pxSize, value2=yvalue3, option=0, option3=option2)
            else:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos2[1], pos_2=pos1[1], slope=xSlope, pxSize2=pxSize, value2=xvalue3, option=1, option3=option2)
        '''if diffArr[0] > diffArr[1]:#if x axis has bigger difference
            print("x axis bigger difference")
            if diffArr[0] < 0 and  diffArr[1] < 0:
                print("xxx")
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos2[0], pos_2=pos1[0], slope=ySlope, pxSize2=pxSize, value2=yvalue3, option=0, diffX=diffArr[0], diffY=diffArr[1])
            else:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos1[0], pos_2=pos2[0], slope=ySlope, pxSize2=pxSize, value2=yvalue2, option=0, diffX=diffArr[0], diffY=diffArr[1])
        else:#if y axis has bigger difference
            print("y axis bigger difference")
            if diffArr[0] < 0 and  diffArr[1] < 0:
                print("xxx")
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos2[1], pos_2=pos1[1], slope=xSlope, pxSize2=pxSize, value2=xvalue3, option=1, diffX=diffArr[0], diffY=diffArr[1])
            else:
                self.DrawLineForMagnifiedBmpNeededFunc(pos_1=pos1[1], pos_2=pos2[1], slope=xSlope, pxSize2=pxSize, value2=xvalue2, option=1, diffX=diffArr[0], diffY=diffArr[1])'''
        
    def DrawLineForMagnifiedBmpNeededFunc(self, pos_1, pos_2, slope, pxSize2, value2, option, option3):#if option == 0 then if diffArr[0] > diffArr[1]
        global leftColorTrue #option3 == 1 then matrix mode, else painting mode.
        if leftColorTrue == True:
            selectedColor = self.selectedColor
        else:
            selectedColor = self.selectedColorRight
        #print("diffX:" + str(diffX) +  " and diffY: " + str(diffY))
        dc = wx.MemoryDC(self.bitmapForMap)
        dc.SetBrush(wx.Brush(selectedColor))
        dc.SetPen(wx.Pen(selectedColor, style=wx.PENSTYLE_SOLID))
        for value in range((pos_1+1), (pos_2+1)): # maybe do in range((pos1[0]+1), (pos2[0]+1)) to ignore first yval entry because already drew that rect.
                value2 += slope
                valueRounded = round(value2)
                if option == 0:
                    if option3 == 1:
                        xVal, yVal = getCoordinatesFromBmp(x1=value, y1=valueRounded, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2=pxSize2)
                        dc.DrawRectangle(x=(xVal*pxSize2), y=(yVal*pxSize2), width=pxSize2, height=pxSize2)
                    else:
                        dc.DrawRectangle(x=(value), y=(valueRounded), width=pxSize2, height=pxSize2)
                else:
                    if option3 == 1:
                        xVal, yVal = getCoordinatesFromBmp(x1=valueRounded, y1=value, xintervals=self.xintervals, yintervals=self.yintervals, arg1=pxSize2, arg2=pxSize2)
                        dc.DrawRectangle(x=(xVal*pxSize2), y=(yVal*pxSize2), width=pxSize2, height=pxSize2)
                    else:
                        dc.DrawRectangle(x=(valueRounded), y=(value), width=pxSize2, height=pxSize2)


    def editRedo(self, e : wx.EVT_MENU):
        if len(self.redo_list) > 0:
            bmp : wx.Bitmap= self.redo_list.pop()

            self.undo_list.append(bmp)
            self.undo_list_index += 1
            print(f"undo_list_index: {self.undo_list_index}")

            sizeNeeded : wx.Size = wx.Size(self.realMagnifyVal * int(self.x_totalSize), self.realMagnifyVal * int(self.y_totalSize))
            wx.Bitmap.Rescale(bmp, sizeNeeded)

            self.bitmapForMap : wx.Bitmap = bmp
            
            #self.staticbitmap.Destroy()
            #self.staticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=bmp)

            self.staticbitmap2.SetBitmap(self.bitmapForMap)
            self.staticbitmap2.Refresh()
            bmpbmp = self.staticbitmap2.GetBitmap()
            self.staticbitmap.SetBitmap(bmpbmp)
            self.bitmapForMap = self.staticbitmap.GetBitmap()

            print("editRedo")
    
    def editUndo(self, e : wx.EVT_MENU):
        if len(self.undo_list) > 1:
            removedItem = self.undo_list.pop(self.undo_list_index)

            self.redo_list.append(removedItem)

            self.undo_list_index -= 1
            print(f"undo_list_index: {self.undo_list_index}")
            tempBmp : wx.Bitmap = self.undo_list[self.undo_list_index]

            sizeNeeded : wx.Size = wx.Size(self.realMagnifyVal * int(self.x_totalSize), self.realMagnifyVal * int(self.y_totalSize))
            
            wx.Bitmap.Rescale(tempBmp, sizeNeeded)

            self.bitmapForMap : wx.Bitmap = tempBmp
            
            #self.staticbitmap.Destroy()
            #self.staticbitmap = wx.lib.statbmp.GenStaticBitmap(parent=self.panel, ID=wx.ID_ANY, pos=(10, 60), bitmap=tempBmp)

            self.staticbitmap2.SetBitmap(self.bitmapForMap)
            self.staticbitmap2.Refresh()
            bmpbmp = self.staticbitmap2.GetBitmap()
            self.staticbitmap.SetBitmap(bmpbmp)
            #self.bitmapForMap = tempBmp
            self.bitmapForMap = self.staticbitmap.GetBitmap()
            print("editUndo")
            

    def getColorLeftRightClick(self, evt):
        evtType = evt.GetEventType()
        if evtType == wx.wxEVT_LEFT_DOWN or evtType == wx.wxEVT_LEFT_UP:
            print("leftclick")
            selectedColor2= self.selectedColor
            global leftColorTrue
            leftColorTrue = True
        if evtType == wx.wxEVT_RIGHT_DOWN or evtType == wx.wxEVT_RIGHT_UP:
            print("rightclick")
            selectedColor2= self.selectedColorRight
        return selectedColor2
    
    def initColorMap2DArr(self, val1 : int, val2 : int, color : str):
        print("before func: ")
        print(self.colorMap2DArr)
        for i in range(0, val1):
            for j in range(0, val2):
                #print(str(i) + " " + str(j) )
                self.colorMap2DArr[i][j] = color

    def initColorMap2DArrDrawModeAndMagnify(self, val1 : int, val2 : int, color : str):
        for i in range(0, val1):
            for j in range(0, val2):
                #print(str(i) + " " + str(j) )
                self.colorMap2DArrDrawModeandMagnNEW[i][j] = color
                self.colorMap2DArrDrawModeandMagnOLD[i][j] = color

    def updateDrawModeMagnified2DColorMap(self, magnifiedUp):
        #tempVal = self.colorMap2DArrDrawModeandMagnNEW or tempVal = self.colorMap2DArrDrawModeandMagnOLD ?? 
        tempVal = self.colorMap2DArrDrawModeandMagnOLD
        newSizeX = self.x_totalSize * self.realMagnifyVal
        newSizeY = self.y_totalSize * self.realMagnifyVal
        print("newSizeX: " + str(newSizeX) + " newSizeY: " + str(newSizeY) )
        temp1 = 0
        temp2 = 0
        i2= 0
        #i2StopVal = newSizeX / 2
        i2StopVal = newSizeX / self.realMagnifyVal
        j2= 0
        print("realmagnifyval = " + str(self.realMagnifyVal) + "magnifyval = " + str(self.magnifyVal))

        if self.magnifyVal > 1:
            comparedVal = (self.magnifyVal + 1)
        else:
            comparedVal = self.magnifyVal


        if magnifiedUp == True:
            self.colorMap2DArrDrawModeandMagnNEW = [['h' for x in range(newSizeY)] for y in range(newSizeX)]
            #print(self.colorMap2DArrDrawModeandMagnNEW)
            for i in range(0, newSizeX):
                #if i2 == i2StopVal:
                    #i2 = 0
                #
                if i2 == i2StopVal:
                    i2 = 0
                j2 = 0
                for j in range(0, newSizeY):
                    if temp1 == comparedVal:
                        #print("i is: " + str(i) + " and j: " + str(j))
                        #print("i2 is: " + str(i2) + " and j2: " + str(j2))
                        #print("newSizeX: " + str(newSizeX) + "newSizeY: " + str(newSizeY) )
                        self.colorMap2DArrDrawModeandMagnNEW[i][j] = self.colorMap2DArrDrawModeandMagnOLD[i2][j2]
                        temp1 = 0
                        j2 += 1
                    else:
                        #print("i is: " + str(i) + " and j: " + str(j))
                        #print("i2 is: " + str(i2) + " and j2: " + str(j2))
                        #print("newSizeX: " + str(newSizeX) + "newSizeY: " + str(newSizeY) )
                        self.colorMap2DArrDrawModeandMagnNEW[i][j] = self.colorMap2DArrDrawModeandMagnOLD[i2][j2]
                        temp1 += 1
                    '''if temp1 == 0:
                        print("i is: " + str(i) + " and j: " + str(j))
                        print("i2 is: " + str(i2) + " and j2: " + str(j2))
                        #print("newSizeX: " + str(newSizeX) + "newSizeY: " + str(newSizeY) )
                        self.colorMap2DArrDrawModeandMagnNEW[i][j] = self.colorMap2DArrDrawModeandMagnOLD[i2][j2]
                        temp1 += 1
                    else:
                        print("i is: " + str(i) + " and j: " + str(j))
                        print("i2 is: " + str(i2) + " and j2: " + str(j2))
                        #print("newSizeX: " + str(newSizeX) + "newSizeY: " + str(newSizeY) )
                        self.colorMap2DArrDrawModeandMagnNEW[i][j] = self.colorMap2DArrDrawModeandMagnOLD[i2][j2]
                        temp1 = 0
                        j2 += 1'''
                #j2 = 0
                if temp2 == comparedVal:
                    temp2 = 0
                    i2 += 1
                else:
                    temp2 += 1
                '''if temp2 == 0: #need to make code dynamic so increments w.r.t self.realMagnifyVal 2^n * 2x
                    temp2 += 1
                elif temp2 == self.magnifyVal:
                    temp2 = 0
                    i2 += 1'''
                
                '''if temp2 == 0: #need to make code dynamic so increments w.r.t self.realMagnifyVal 2^n * 2x
                    temp2 += 1
                else:
                    temp2 = 0
                    i2 += 1'''
            #for i in range(0, newSizeX):
            self.colorMap2DArrDrawModeandMagnOLD = tempVal
            print("newSizeX: " + str(newSizeX) + "newSizeY: " + str(newSizeY) )
            print("UPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUP")
            print(self.colorMap2DArrDrawModeandMagnNEW)
            #for i in range(0, )
        else: #this is magnified Down
            print("DOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWN")

    def initColorMap2DArrDrawModeandMagnOLD(self, val1 : int, val2 : int, color : str):
        self.colorMap2DArrDrawModeandMagnOLD[val1][val2] = color
    
    def updateColorMap2DArr(self, val1 : int, val2 : int, color : str):
        self.colorMap2DArr[val1][val2] = color #correct functionality.

    
    def initColorMapBinTree(self, val1 : int, val2 : int, color : str):
        for i in range(val1):
            for j in range(val2):
                str1 = str(i) + "," + str(j)
                print(str1)
                if i == 0 and j == 0:
                    print("doing nothing")
                    #do nothing
                    #self.rootNode = Node(data=str1, string1=color)
                else:
                    self.rootNode.insert(data2=str1, string2=color)
        print("TESTINGTESTINGINITCOLORMAPBINTREE:")
        print(self.rootNode.left.left.left.left.left.right.right.right.data)
    
    def updateColorMapBinTree(self, val1 : int, val2 : int, color2 : str):
        print("TESTINGTESTINGINITCOLORMAPBINTREE2: val1, val2: :"+ str(val1) +", "+str(val2))
        coordinates1 = str(val1) + "," + str(val2)
        self.rootNode.updateColorAtCoordinates(coordinates=coordinates1, color=color2)

    def performFill_DFS(self, xPos, yPos, targetColor, pxSizeIs0, isDrawingModeAndMagnified): #this performs a dfs depth first search on a 2D array. 
        
        dc = wx.MemoryDC(self.bitmapForMap)
        #dc.SetPen(wx.Pen(targetColor, style=wx.PENSTYLE_SOLID))
        if xPos < 0 or xPos >= self.x_totalSize or yPos < 0 or yPos >= self.y_totalSize or targetColor == self.colorMap2DArr[xPos][yPos]:
            return
        else:
            if pxSizeIs0 == True:
                dc.SetPen(wx.Pen(targetColor, style=wx.PENSTYLE_SOLID))
                point = wx.Point(xPos, yPos)
                dc.DrawPoint(point)
                self.updateColorMap2DArr(val1=xPos, val2=yPos, color=targetColor)
                self.performFill_DFS(xPos=xPos+1, yPos=yPos, targetColor=targetColor, pxSizeIs0=True, isDrawingModeAndMagnified=False)
                self.performFill_DFS(xPos=xPos-1, yPos=yPos, targetColor=targetColor, pxSizeIs0=True, isDrawingModeAndMagnified=False)
                self.performFill_DFS(xPos=xPos, yPos=yPos+1, targetColor=targetColor, pxSizeIs0=True, isDrawingModeAndMagnified=False)
                self.performFill_DFS(xPos=xPos, yPos=yPos-1, targetColor=targetColor, pxSizeIs0=True, isDrawingModeAndMagnified=False)
            else:
                pxSize2= self.realMagnifyVal
                dc.SetBrush(wx.Brush(targetColor))
                dc.SetPen(wx.Pen(targetColor, style=wx.PENSTYLE_SOLID))
                dc.DrawRectangle(x=(xPos*pxSize2), y=(yPos*pxSize2), width=pxSize2, height=pxSize2)
                self.updateColorMap2DArr(val1=xPos, val2=yPos, color=targetColor)
                self.performFill_DFS(xPos=xPos+1, yPos=yPos, targetColor=targetColor, pxSizeIs0=False, isDrawingModeAndMagnified=False)
                self.performFill_DFS(xPos=xPos-1, yPos=yPos, targetColor=targetColor, pxSizeIs0=False, isDrawingModeAndMagnified=False)
                self.performFill_DFS(xPos=xPos, yPos=yPos+1, targetColor=targetColor, pxSizeIs0=False, isDrawingModeAndMagnified=False)
                self.performFill_DFS(xPos=xPos, yPos=yPos-1, targetColor=targetColor, pxSizeIs0=False, isDrawingModeAndMagnified=False)
    
    def performFill_flood_fill(self, xPos, yPos, targetColor, pxSizeIs0, isDrawingModeAndMagnified):
        if isDrawingModeAndMagnified == True:
            print("isDrawingModeAndMagnifiedisDrawingModeAndMagnifiedisDrawingModeAndMagnifiedisDrawingModeAndMagnified")
        oldColor = self.colorMap2DArr[xPos][yPos]
        if oldColor == targetColor:
            return
        self.performFill_DFS(xPos, yPos, targetColor, pxSizeIs0, isDrawingModeAndMagnified)


    def Quit(self, e):
        global notifySaveProjectForImgBlock
        global isProjectSaved
        if notifySaveProjectForImgBlock == True and isProjectSaved == False:
            print("areyousure?\n")
            dialog = wx.MessageDialog(self, "Do you want to save the project before quitting?", "Save Project Before Quitting", wx.YES_NO | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_INFORMATION)
            answer = dialog.ShowModal()
            dialog.Destroy()
            if answer == wx.ID_YES:
                # Do something for the "Yes" button press
                self.SaveProject(e)
                self.Destroy()
            elif answer == wx.ID_NO:
                # Do something for the "No" button press
                isProjectSaved = False
                self.Destroy()
                #self.GetEventHandler().ProcessEvent(wx.EVT_WINDOW_DESTROY)
            else:
                # Do nothing for the "Cancel" button press
                return
        notifySaveProjectForImgBlock = False

        global doesStaticImgBlockExist
        doesStaticImgBlockExist = False
        
        isProjectSaved = False
        self.Destroy()
        #self.Destroy()
        #self.Close()

class GetModeData(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Create Image Block", size= (470,320))
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.lblname = wx.StaticText(self.panel, label="Choose drawing mode:", pos=(20,20))
        #self.x_dir = wx.TextCtrl(self.panel, value="", pos=(140,20), size=(100,-1))#pos=(110,20)

        self.drawingMode : str
        self.drawingModeList = ["Matrix Mode", "Painting Mode"]

        self.drawingModeRadioBox : wx.RadioBox = wx.RadioBox(self.panel, label = 'Choose', pos = (20,60), choices = self.drawingModeList, majorDimension = 1, style = wx.RA_SPECIFY_ROWS)

        self.saveButton = wx.Button(self.panel, id=wx.ID_OK, label="Save", pos=(140,220))
        self.saveButton.SetDefault()

        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(240,220))#pos=(240,240))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveDrawingMode)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Center()
        self.Show()
    
    def SaveDrawingMode(self, event):
        index1 : int = self.drawingModeRadioBox.GetSelection()
        self.drawingMode = self.drawingModeList[index1]
        self.isDataThere = True
        self.Destroy()

    def OnQuit(self, event):
        #self.result_name = None
        global doesStaticImgBlockExist
        doesStaticImgBlockExist = False
        print("OnQuit call")
        parent = self.GetGrandParent()
        parent.Destroy()
        global returnFromFrameClass
        returnFromFrameClass = True

class GetData(wx.Dialog):
    def __init__(self, parent):
        self.isDataThere = False
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Create New Project", size= (470,320))
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.lblname = wx.StaticText(self.panel, label="x-dir per block:", pos=(20,20))
        self.x_dir = wx.TextCtrl(self.panel, value="", pos=(140,20), size=(100,-1))#pos=(110,20)
        self.lblsur = wx.StaticText(self.panel, label="y-dir per block:", pos=(20,60))
        self.y_dir = wx.TextCtrl(self.panel, value="", pos=(140,60), size=(100,-1))
        
        self.lblname2 = wx.StaticText(self.panel, label="x total size:", pos=(20,100))
        self.x_totalSize2 = wx.TextCtrl(self.panel, value="", pos=(140,100), size=(100,-1))
        self.lblsur2 = wx.StaticText(self.panel, label="y total size:", pos=(20,140))
        self.y_totalSize2 = wx.TextCtrl(self.panel, value="", pos=(140,140), size=(100,-1))

        self.saveButton = wx.Button(self.panel, id=wx.ID_OK, label="Save", pos=(140,220))
        self.saveButton.SetDefault()

        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(240,220))#pos=(240,240))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Center()
        self.Show()

    def SaveConnString(self, event):
        self.result_x_dir = self.x_dir.GetValue()
        self.result_y_dir = self.y_dir.GetValue()
        self.x_totalSize = self.x_totalSize2.GetValue()
        self.y_totalSize = self.y_totalSize2.GetValue()
        if self.result_x_dir=="" or self.result_y_dir=="" or self.x_totalSize=="" or self.y_totalSize=="":
            print("input must not be blank.\n")
            dlg = ErrorDialog(parent=self.panel, option=1)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            regexp1 = re.search('[a-zA-Z]', self.result_x_dir)
            regexp2 = re.search('[a-zA-Z]', self.result_y_dir)
            regexp3 = re.search('[a-zA-Z]', self.x_totalSize)
            regexp4 = re.search('[a-zA-Z]', self.y_totalSize)

            if regexp1 == None and regexp2 == None and regexp3 == None and regexp4 == None:
                if (int(self.x_totalSize) % int(self.result_x_dir) == 0) & (int(self.y_totalSize) % int(self.result_y_dir) == 0):
                    self.isDataThere = True
                    self.Destroy()
                else:
                    self.isDataThere = False
                    dlg = ErrorDialog(parent=self.panel, option=2)
                    dlg.ShowModal()
                    dlg.Destroy()
                    '''errormessage = wx.StaticText(self.panel, label="ERROR", pos=(260,70))
                    errormessage.SetForegroundColour("#FF0000")
                    errormessage2 = wx.StaticText(self.panel, label="numbers must be divisible", pos=(260,90))
                    errormessage2.SetForegroundColour("#FF0000")
                    errormessage3 = wx.StaticText(self.panel, label="with no remainder.", pos=(260,110))
                    errormessage3.SetForegroundColour("#FF0000")'''
            else:
                self.isDataThere = False
                dlg = ErrorDialog(parent=self.panel, option=4)
                dlg.ShowModal()
                dlg.Destroy()

    
    def OnQuit(self, event):
        #self.result_name = None
        self.isDataThere = False
        self.Destroy()

class GetData2(wx.Dialog):
    def __init__(self, parent):
        self.isDataThere = False
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Create Image Block", size= (470,220))
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.lblname = wx.StaticText(self.panel, label="x total size:", pos=(20,20))
        self.x_totalSize2 = wx.TextCtrl(self.panel, value="", pos=(140,20), size=(100,-1))#pos=(110,20)
        self.lblsur = wx.StaticText(self.panel, label="y total size:", pos=(20,60))
        self.y_totalSize2 = wx.TextCtrl(self.panel, value="", pos=(140,60), size=(100,-1))

        self.saveButton = wx.Button(self.panel, id=wx.ID_OK, label="Save", pos=(140,100))
        self.saveButton.SetDefault()

        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(240,100))#pos=(240,240))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString2)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Center()
        self.Show()

    def SaveConnString2(self, event):
        self.x_totalSize = self.x_totalSize2.GetValue()
        self.y_totalSize = self.y_totalSize2.GetValue()
        regexp5 = re.search("[a-zA-Z]", self.x_totalSize)
        regexp6 = re.search("[a-zA-Z]", self.y_totalSize)
        if regexp5 == None and regexp6 == None:
            if (self.x_totalSize and self.y_totalSize):
                self.isDataThere = True
                self.Destroy()
            else:
                self.isDataThere = False
                dlg = ErrorDialog(parent=self.panel, option=1)
                dlg.ShowModal()
                dlg.Destroy()
                '''errormessage = wx.StaticText(self.panel, label="ERROR", pos=(260,70))
                errormessage.SetForegroundColour("#FF0000")
                errormessage2 = wx.StaticText(self.panel, label="numbers must be divisible", pos=(260,90))
                errormessage2.SetForegroundColour("#FF0000")
                errormessage3 = wx.StaticText(self.panel, label="with no remainder.", pos=(260,110))
                errormessage3.SetForegroundColour("#FF0000")'''
        else:
            self.isDataThere = False
            dlg = ErrorDialog(parent=self.panel, option=4)
            dlg.ShowModal()
            dlg.Destroy()

    def OnQuit(self, event):
        #self.result_name = None
        self.isDataThere = False
        self.Destroy()
        self.Close()

class ShowHelpDialog(wx.Dialog):
        def __init__(self, parent):
            wx.Dialog.__init__(self, parent, wx.ID_ANY, "Help", size= (580,470))
            self.panel = wx.Panel(self, wx.ID_ANY)

            self.lbl1name = wx.StaticText(self.panel, label="Go to File >> New Project, and File >> Select Image Block", pos=(20,20))
            self.lbl1name.SetForegroundColour("Blue")
            self.lbl2name = wx.StaticText(self.panel, label="to configure new project and select the image for the map. ", pos=(20,40))
            self.lbl2name.SetForegroundColour("Blue")
            self.lbl3name = wx.StaticText(self.panel, label="In \"New Project\" you give the image block size, in px for", pos=(20,60))
            self.lbl3name.SetForegroundColour("Blue")
            self.lbl4name = wx.StaticText(self.panel, label="width and height. Creating \"image blocks\" is currently unavailable, ", pos=(20,80))
            self.lbl4name.SetForegroundColour("Blue")
            self.lbl5name = wx.StaticText(self.panel, label="but is a feature which is to be included in future versions. Using ", pos=(20,100))
            self.lbl5name.SetForegroundColour("Blue")
            self.lbl6name = wx.StaticText(self.panel, label="\"GraphicsGale\" is suggested for building image blocks.", pos=(20,120))
            self.lbl6name.SetForegroundColour("Blue")
            self.lbl7name = wx.StaticText(self.panel, label="When New Project is set up and the image block is selected, click anywhere", pos=(20,140))
            self.lbl7name.SetForegroundColour("Blue")
            self.lbl8name = wx.StaticText(self.panel, label="on the map to draw the image block to the map. When finished, ", pos=(20,160))
            self.lbl8name.SetForegroundColour("Blue")
            self.lbl9name = wx.StaticText(self.panel, label="go to File >> Save map to save the map as an image to the specified", pos=(20,180))
            self.lbl9name.SetForegroundColour("Blue")
            self.lbl10name = wx.StaticText(self.panel, label="directory. File >> Save project are used to save your work in a file", pos=(20,200))
            self.lbl10name.SetForegroundColour("Blue")
            self.lbl11name = wx.StaticText(self.panel, label="with a .smp file extension. File >> Open project will restore the saved", pos=(20,220))#Intended software use is designed so that the same block
            self.lbl11name.SetForegroundColour("Blue")
            self.lbl12name = wx.StaticText(self.panel, label="work when directed to the file path that has .smp file extension.", pos=(20,240))
            self.lbl12name.SetForegroundColour("Blue")
            self.lbl13name = wx.StaticText(self.panel, label="Intended software use is designed so that the same block", pos=(20,260))
            self.lbl13name.SetForegroundColour("Blue")
            self.lbl14name = wx.StaticText(self.panel, label="dimensions for width and height (px) is used in the \"Configure\"", pos=(20,280))
            self.lbl14name.SetForegroundColour("Blue")
            self.lbl15name = wx.StaticText(self.panel, label="settings and selected image block dimensions.", pos=(20,300))
            self.lbl15name.SetForegroundColour("Blue")

            self.closeButton = wx.Button(self.panel, label="Ok", pos=(220,350))#pos=(240,240))
            self.closeButton.SetDefault()
            
            self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
            self.Bind(wx.EVT_CLOSE, self.OnQuit)
            self.Center()
            self.Show()
        
        def OnQuit(self, event):
            self.Destroy()
            self.Close()

class ErrorDialog(wx.MessageDialog):
    def __init__(self, parent, option):
        match option:
            case 0:
                wx.MessageDialog.__init__(self, parent, message="There is no active map.", caption="Error", style=wx.OK_DEFAULT|wx.CENTRE)
            case 1:
                wx.MessageDialog.__init__(self, parent, message="Inputs must not be blank.", caption="Error", style=wx.OK_DEFAULT|wx.CENTRE)
            case 2:
                wx.MessageDialog.__init__(self, parent, message="Numbers must be divisible with no remainder.", caption="Error", style=wx.OK_DEFAULT|wx.CENTRE)
            case 3:
                wx.MessageDialog.__init__(self, parent, message="There is no active image block.", caption="Error", style=wx.OK_DEFAULT|wx.CENTRE)
            case 4:
                wx.MessageDialog.__init__(self, parent, message="Input must be numbers", caption="Error", style=wx.OK_DEFAULT|wx.CENTRE)
        self.Center()
        self.Show()
    
    def OnQuit(self, event):
        self.Destroy()
        self.Close()

'''class SaveBeforeQuitDialog2(wx.MessageDialog):
    def __init__(self, parent):
        wx.MessageDialog.__init__(self, parent, message="Do you want to save project before quitting?", caption="Save Project Before Quit", style=wx.OK_DEFAULT|wx.CENTRE|wx.OK|wx.CANCEL)
    
    def OnQuit(self, event):
        self.Destroy()
        self.Close()'''
class SaveBeforeQuitDialog(wx.Dialog):
        def __init__(self, parent):
            wx.Dialog.__init__(self, parent, wx.ID_ANY, "Save Project Before Quit", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
            self.panel = wx.Panel(self, wx.ID_ANY)
            self.lblname = wx.StaticText(self.panel, label="Do you want to save the project before quitting?", pos=(20,20))

            self.saveButton = wx.Button(self.panel, id=wx.ID_OK, label="Save", pos=(140,100))
            self.saveButton.SetDefault()

            self.closeButton = wx.Button(self.panel, label="Cancel", pos=(240,100))#pos=(240,240))
            self.saveButton.Bind(wx.EVT_BUTTON, parent.SaveProject)
            self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
            self.Bind(wx.EVT_CLOSE, self.OnQuit)
            self.Center()
            self.Show()
        
        def OnQuit(self, e):
            self.Destroy()
            self.Close()


class TestPanel(scrolled.ScrolledPanel):

    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)

        self.vbox = wx.BoxSizer(wx.VERTICAL) #this is the main box sizer
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vhbox = wx.BoxSizer(wx.HORIZONTAL)#this is the vertical horizontal box sizer

    def setAddToBoxSizerVbox(self, itemToAdd):
        self.vbox.Add(self.vhbox)
        self.vhbox.Add(itemToAdd)

    '''def setAddToBoxSizerVboxLeftAlign(self, itemToAdd):
        self.vbox.Add(self.vhbox)
        self.vhbox.Add(itemToAdd, flag=wx.ALIGN_LEFT)'''

    def addToBoxSizerVbox(self, itemToAdd):
        self.vbox.Add(itemToAdd)

    def addToBoxSizerVBoxCentre(self, itemToAdd):
        self.vbox.Add(window=itemToAdd, flag=wx.ALIGN_CENTRE) #wx.EXPAND?

    def addToBoxSizerHbox(self, itemToAdd):
        self.hbox.Add(itemToAdd)

    def setSizerAndScrolling(self):
        self.vbox.Add(self.hbox)
        self.SetSizer(self.vbox)
        self.SetupScrolling()
    
    def setupScrolling(self):
        self.SetupScrolling()
    
    def addToBoxSizerVHbox(self, itemToAdd):
        self.vhbox.Add(itemToAdd)
    
    def OnQuit(self, event):
        self.Destroy()
        self.Close()

def getCoordinatesFromBmp(x1, y1, xintervals, yintervals, arg1, arg2): # global function.
    for x2 in range(xintervals):
        if x1 in range(x2*arg1, arg1*(x2+1)):
            xVal2 = x2
    for y2 in range(yintervals):
        if y1 in range(y2*arg2, arg2*(y2+1)):
            yVal2 = y2
    return xVal2, yVal2
    '''for x2 in range(xintervals):
        for y2 in range(yintervals):
            if x1 in range(x2*arg1, arg1*(x2+1)):
                if y1 in range(y2*arg2, arg2*(y2+1)):
                    #print(f"here x2: {x2} and y2: {y2}")
                    xVal2 = x2
                    yVal2 = y2
    return xVal2, yVal2'''

def main():
    app = wx.App()
    #wx.lib.inspection.InspectionTool().Show()
    windowClass(None)
    app.MainLoop()
    return 0

main()
