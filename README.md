# SEM-Lab
This is a GUI which works with the Zeiss DSM 940 A SEM

It has 2 general modes, the "Work Mode" and the "Aquisition Mode":

<p>
  <img width="48%" src="https://user-images.githubusercontent.com/40501092/122232303-6b56f800-cebb-11eb-8337-e0d60ccfdefb.png">
  <img align="right" width="48%" src="https://user-images.githubusercontent.com/40501092/122232381-7c076e00-cebb-11eb-8903-cf495986c2c0.png">
</p> <br>

## Work Mode:
The Work Mode is used to set up the right focus etc. of the SEM with help of the console of the SEM and the live image. <br>

For that purpose there are the settings of the REM (Voltage, Magnification, Working Distance), which are filtered from the live image. <br><br>
Below that is a selection of cv2 Look Up Tables you can choose from to change the color of the image and highlight some areas better. 
<a href="https://user-images.githubusercontent.com/40501092/122237568-b7a43700-cebf-11eb-9ccc-83b51f2a9179.png"> Example </a> <br><br>
You are also able to measure distances with your mouse. 
<a href="https://user-images.githubusercontent.com/40501092/122238461-71030c80-cec0-11eb-915b-6ad8bbb9563e.png"> Example </a><br>
There also is a drop down menu if you right-click on the live image, where you can choose a measuring mode (Either a cirlce, or a rectangle), open the driver settings or show the live image in a external window <br><br>

## Aquisition Mode:
The Aquisition Mode is used to capture the actual Image <br>

On the first panel you are able to put in all of the settings of the REM you used to capture the current image. If you save the picture after that, all of the metadata you put in is going to be saved. <br>
You can look at it in the PNG-metadata, or you can open the picture with a left-click on the saved image on the right hand "Images"-Panel and the metadata is going to be shown in the top left panel and the image in the middle of the canvas. <br><br>
Below that is the "Image aquisition"-panel. <br>
If you want to capture an image, you have to click the "Capture Image"-button and follow the instructions that are shown below that. <br>
After successfully capturing an image you can save the image with the help of the "Save Image"-button, which is conveniently placed right below the "Capture Image"-button. <br>
If you saved the image where you want it, it is going to appear in the "Image"-panel, along all of the other images which are located in the folder where you saved the new image. <br><br>
Below that, is the "Image-Spaw-Repair"-panel <br>
The "Swap Up"-button and "Swap Down"-button are used for "repairing" the newly captured image, since sometimes a bug occures, where the image gets shifted in some odd pattern, which you can fix with either of the buttons !!!INSERT EXAMPLE HERE!!! <br><br>
The "Squish"-button is used to "squish" the image, since it is shifted in a way, which makes it not perfectly square <br>
This distortion won't be noticed under normal circumstances and it fine in almost all cases, but if you want exactly the right dimensions, you can use the "Squish"-button to fix that <br>
