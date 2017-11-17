#pragma once
#ifndef __Sphere__
#define __Sphere__

#include <vector>
#include <memory>

#include <BrenderManager.h>
#include <Brenderable.h>

class Shape;
class Particle;
class MatrixStack;
class Program;

class Sphere : public Brenderable
{
public:
	Sphere();
	virtual ~Sphere();
	void load(const std::string &RESOURCE_DIR);
	void init();
	void tare();
	void reset();
	void step(double t, double h);
	void draw(std::shared_ptr<MatrixStack> MV, const std::shared_ptr<Program> prog);
	std::shared_ptr<Particle> retParticle();
	void exportBrender(std::ofstream& outfile) const;
	std::string getName() const;
	//
private:
	// holds posbuf, norbuf, and texbuf
	//reference variable set in the initialization list
	//
	std::shared_ptr<Shape> sphereShape;
	std::shared_ptr<Particle> particle;
};

#endif