# SEM-Lab
This is a GUI which works with the Zeiss DSM 940 A SEM

It has 2 general modes, the "Work Mode" and the "Aquisition Mode":

<p>
  <img width="48%" src="https://user-images.githubusercontent.com/40501092/122232303-6b56f800-cebb-11eb-8337-e0d60ccfdefb.png">
  <img align="right" width="48%" src="https://user-images.githubusercontent.com/40501092/122232381-7c076e00-cebb-11eb-8903-cf495986c2c0.png">
</p>

<br>
The Work Mode is used to set up the right focus etc. of the SEM with help of the console of the SEM and the live image. <br>

For that purpose there are the settings of the REM (Voltage, Magnification, Working Distance), which are filtered from the live image. <br>
Below that is a selection of cv2 Look Up Tables you can choose from to change the color of the image and highlight some areas better. 
<a href="https://user-images.githubusercontent.com/40501092/122237568-b7a43700-cebf-11eb-9ccc-83b51f2a9179.png"> Example </a> <br>
You are also able to measure distances with your mouse. 
<a href="https://user-images.githubusercontent.com/40501092/122238461-71030c80-cec0-11eb-915b-6ad8bbb9563e.png"> Example </a><br>
There also is a drop down menu if you right-click on the live image, where you can open the driver settings, show the live image in a external window or choose a measuring mode (Either a cirlce, or a rectangle). <br><br>

The Aquisition Mode is used to capture the actual Image <br>

On the first panel you are able to put in all of the settings of the REM you used to capture the current image. If you save the picture after that, all of the metadata you put in is going to be saved. <br>
You can look at it in the PNG-metadata, or you can open the picture with a left-click on the saved image on the right hand "Images"-Panel and the metadata is going to be shown in the top left panel and the image in the middle of the canvas.

There are some elements that are always in the view: <br> 
- The buttons to switch from Work Mode to Aquisition Mode <br>
- The Probe Camera on the bottom left <br>
- The panel on the right with all of the saved pictures which are in the current folder <br>
- The Navigation Bar


