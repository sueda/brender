/*
 * @author: Gustavo Lopez 10-21-17
 * 
 * @version: 1.0
 */

#include <math.h>
#include "BrenderManager.h"
#include "Brenderable.h"

using namespace std;

bool BrenderManager::instanceFlag = false;
BrenderManager* BrenderManager::manager = NULL;
BrenderManager* BrenderManager::getInstance()
{
	if (!instanceFlag)
	{
		manager = new BrenderManager();
		instanceFlag = true;
		return manager;
	}
	else
	{
		return manager;
	}
}

void BrenderManager::exportBrender(double time)
{
	bool doExport = false;
	if(fps == 0) {
		// Don't export if fps = 0
		doExport = false;
	}
	if(fps == -1) {
		// Export every frame if fps = -1
		doExport = true;
	} else {
		// Export only if enough time has elapsed
		if(frame == 0) {
			// Always export first frame
			doExport = true;
		} else {
			double dtExport = 1.0/fps;
			if(fmod(time, dtExport) - fmod(time - timeLast, dtExport) < 0.0) {
				doExport = true;
			} else {
				doExport = false;
			}
		}
	}
	timeLast = time;
	if(!doExport) {
		return;
	}
	// Start exporting
	int objNum = 1;
	for (auto brenderable : brenderables) {
		vector<string> names = brenderable->getBrenderNames();
		vector< shared_ptr< ofstream > > outfiles;
		// Initialize files
		for (int i = 0; i < brenderable->getBrenderCount(); ++i) {
			auto outfile = make_shared<ofstream>();
			outfiles.push_back(outfile);

			char filename[512];

			//if object has not been given name
			if (names[i].compare("") == 0) {
				sprintf(filename, "%s/%06d_Object%d.obj", EXPORT_DIR.c_str(), frame, objNum);
			}
			//if object has been given specific name
			else {
				sprintf(filename, "%s/%06d_%s.obj", EXPORT_DIR.c_str(), frame, names[i].c_str());
			}
			//open file
			outfile->open(filename);
			//frame string
			char framestring[50];
			sprintf(framestring, "# frame %06d \n", frame);
			*outfile << framestring;
			//frame time
			char timeval[50];
			sprintf(timeval, "# time %f \n", time);
			*outfile << timeval;
			//obj name
			//if object has not been given name
			if (names[i].compare("") == 0) {
				*outfile << "# name Object" + to_string(objNum) + " \n";
			}
			//if object has been given specific name
			else {
				*outfile << "# name " + names[i] + " \n";
			}
		}
		// Write to files
		brenderable->exportBrender(outfiles);
		// Close files
		for (int i = 0; i < brenderable->getBrenderCount(); ++i) {
			outfiles[i]->close();
		}
		objNum++;
	}
	//Only time frame should be changed/modified
	frame++;
}

void BrenderManager::add(shared_ptr<Brenderable> brenderable)
{
	brenderables.push_back(brenderable);
}

void BrenderManager::setExportDir(string export_dir) 
{	
	EXPORT_DIR = export_dir;
}


