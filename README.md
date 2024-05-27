#Simple Map Builder and Sprite Editor
##Tutorial
In the "File" option, top-left corner, presents all the program options.
###Create a 2D map project
File>>New Project
Input dimensions wanted, squares must be divisible by total x, y, (map) size. Values are in pixels. 
For example,
x-dir per block: 32
y-dir per block: 64
x total size: 320
y total size: 640

After creating a project, select your image block by clicking File>>Select image block, and click on the map squares to start creating your map.
Redo, and Undo options are present in Edit>>Redo, and Edit>>Redo, also with shortcuts Ctrl+Z, and Ctrl+Y.
To save your map as a PNG when done, click File>>Save map.
To save your work to reopen on the program later, save work by clicking File>>Save project, to save your work as a .SMP(simple map project) file.
To continue your work, click File>>Open Project to search for an .SMP file and continue your work.

###Create Sprites or Pixel Art
In the "File" option, top-left corner, presents all the program options.
To create sprites or pixel art, select File>>Create image block.
Select between Matrix or Painting mode. Matrix mode creates a matrix for you to draw on, and painting mode is more fluid, no matrix. I personally prefer the matrix mode.
Next, input the desired size in pixels for your image block.
For example
x total size: 32
y total size: 64

Then when the map is presented, left click to draw current color, and right click to draw last color, select color button to select colors, and magnify, and minimize by clicking on magnify/minimize buttons. Draw, Line, and Fill options are present to help draw. Fill option does not work yet for painting mode.
Redo, and Undo options are present in Edit>>Redo, and Edit>>Redo, also with shortcuts Ctrl+Z, and Ctrl+Y.
To save your image block as a PNG when done, click File>>Save image.
To save your work to reopen on the program later, save work by clicking File>>Save create block project, to save your work as a .SMB(simple map block) file.
To continue your work, click File>>Open block project to search for an .SMB file and continue your work.

##Installation
To run Simple Map Builder and Sprite Editor with Python, run  mapbuilder.py from the root directory, with the needed .ico found in the same directory as mapbuilder.py. 
To run this program, Python 3.10.6 is used, and the python module wxPython==4.2.0 is required.

To install the Simple Map Builder and Sprite Editor, download the zip file: [https://drive.google.com/uc?export=download&id=16BQ9Ee1y35aF5r_HbvVw6tIk0Nx4g99j](HERE). After downloading, extract the folder anywhere in your PC, and run the mapbuilder.exe file that is inside the folder, to run the program. Afterwards you could create a shortcut of mapbuilder.exe for easy acces.