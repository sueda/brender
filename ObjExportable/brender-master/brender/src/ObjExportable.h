#pragma once
#include <fstream>
#include <string>
#include <memory>
#include "ObjExportManager.h"


class ObjExportable
{
public:
	ObjExportable() {};
	virtual ~ObjExportable() {}
	virtual void exportObj(std::ofstream& outfile) = 0;	//pure virtual (must be overwritten)
	virtual std::string getObjName() { return ""; }
private:

};