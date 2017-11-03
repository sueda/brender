#pragma once
#ifndef __Sphere__
#define __Sphere__

#include <vector>
#include <memory>

#include <BrenderManager.h>
#include <Brenderable.h>

class Sphere
{
public:
	Sphere();
	virtual ~Sphere();
	void load(const std::string &RESOURCE_DIR);
	void init();
	void exportSphere();
private:
	// holds posbuf, norbuf, and texbuf
	std::shared_ptr<Shape> sphereShape;
	std::vector< std::shared_ptr<Particle> > spheres;
};

#endif