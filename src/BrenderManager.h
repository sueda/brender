/*
 * @author: Gustavo Lopez 10-21-17
 *
 * @version: 1.0
 */

#pragma once

#include <fstream>
#include <chrono>
#include <vector>
#include <memory>
#include <string>
#include <iostream>

class Brenderable;

class BrenderManager
{
private:
	static bool instanceFlag;
	static BrenderManager *manager;
	int frame;
	const char* EXPORT_DIR;
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
	int getFrame() const;
	void exportBrender();									//does not require/use timestamp
	void exportBrender(double time);
	void add(std::shared_ptr<Brenderable> brenderable);
	~BrenderManager()
	{
		instanceFlag = false;
	}
};

