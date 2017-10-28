/*
 * @author: Gustavo Lopez 10-21-17
 *
 * @version: 1.0
 */

#pragma once
#include <fstream>
#include <string>
#include <memory>
#include "BrenderManager.h"


class Brenderable
{
public:
	Brenderable() {};
	virtual ~Brenderable() {}
	virtual void exportBrender(std::ofstream& outfile) = 0;	//pure virtual (must be overwritten)
	virtual std::string getName() { return ""; }
private:

};