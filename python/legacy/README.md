# Project Brender: Blender Brender Panel
```
Author: Gustavo Lopez and Feras Khemakhem
Date:	3-13-2019
Version: 3.1.0
```

The **Brender Panel** is a simple Panel addon to Blender to allow the user to apply materials, transformations, and wireframe overlays systematically to the animations exported/imported using Brender.

## Getting Started

These instructions will help you get started with applying materials and wireframe overlays to objects in your blender animation.

### Prerequisites

What you will need as a starting point to use the Brender panel.

1. Download all python directories/scripts from the Brender package.

2. Import an animation using the Brender python import script. In this example we will have two objects in the scene with names:

  * Cloth1
  * Sphere

This tutorial assumes that the naming scheme of your objects follows the "######\_ObjName" format.

### Brender Panel Setup and Sample Run

How to setup the Brender panel in Blender to be used with the sample.

1. Open the necessary addon scripts

   Once your animation/objects are imported to the scene, open the scripting view in Blender. Click the "Open" button in the scripting panel to open all scripts in the `brender/python/brender_imports` directory (one at a time). 

2. Run each of the scripts that you have opened. 

	Note: nothing will happen to your animation or objects just yet. `brender_panel_addon.py` will create a Brender Toolset Panel in Blender, though.

3. Access the panel by navigating to the 3D view Panel in Blender and click the "+" sign in the upper left corner.

	You will see a tab titled "Brender". Click this tab.

6. From this tab, you can:

	* Resize all objects in the scene by a user input scale. (default = 2)
	* Translate all objects in the x, y, or z direction. (default = 0,0,0)
	* Apply Wireframe Overlays 
		
		* to do this, input the object's common name you wish to overlay in the text box labeled "Wireframe Object Name". (ex. if your scene has objects "000001_Cloth1",...,"009999_Cloth1", you would input "Cloth1") Then click the Wireframe Overlay Button. Note: This may take some time to apply.
	
	* Apply Predefined Cloth Material 
		
		* in the same manor described above, input the Object's common name you wish to apply the material to and click the following button.
		
	* Apply Predefined Cube Material
		** same usage as above.

7. In addition to `.obj` file support, `.json` files and `.strand` files of certain structures are supported.

	* `.json` files of a very specific format are supported for importing animations. Json files come with object files, which are given transformations to create specific objects. In addition, different transformations may be applied to different frames, essentially formating an animation. An example of such a file can be found under `brender/python/developer_scripts/test_documents/first_test.json`. Note: the example file has no `.obj` files with it. In order to test run it, object files with these names must be added. This file is supported under "Import Json as Animation" of the panel. Json files support object transforming by frame (animating), grouping, and naming.
	* The `.strand` file type is unique to the implementers.

