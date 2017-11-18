#pragma once
#ifndef __Cloth__
#define __Cloth__

#include <vector>
#include <memory>

#define EIGEN_DONT_ALIGN_STATICALLY
#include <Eigen/Dense>
#include <Eigen/Sparse>

#include "Brenderable.h"

class Particle;
class Sphere;
class Spring;
class MatrixStack;
class Program;

class Cloth : public Brenderable
{
public:
	EIGEN_MAKE_ALIGNED_OPERATOR_NEW
	
	Cloth(int rows, int cols,
		  const Eigen::Vector3d &x00,
		  const Eigen::Vector3d &x01,
		  const Eigen::Vector3d &x10,
		  const Eigen::Vector3d &x11,
		  double mass,
		  double stiffness,
		  double bending,
		  const Eigen::Vector2d &damping);
	virtual ~Cloth();
	
	void tare();
	void reset();
	void updatePosNor();
	void step(double h, const Eigen::Vector3d &grav, const std::shared_ptr<Sphere> sphere);
	void init();
	void draw(std::shared_ptr<MatrixStack> MV, const std::shared_ptr<Program> p) const;
	/*
	 * The following functions are used to overwrite Brenderable.h
	 * functions and be able to utilize BrenderManager Functions
	 */
	void exportBrender(std::ofstream& outfile) const;
	std::string getName() const;

private:
	int rows;
	int cols;
	int n;
	Eigen::Vector2d damping;
	std::vector< std::shared_ptr<Particle> > particles;
	std::vector< std::shared_ptr<Spring> > springs;
	
	std::vector<unsigned int> eleBuf;
	std::vector<float> posBuf;
	std::vector<float> norBuf;
	std::vector<float> texBuf;
	unsigned eleBufID;
	unsigned posBufID;
	unsigned norBufID;
	unsigned texBufID;
};

#endif
