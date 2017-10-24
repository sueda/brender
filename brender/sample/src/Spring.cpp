#include "Spring.h"
#include "Particle.h"

using namespace std;
using namespace Eigen;

Spring::Spring(shared_ptr<Particle> p0, shared_ptr<Particle> p1) :
	E(1.0)
{
	assert(p0);
	assert(p1);
	assert(p0 != p1);
	this->p0 = p0;
	this->p1 = p1;
	Vector3d x0 = p0->x;
	Vector3d x1 = p1->x;
	Vector3d dx = x1 - x0;
	L = dx.norm();
	assert(L > 0.0);
}

Spring::~Spring()
{
	
}
