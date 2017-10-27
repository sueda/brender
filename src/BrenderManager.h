#pragma once

#include <fstream>
#include <chrono>
#include <vector>
#include <memory>
/*
 * @author: Gustavo Lopez 10-21-17
 *
 * @version: 1.0
 */

#include <string>
#include <iostream>

class Brenderable;
class BrenderManager
{
private:
	static bool instanceFlag;
	static BrenderManager *manager;
	int frame;
	char* EXPORT_DIR;
	std::vector<std::shared_ptr<Brenderable> > brenderables;
	BrenderManager()
	{
		//private constructor
		EXPORT_DIR = ".";
		frame = 0;
	}
public:
	static BrenderManager* getInstance();
	void setExportDir(std::string export_dir);
	int getFrame();
	void export();									//does not require/use timestamp
	void export(double time);
	void add(std::shared_ptr<Brenderable> brenderable);
	~BrenderManager()
	{
		instanceFlag = false;
	}
};

