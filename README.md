# Project Brender

**Brender** is a C++ and Python package. Brender is a simple library to export animations as .obj files and then import this set into Blender(an open source 3D creation suite) as an editable animation, along with additional features and functionalities.

**Authors**
  * Kyle Piddington (2016-2017)
  * Gustavo Lopez (2017-2018)
  * Feras Khemakhem (2018-2019)
  * Nicholas Weidner (2017-2021)
  * Shinjiro Sueda (2016-)

## Getting Started

These instructions will help you get a copy of the Brender package on your machine for developing and testing your OpenGL animations.

### Prerequisites

What you will need installed on your system before using Brender and its sample code.

1. The following Libraries are used in the sample code. Get the source code for each.

  * **GLM** (http://glm.g-truc.net)
  * **GLFW** (http://www.glfw.org)
  * **GLEW** (http://glew.sourceforge.net): (for windows: get the windows binaries)
  * **EIGEN** (http://eigen.tuxfamily.org)

2. Set up the Environment Variables. (This ensures that the sample code will be made properly)

  * Set `GLM_INCLUDE_DIR` to `/path/to/GLM`
  * Set `GLFW_DIR` to `/path/to/GLFW`
  * Set `GLEW_DIR` to `/path/to/GLEW`
  * Set `EIGEN3_INCLUDE_DIR` to `/path/to/EIGEN`

3. **Cmake** (https://cmake.org/download/) is used to build the projects using the included `CMakeLists.txt` file.

### How-to Videos

These links require TAMU access.

  * [Set up brender](https://drive.google.com/file/d/1uSpye6BvVed5ccGZGErH23BjtkYGqC0O/view?usp=sharing)
  * [Import obj as anim](https://drive.google.com/file/d/1-64uqbk60m526nzMDgW4CjbkAMU5OVsx/view?usp=sharing)
  * [Scene backdrop](https://drive.google.com/file/d/1UAbzINyDLnSoIOKwEG2ax-Ey3sD4aq61/view?usp=sharing)
  * [Setup light](https://drive.google.com/file/d/17up8yyenXgDr1Fvd9RubHPnRbeRupuDk/view?usp=sharing)
  * [Custom Material](https://drive.google.com/file/d/1wSoHs16hZJIIhM3jK4KqRSZy8M4hEt3Q/view?usp=sharing)
  * [Setup camera](https://drive.google.com/file/d/1QxFkF1ylOs2pvOnOIi3iwFch8RYQ-87X/view?usp=sharing)
  * [Render scene](https://drive.google.com/file/d/1Fz7ytx2OzpgmYTDVVSTRA_X7Hr6XzB8p/view?usp=sharing)
  * [Video editor](https://drive.google.com/file/d/1eZzOgehqCjMzauzfVkC8oFAUxr_pSal8/view?usp=sharing)

### Brender Setup and Sample Run

How to setup the Brender package to be used with the sample.

1. Set Environment Variable

   Set `BRENDER_DIR` to *path/to* `/brender`

   NOTE: Make sure to use forward slashes (/) for the Brender environment variable.

2. Run Cmake and set "Where is the source code:" to the */path/to/* `brender/sample` folder. Set "Where to build the binaries" to */path/to* `/sample/build`. This will create a build folder in the sample directory to store the binaries.

3. Now navigate to the `build` directory and open the project file (`sample.sln` in Visual Studio).

4. Set the project to "Set as startup Project"

5. Open the project properties and navigate to the "Configuration Properties>Debugging" tab. In the Debugging window, set `Command Arguments` to `../resources`. **NOTE:** It is suggested that you run the sample code in Release mode. *There are currently issues with the sample code running in debug mode on some machines.* (Note that if you run in release mode, you must apply the same setting to the "Release" configuration)

6. You may now build and run the code. Press spacebar to play the animation and export frames. Press the spacebar again to stop. **Note:** exported files will be, by default, in the build folder. See **Understanding and Using Brenderables** section for details.

### Understanding and Using Brenderables

   The Brender package includes two special classes called **Brenderables** and **BrenderManager**. `Brenderable.h` is a parent class with a set of functions that must be overwritten by the inheriting class to function. *Brenderables* are how we refer to the objects we want to export. In the sample code, we are exporting a cloth (defined in `Cloth.h`). *BrenderManagers* are how we refer to and manipulate our objects in a given scene we wish to export. `BrenderManager.h` is a singleton class that manages the exports throughout your project animation.

#### Brenderable 

Brenderable consists of two main functions.

   `exportBrender(std::ofstream& outfile)` is a pure virtual function and must be overwritten by the user's inherited class. This should be a user defined function that exports the user-defined object as an .obj file.

   `getName()` If this function is not overwritten, each object that is exported will have a default name: Object1, Object2, etc. You can overwrite this function in the inherited class to return a custom object name.

##### In our Sample Code

1. **Cloth.h**

   * Because Cloth is the object we want to export, we start by setting the Cloth class to inherit the Brenderable class
	```cpp
	19	class Cloth : public Brenderable
	```
   * Within the Cloth Class, we will add our derived functions that we are overwriting
	```cpp
	45	void exportBrender(std::ofstream& outfile);
	46	std::string getName();
	```

2. **Cloth.cpp**

   * In the function `exportBrender`(lines 438-473) the user defines how thier OpenGl Object is translated into an .obj format. Note: BrenderManager handles the file naming and exporting.

   * In the function `getName` the user is simply defining a desired object name as a string and returning the value.

#### BrenderManager

BrenderManager consists of a few functions that simplify the process of exporting our objects. BrenderManager is a singleton class and can contain multiple objects to export.

   `setExportDir(std::string export_dir)` This function takes a string as an input to set the export path you'd like for your files. The default export path is "."

   `add(shared_ptr<Brenderable brenderable>)` This function adds an object to the manager to later be exported using the manager's functions.

   `exportBrender(double time)` This function iterates through all objects added to the manager and exports the according .obj file. The file name is the frame number followed by the object's name. The header of each file contains the commented information: object name, frame time, and frame number.

   `exportBrender()` This function does the same as the above, however it does not utilize or export the frame time (defined by the user's scene).

##### In our Sample Code

1. **Scene.h**
	* In scene, we add the private variable pointer "brender"
	```cpp
	47	BrenderManager *brender;
	```
2. **Scene.cpp**
  * In the `init()` function, we initiate the manager singleton by getting the instance
	```cpp
	57	brender = BrenderManager::getInstance();
	```
	We also can set the export directory if we choose to here (commented out in sample)
	```cpp
	62	//brender->setExportDir("EXPORT/PATH/FOLDER NAME");
	```
	Lastly, in the `init()` function, we add the object we wish to export (cloth) into the manager
	```cpp
	63	brender->add(cloth);
	```
  * In the `step()` function (the function where the frame steps), we export our objects using the manager
	```cpp
	101	brender->exportObjs(t);
	```

## Exporting Files

The following gives simple instructions to run the Sample code and obtain a set of exported .obj files from the OpenGL animation.

1. Build and Run the Project in either Debug or Release mode. Note: Release Mode will run the animation faster.
2. Hit the **spacebar** on the keyboard to begin the animation. 

   NOTE: Because our manager is exporting each time the animation takes a step in the `step()` function of `Scene.cpp`, our files are now being exported to the designated directory.
   
3. Hit **spacebar** again to stop the animation. Stopping the animation stops the exporting. Therefore, simply run the animation as long as you want the exported animation to run.
4. If you chose to overwrite the default directory, all your .obj files should now be in the designated directory, ready for import to Blender. (If you did not overwrite the destination path, all your files should be in the same folder as your build.)

## Importing to Blender

The following gives simple instructions on how to import the exported files from your animation to Blender.

1. Open Blender. (Delete default cube)
2. Change environment (at the top) from **Default** to **Scripting**.
3. In the Scripting window, Select **Open** and navigate to /path/to/brender/`python/brender_imports/blender_import_obj_anim.py` and hit the `enter` key or click **Open Text Block**.
4. Once the code is open in the scripting panel, click **Run Script**.

   Note: This added a new option to the import menu.

5. With the file browser open, select all the .obj files that were previously exported from the Sample code. Note: If all the files in your directory are to be imported, simply select one file and press the `a` key twice.
6. With all the desired files selected, click **Import OBJ As Animation**
7. By default, all obj files are selected and in view. Return to the **Default** Environment at the top of the window. Press the `h` key twice to hide all frames except the current frame.
8. You now have your animation imported. You can scrub through the timeline to view each frame, or simply hit the **Play** button at the bottom of the animation timeline.
