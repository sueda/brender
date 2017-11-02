#ifndef __Sphere__
#define __Sphere__

#include <vector>
#include <memory>

#include <BrenderManager.h>

class Sphere
{
public:
	Sphere();
	virtual ~Sphere();
private:

	std::shared_ptr<Shape> sphereShape;
};

#endif