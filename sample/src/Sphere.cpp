#include "Sphere.h"
#include <iostream>

#include <fstream>

#include "GLSL.h"
#include "Program.h"

#include <Eigen/Dense>

#include "Particle.h"
#include "Shape.h"

using namespace std;
using namespace Eigen;

Sphere::Sphere()
{

}

Sphere::~Sphere()
{
}

void Sphere::load(const std::string &RESOURCE_DIR){
	
	shape = make_shared<Shape>();
	shape->loadMesh(RESOURCE_DIR + "sphere2.obj");

	particle = make_shared<Particle>(shape);
	//spheres.push_back(sphere);
	particle->r = 0.1;
	particle->x = Vector3d(0.0, 0.2, 0.0);
}

void Sphere::init(){
	shape->init();
}

void Sphere::tare()
{
	particle->tare();
}

void Sphere::reset()
{
	particle->reset();
}

void Sphere::draw(shared_ptr<MatrixStack> MV, const shared_ptr<Program> prog)
{
	particle->draw(MV, prog);
}

void Sphere::exportBrender(std::ofstream& outfile) const{
	Eigen::Matrix4d T, S;
	S.setIdentity();
	S(0,0) = particle->r;
	S(1,1) = particle->r;
	S(2,2) = particle->r;
	T.setIdentity();
	T.block<3,1>(0,3) = particle->x;

	shape->exportBrender( T*S , outfile);
}

std::string Sphere::getName() const
{
	return "Sphere";
}
