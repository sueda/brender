//ObjExportableCpp
//
// A single-header library for exporting OpenGl animations as a set of 
//	.obj files by Gustavo Lopez under Dr. Shinjiro Sueda.
// 
#pragma once

#ifndef OBJEXPORTABLE_H
#define OBJEXPORTABLE_H

#include <fstream>
#include <string>
#include <memory>

namespace Brender {
	class ObjExportable {
	public:
		ObjExportable() {};
		virtual ~ObjExportable() {}
		virtual void exportObj(std::ofstream& outfile) = 0;	// pure virtual
		virtual std::string getObjName() {return "";} // overwrite derived
													// method to name
	}
}

#endif	// OBJEXPORTABLE_H