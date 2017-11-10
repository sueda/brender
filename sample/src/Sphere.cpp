#include "Sphere.h"
#include <iostream>

#include <fstream>

#include "GLSL.h"
#include "Program.h"

#define TINYOBJLOADER_IMPLEMENTATION
#include "tiny_obj_loader.h"

#include <Eigen/Dense>

using namespace std;

void Sphere::load(const std::string &RESOURCE_DIR){
	
	sphereShape = make_shared<Shape>();
	sphereShape->loadMesh(RESOURCE_DIR + "sphere2.obj");

	auto sphere = make_shared<Particle>(sphereShape);
	spheres.push_back(sphere);
	sphere->r = 0.1;
	sphere->x = Vector3d(0.0, 0.2, 0.0);
}

void Sphere::init(){
	sphereShape->init();
}

void Sphere::exportBrender(std::ofstream& outfile) const{
	Eigen::Matrix4d E = Eigen::Matrix4d.Identity();
	// world coordinates of sphere --> particle's position? 
	E(0, 0) = particle.x(x);
	E(0, 1) = particle.x(y);
	E(0, 2) = particle.x(z);

	sphereShape.exportBrender( E , outfile);
}

std::string Sphere::getName() const
{
	string ObjName = "Sphere1_OverwrittenName";
	return ObjName;
}

