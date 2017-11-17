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
	
	sphereShape = make_shared<Shape>();
	sphereShape->loadMesh(RESOURCE_DIR + "sphere2.obj");

	auto sphere = make_shared<Particle>(sphereShape);
	//spheres.push_back(sphere);
	sphere->r = 0.1;
	sphere->x = Vector3d(0.0, 0.2, 0.0);
}

void Sphere::init(){
	sphereShape->init();
}

void Sphere::tare()
{
	particle->tare();
}

void Sphere::reset()
{
	particle->reset();
}

void Sphere::step(double t, double h)
{
	auto s = particle;
	Vector3d x0 = s->x;
	double radius = 0.5;
	double a = 2.0*t;
	s->x(2) = radius * sin(a);
	Vector3d dx = s->x - x0;
	s->v = dx/h;
}

void Sphere::draw(shared_ptr<MatrixStack> MV, const shared_ptr<Program> prog)
{
	particle->draw(MV, prog);
}

std::shared_ptr<Particle> Sphere::retParticle()
{
	return particle;
}

void Sphere::exportBrender(std::ofstream& outfile) const{
	Eigen::Matrix4d E;  //Matrix4d.Identity();
	double x, y, z;
	x = particle->x(0);
	y = particle->x(1);
	z = particle->x(2);
	E << 1.0, 0.0, 0.0, x,
		0.0, 1.0, 0.0, y,
		0.0, 0.0, 1.0, z,
		0.0, 0.0, 0.0, 1.0;

	sphereShape->exportBrender( E , outfile);
}

std::string Sphere::getName() const
{
	string ObjName = "Sphere1_OverwrittenName";
	return ObjName;
}

