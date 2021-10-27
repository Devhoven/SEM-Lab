# SEM-Lab
This is a Software which works with the Zeiss DSM 940 A SEM

It has 2 general modes, the "Operation Mode" and the "Aquisition Mode":

<p>
  <img width="48%" src="https://user-images.githubusercontent.com/40501092/122560962-894e6500-d041-11eb-91c1-2d8ce6e055e9.png"/>
  <img align="right" width="48%" src="https://user-images.githubusercontent.com/40501092/122561004-9408fa00-d041-11eb-82df-51895312c77d.png"/>
</p> <br>

## Operation Mode:
This mode provides the real-time examination of samples, e.g. qualitative inspection and geometrical measurement. <br>

For this purpose, the actual values for acceleration voltage, magnification and working distance are read from the live image and displayed in the left-hand side panel. <br>
The read values are recalculated to match the utilization of a 75” 4K display, 430 µm pixel pitch. <br><br>
Furthermore the real-time image can be displayed using different look up tables (LUTs), colorizing the actual grayscale image. <br>
This can be used to improve highlighting special features of a specimen or simply offering a more appealing way of displaying.
<a href="https://user-images.githubusercontent.com/40501092/122561077-af740500-d041-11eb-987b-90212a72d3cb.png"> Example </a> <br><br>
To quantitatively measure geometrical features of a specimen the cursor can be used by pulling a line using the left mouse-button. <a href="https://user-images.githubusercontent.com/40501092/122561121-c286d500-d041-11eb-9cdd-395bc5153395.png"> Example </a> <br>
To toggle between rectangular or circular area measurement mode use the right-click and choose from the drop down menu. <br>
Additionally the real-time image can be un-docked from the GUI and be displayed in external window. <br><br>
On the lower left-hand side the specimen chamber is displayed for observation purposes. This window is active as well in Operation Mode and in Acquisition Mode. <br><br>

## Aquisition Mode:
The Acquisition Mode is used to acquire the actual image in high resolution for documentation purposes.  <br>

On the first panel all of the settings of the SEM, which have been used to capture the current image, can be put in. If the image is saved, all this data is going to be saved as metadata in the image file. <br>
Those can be viewed in the PNG-metadata, or can be opened in the picture with a click on the saved image on the right-hand side Images-panel and the metadata is going to be displayed along the image. <br><br>
Below that is the "Image aquisition"-panel. <br>
To capture an image, the "Capture Image"-button has to be used. The capturing will be guided with instructions that are shown at the bottom of the panel. <br>
After successfully capturing an image, it can be saved using the "Save Image"-button. <br>
If an image has been saved, it is going to appear in the Image-panel, along all of the other images which are located in the same folder, which has been chosen. <br><br>
Beneath that, is the "Image-Spaw-Repair"-panel. <br>
The "Swap Up"-button and "Swap Down"-button are used for "repairing" the recently captured image, since sometimes a bug occures, where the image gets stretched in some odd pattern, which can be fixed with either of the buttons. <a href="https://user-images.githubusercontent.com/40501092/122522560-63f83180-d016-11eb-9fd5-3c449747a33b.png"> Example </a> <br><br>
The SEM does not scan the image completely linearly, which causes a distortion in the result.
This distortion won't be noticed under normal circumstances and is fine in almost all cases, but if you want more accurate dimensions, you can use the "Squish"-button to get a more "square" image Example. <a href="https://user-images.githubusercontent.com/40501092/122523529-69a24700-d017-11eb-884b-cdec01528045.png"> Example </a> <br><br>

## Full Photo View:
There actually is a third mode, the <a href="https://user-images.githubusercontent.com/40501092/122532910-47adc200-d021-11eb-8993-2279dd2a181f.png"> Full Photo View</a>. <br><br>
It is used to view the captured image in full resolution without any of the GUI elements next to it. <br>
And just like in the Photo Mode, zooming and panning is available to take a closer look at the image. <br><br>

## Settings:
The <a href="https://user-images.githubusercontent.com/40501092/122524523-8428f000-d018-11eb-9ad0-66cfaedacf94.png"> Settings </a> can be accessed via the Navigation Bar under the "Program"-tab. <br>
The first setting is a drop down list of all the currently available ports. <br>
A selection of the port of the Digital Photo Unit must be made, otherwise it’s not possible to capture any images. <br><br>
The "Choose full photo view background color"-button should be self-explanatory. <br><br>
The "Choose the line color"-button is used to change the color of the measuring tools. <br><br>
The last two radio buttons are used to change the language of the program. <br>
To change the language, the SEM Lab software must be restarted to apply the changes. <br><br>

## The Image-panel:
In the Image-panel are all of the images which have been saved with the SEM Lab software, which are in the folder, which is currently chosen. <br>
The path of the current folder is displayed right beneath the headline of the panel. <br><br>
By clicking any of the shown images, the image itself with its metadata is going to be displayed. <br><br>
By hovering long enough over one image, its name is going to show up as a tooltip. <br><br>
To delete one of the images, right-click on the image and press the delete button. <br><br>

## Shortcuts:
There are a few shortcuts to make the navigation in the program much easier:
- ESC: Close the program, or close the Full Photo View
- F1: Toggle Fullscreen
- 1: Switch to Operation Mode
- 2: Switch to Aquisition Mode
- A: Toggle the Full Photo View
- Enter: In the Aquisition Mode, the image-capturing-process is going to be started
- E: Open the Settings
- M: Open the Manual of the Zeiss DSM 940 A
- K: Shows the key assignment of the SEM keyboard

## Known problems and their solutions:
I made a small video showcasing a few problems and their solutions: <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"> Video </a>
