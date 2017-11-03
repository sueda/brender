#include "Sphere.h"
#include <iostream>

#include <fstream>

#include "GLSL.h"
#include "Program.h"

#define TINYOBJLOADER_IMPLEMENTATION
#include "tiny_obj_loader.h"

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

void Sphere::exportBrender(std::ofstream& outfile){
	//vertex positions
	for (int i = 0; i < posBuf.size(); i = i + 3) {
		char vert[50];
		sprintf(vert, "v %f %f %f\n", posBuf[i], posBuf[i + 1], posBuf[i + 2]);
		outfile << vert;
	}
	//texture coordinates
	for (int i = 0; i < texBuf.size(); i = i + 2) {
		char vtex[50];
		sprintf(vtex, "vt %f %f\n", texBuf[i], texBuf[i + 1]);
		outfile << vtex;
	}
	//normal vectors
	for (int i = 0; i < norBuf.size(); i = i + 3) {
		char norm[50];
		sprintf(norm, "vn %f %f %f\n", norBuf[i], norBuf[i + 1], norBuf[i + 2]);
		outfile << norm;
	}
	//faces--Using Triangle Strips

	//
	//face
	//f vertex/texture/normal1 vertex/texture/normal2 vertex/texture/normal3 
	// posbuf holds all vertices. each face has 3 vertices.
	for(int i = 1; i < (posBuf.size() / 3); i = i + 3 ){
		char face[50];
		int f1,f2,f3;
		f1 = i;
		f2 = i+1;
		f3 = i+3;

		sprintf(face, "f %i/%i/%i %i/%i/%i %i/%i/%i\n", f1, f1, f1, f2, f2, f2, f3, f3, f3);
		outfile << face;
	}
	
	// for (int j = 0; j < rows*2-2; j = j+2) {
	// 	///one row:
	// 	for (int i = 0; i < cols*2-2; i++) {
	// 		char facetri[50];
	// 		int strt = cols*j;
	// 		int v1, v2, v3;
	// 		v1 = eleBuf[strt+ i] + 1;
	// 		v2 = eleBuf[strt+ i + 1] + 1;
	// 		v3 = eleBuf[strt+ i + 2] + 1;

	// 		sprintf(facetri, "f %i/%i/%i %i/%i/%i %i/%i/%i\n", v1, v1, v1, v2, v2, v2, v3, v3, v3);
	// 		outfile << facetri;
	// 	}
	// }	
}

std::string Sphere::getName()
{
	string ObjName = "Sphere1_OverwrittenName";
	return ObjName;
}

