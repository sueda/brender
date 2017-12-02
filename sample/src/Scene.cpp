#include <iostream>

#include "GLSL.h"
#include "Scene.h"
#include "Particle.h"
#include "Cloth.h"
#include "Sphere.h"
#include "Program.h"

using namespace std;
using namespace Eigen;

Scene::Scene() :
	t(0.0),
	h(1e-2),
	grav(0.0, 0.0, 0.0)
{
}

Scene::~Scene()
{
}

void Scene::load(const string &RESOURCE_DIR)
{
	// Units: meters, kilograms, seconds
	h = 5e-3;
	
	grav << 0.0, 0.0, -9.8;
	
	int rows = 20;
	int cols = 20;
	double mass = 0.1;
	double stiffness = 2e1;
	double bending = 2e1;
	Vector2d damping(1.0, 1.0);
	Vector3d x00(-0.25, 0.0, 0.25);
	Vector3d x01(0.25, 0.0, 0.25);
	Vector3d x10(-0.25, -0.5, 0.25);
	Vector3d x11(0.25, -0.5, 0.25);
	cloth = make_shared<Cloth>(rows, cols, x00, x01, x10, x11, mass, stiffness, bending, damping);
	
	sphere = make_shared<Sphere>();
	sphere->load(RESOURCE_DIR);
}

void Scene::init()
{
	sphere->init();
	cloth->init();
	brender = BrenderManager::getInstance();
	/*
	 * Edit the following commented line to choose a specific
	 * file path for the exported obj files
	 */
	//brender->setExportDir("EXPORT/PATH/FOLDER NAME");
	brender->setFPS(30.0);
    brender->add(cloth);
    brender->add(sphere);
	brender->exportBrender(t);
}

void Scene::tare()
{
	sphere->tare();
	cloth->tare();
}

void Scene::reset()
{
	t = 0.0;
	sphere->reset();
	cloth->reset();
}

void Scene::step()
{
	t += h;
    
    // Move the big sphere
    auto p = sphere->particle;
    Vector3d x0 = p->x;
    double radius = 0.5;
    double a = 2.0*t;
    p->x(1) = -radius * sin(a);
    Vector3d dx = p->x - x0;
    p->v = dx/h;
	
	// Simulate the cloth
	cloth->step(h, grav, sphere);

    // Export Obj Files
	brender->exportBrender(t);
}

void Scene::draw(shared_ptr<MatrixStack> MV, const shared_ptr<Program> prog) const
{
	glUniform3fv(prog->getUniform("kdFront"), 1, Vector3f(1.0, 1.0, 1.0).data());
	sphere->draw(MV,prog);
	cloth->draw(MV, prog);
}
