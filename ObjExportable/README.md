# Project Brender
```
Author: Gustavo Lopez 
Date:	10-21-2017
Version: 2.2.0
```
----project description--UnderConstruction------
Brender is a c++ and python package that works in conjunction with OpenGL. The goal is to provide a simple library to export OpenGL animations as .obj files and then import this set into Blender(an open source 3D creation suite) as an editable animation.

## Getting Started

These instructions will help you get a copy of the Brender package on your machine for development and testing your OpenGL animations.

### Prerequisites

What things you will need installed on your system before using Brender and its sample code.

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

### Brender Setup and Sample Run

How to setup the Brender package to be used with the sample.

1. Set Environment Variable

   Set `BRENDER_DIR` to `path/to/ObjExportable/brender-master/brender`

2. Run Cmake and set where the source code is to the `/path/to/sample` folder. Set where to build the binaries to `/path/to/sample/build`. This will create a build folder in the sample directory to store the binaries.

3. You can now run build and run the project.

### Understanding and Using ObjExportables

   The Brender package includes two special classes called **ObjExportables** and **ObjExportManager**. `ObjExportable.h` is a parent class with a set of functions that must be overwritten by the inheriting class to function. *ObjExportables* are how we refer to the objects we want to export. In the sample code, we are exporting a cloth (defined in `Cloth.h`). *ObjExportManagers* are how we refer to and manipulate our objects in a given scene we wish to export. `ObjExportManager.h` is a singleton class that manages the exports throughout your project animation.

#### ObjExportable 

ObjExportable consists of two main functions.
   `exportObj(std::ofstream& outfile)` is a pure virtual function and must be overwritten by the user's inherited class. This should be a user defined function that exports the user-defined object as an .obj file.
   `getObjName()` If this function is not overwritten, each object that is exported will have a default name Object1, Object2, etc. You can overwrite this function in the inherited class to return a custom object name.

##### In our Sample Code

1. **Cloth.h**
	Because Cloth is the object we want to export, we start by setting the Cloth class to inherit the ObjExportable class
	```cpp
	19	class Cloth : public ObjExportable
	```
	Within the Cloth Class, we will add our derived functions that we are overwriting
	```cpp
	45	void exportObj(std::ofstream& outfile);
	46	std::string getObjName();
	```
2. **Cloth.cpp**
	In the function `exportObj`(lines 438-473) the user defines how thier OpenGl Object is translated into an .obj format. Note: ObjExportManager handles the file naming and exporting.
	In the function `getObjName` the user is simply defining a desired object name as a string and returning the value.

#### ObjExportManager

ObjExportManager consists of a few functions that somplify the process of exporting our objects. ObjExportManager is a singleton class and can contain multiple objects to export.
	`setExportDir(std::string export_dir)` This function takes a string as an input to set the export path you'd like for your files. The default export path is "."
	`add(shared_ptr<ObjExportable exportable>)` This function adds an object to the manager to later be exported using the manager's functions.
	`exportObjs(double time)` This function iterates through all objects added to the manager and exports the according .obj file. The file name is the frame number followed by the object's name. The header of each file contains the commented information: object name, frame time, and frame number.
	`exportObjs()` This function does the same as the above, however it does not utilize or export the frame time (defined by the user's scene).

##### In our Sample Code

1. **Scene.h**
	* In scene, we add the private variable pointer "exportables"
	```cpp
	47	ObjExportManager *exportables;
	```
2. **Scene.cpp**
  * In the `init()` function, we initiate the manager singleton by getting the instance
	```cpp
	57	exportables = ObjExportManager::getInstance();
	```
	We also can set the export directory if we choose to here (commented out in sample)
	```cpp
	62	//exportables->setExportDir("EXPORT/PATH/FOLDER NAME");
	```
	Lastly, in the `init()` function, we add the object we wish to export (cloth) into the manager
	```cpp
	63	exportables->add(cloth);
	```
  * In the `step()` function (the function where the frame steps), we export our objects using the manager
	```cpp
	101	exportables->exportObjs(t);
	```
