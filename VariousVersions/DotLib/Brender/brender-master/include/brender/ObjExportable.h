#pragma once
#include <fstream>
#include <string>
#include <memory>
//#include "ObjExportManager.h"

namespace brender
{
	class ObjExportable
	{
	public:
		ObjExportable() {};
		virtual ~ObjExportable() {}
		virtual void exportObj(std::ofstream& outfile) = 0;	//=0 makes method pure virtual
															//also makes this class abstract
		virtual std::string getObjName() { return ""; }
	private:

	};
}
