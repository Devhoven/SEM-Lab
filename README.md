# SEM-Lab
This is a GUI which works with the Zeiss DSM 940 A SEM

It has 2 general modes, the "Work Mode" and the "Aquisition Mode":

<p>
  <img width="48%" src="https://user-images.githubusercontent.com/40501092/122232303-6b56f800-cebb-11eb-8337-e0d60ccfdefb.png"/>
  <img align="right" width="48%" src="https://user-images.githubusercontent.com/40501092/122232381-7c076e00-cebb-11eb-8903-cf495986c2c0.png"/>
</p> <br>

## Work Mode:
The Work Mode is used to set up the right focus etc. of the SEM with help of the console of the SEM and the live image. <br>

For that purpose are the settings of the SEM (Voltage, Magnification, Working Distance) displayed in this panel, which are filtered from the live image and adjusted to the new screen. <br><br>
Below that is a selection of cv2 Look Up Tables you can choose from, to change the color of the image and highlight some areas better. 
<a href="https://user-images.githubusercontent.com/40501092/122237568-b7a43700-cebf-11eb-9ccc-83b51f2a9179.png"> Example </a> <br><br>
You are also able to measure the probe with your mouse. 
<a href="https://user-images.githubusercontent.com/40501092/122238461-71030c80-cec0-11eb-915b-6ad8bbb9563e.png"> Example </a><br><br>
There also is a drop down menu if you right-click on the live image, where you can choose a measuring mode (Either a cirlce, or a rectangle), open the driver settings or show the live image in a external window. <br><br>
The last panel is a cam, which shows the Probe Table all of the time, even in the Aquisition Mode. <br>
You can also show this cam in an external window, or open its driver settings, with a right-click on the cam. <br><br>

## Aquisition Mode:
The Aquisition Mode is used to capture the actual Image. <br>

On the first panel you are able to put in all of the settings of the SEM, you used to capture the current image. If you save the picture after that, all of the metadata you put in is going to be saved. <br>
You can look at it in the PNG-metadata, or you can open the picture with a click on the saved image on the right hand Images-Panel and the metadata is going to be displayed along the image. <br><br>
Below that is the "Image aquisition"-panel. <br>
If you want to capture an image, you have to click the "Capture Image"-button and follow the instructions that are shown below that. <br>
After successfully capturing an image you can save the image with the help of the "Save Image"-button, which is conveniently placed right below the "Capture Image"-button. <br>
If you saved the image where you want it, it is going to appear in the Image-panel, along all of the other images which are located in the folder where you saved the new image. <br><br>
Below that, is the "Image-Spaw-Repair"-panel. <br>
The "Swap Up"-button and "Swap Down"-button are used for "repairing" the newly captured image, since sometimes a bug occures, where the image gets shifted in some odd pattern, which you can fix with either of the buttons. <a href="https://user-images.githubusercontent.com/40501092/122522560-63f83180-d016-11eb-9fd5-3c449747a33b.png"> Example </a> <br><br>
The "Squish"-button is used to "squish" the image, since it is shifted in a way, which makes it not perfectly square. <br>
This distortion won't be noticed under normal circumstances and is fine in almost all cases, but if you want the exactly right dimensions, you can use the "Squish"-button to fix that. <a href="https://user-images.githubusercontent.com/40501092/122523529-69a24700-d017-11eb-884b-cdec01528045.png"> Example </a> <br><br>

## Full Photo View:
There actually is a third mode, the <a href="https://user-images.githubusercontent.com/40501092/122532910-47adc200-d021-11eb-8993-2279dd2a181f.png"> Full Photo View</a>. <br><br>
It is used to view the image in full resolution without any of the GUI elements next to it. <br>
And just like in the Photo Mode, you can zoom and pan to take a closer look at the image. <br><br>

## Settings:
You can access the  <a href="https://user-images.githubusercontent.com/40501092/122524523-8428f000-d018-11eb-9ad0-66cfaedacf94.png"> Settings </a> via the Navigation Bar under the "Program"-tab. <br>
The first setting is a drop down list of all the currently available ports. <br>
There you have to select the port of the Digital Photo Unit, otherwise you won't be able to capture any images. <br><br>
The "Choose full photo view background color"-button should be self-explanatory. <br><br>
The "Choose the line color"-button is used to change the color of the measuring tools. <br><br>
The last two radio buttons are used to change the language of the program. <br>
If you change the language, you have to restart the SEM Lab to apply the changes. <br><br>

## The Image-panel:
In the Image-panel are all of the images you saved with the SEM Lab, which are in the folder you are currently located in. <br>
You can see the  path of the folder you are currently located in, right beneath the headline of the panel. <br><br>
You can click on any of the shown images and the image itself with its metadata is going to be displayed. <br><br>
If you hover long enough over one image, its name is going to show up as a tooltip. <br><br>
And if you want to delete one of the images, you can do that with a right-click on the image. <br><br>

## Shortcuts:
There are a few shortcuts to make the navigation in the program much easier:
- ESC: Close the program, or close the Full Photo View
- F1: Toggle Fullscreen
- 1: Switch to Work Mode
- 2: Switch to Aquisition Mode
- A: Toggle the Full Photo View
- Enter: If you are in the Aquisition Mode, the image-capturing-process is going to be started
- E: Open the Settings
- M: Open the Manual of the Zeiss DSM 940 A
- K: Shows the key assignment of the SEM keyboard

## Known problems and their solutions:
I made a small video showcasing a few problems and their solutions: <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"> Video </a>
