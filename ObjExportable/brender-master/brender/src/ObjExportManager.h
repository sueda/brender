#pragma once

#include <fstream>
#include <chrono>
#include <vector>
#include <memory>
#include <string>
#include <iostream>

class ObjExportable;
class ObjExportManager
{
private:
	static bool instanceFlag;
	static ObjExportManager *manager;
	int frame;
	char* EXPORT_DIR;
	std::vector<std::shared_ptr<ObjExportable>> objExportables;
	ObjExportManager()
	{
		//private constructor
		EXPORT_DIR = ".";
		frame = 0;
	}
public:
	static ObjExportManager* getInstance();
	void setExportDir(std::string export_dir);
	int getFrame();
	void exportObjs();									//does not require/use timestamp
	void exportObjs(double time);
	void add(std::shared_ptr<ObjExportable> exportable);
	~ObjExportManager()
	{
		instanceFlag = false;
	}
};

