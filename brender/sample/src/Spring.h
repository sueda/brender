#pragma once
#ifndef __Spring__
#define __Spring__

#include <memory>

class Particle;

class Spring
{
public:
	Spring(std::shared_ptr<Particle> p0, std::shared_ptr<Particle> p1);
	virtual ~Spring();
	
	std::shared_ptr<Particle> p0;
	std::shared_ptr<Particle> p1;
	double E;
	double L;
};

#endif
