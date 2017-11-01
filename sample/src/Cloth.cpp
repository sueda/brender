#include <iostream>

#define GLM_FORCE_RADIANS
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "Cloth.h"
#include "Particle.h"
#include "Spring.h"
#include "MatrixStack.h"
#include "Program.h"
#include "GLSL.h"

using namespace std;
using namespace Eigen;

shared_ptr<Spring> createSpring(const shared_ptr<Particle> p0, const shared_ptr<Particle> p1, double E)
{
	auto s = make_shared<Spring>(p0, p1);
	s->E = E;
	Vector3d x0 = p0->x;
	Vector3d x1 = p1->x;
	Vector3d dx = x1 - x0;
	s->L = dx.norm();
	return s;
}

Cloth::Cloth(int rows, int cols,
			 const Vector3d &x00,
			 const Vector3d &x01,
			 const Vector3d &x10,
			 const Vector3d &x11,
			 double mass,
			 double stiffness,
			 double bending,
			 const Vector2d &damping)
{
	assert(rows > 1);
	assert(cols > 1);
	assert(mass > 0.0);
	assert(stiffness > 0.0);
	
	this->rows = rows;
	this->cols = cols;
	this->damping = damping;
	
	// Create particles
	n = 0;
	double r = 0.01; // Used for collisions
	int nVerts = rows*cols;
	for(int i = 0; i < rows; ++i) {
		double u = i / (rows - 1.0);
		Vector3d x0 = (1 - u)*x00 + u*x10;
		Vector3d x1 = (1 - u)*x01 + u*x11;
		for(int j = 0; j < cols; ++j) {
			double v = j / (cols - 1.0);
			Vector3d x = (1 - v)*x0 + v*x1;
			auto p = make_shared<Particle>();
			particles.push_back(p);
			p->r = r;
			p->x = x;
			p->v << 0.0, 0.0, 0.0;
			p->m = mass/(nVerts);
			// Pin two particles
			if(i == 0 && (j == 0 || j == cols-1)) {
				p->fixed = true;
				p->i = -1;
			} else {
				p->fixed = false;
				p->i = n;
				n += 3;
			}
		}
	}
	
	// Create x springs
	for(int i = 0; i < rows; ++i) {
		for(int j = 0; j < cols-1; ++j) {
			int k0 = i*cols + j;
			int k1 = k0 + 1;
			springs.push_back(createSpring(particles[k0], particles[k1], stiffness));
		}
	}
	
	// Create y springs
	for(int j = 0; j < cols; ++j) {
		for(int i = 0; i < rows-1; ++i) {
			int k0 = i*cols + j;
			int k1 = k0 + cols;
			springs.push_back(createSpring(particles[k0], particles[k1], stiffness));
		}
	}
	
	// Create shear springs
	for(int i = 0; i < rows-1; ++i) {
		for(int j = 0; j < cols-1; ++j) {
			int k00 = i*cols + j;
			int k10 = k00 + 1;
			int k01 = k00 + cols;
			int k11 = k01 + 1;
			springs.push_back(createSpring(particles[k00], particles[k11], stiffness));
			springs.push_back(createSpring(particles[k10], particles[k01], stiffness));
		}
	}
	
	// Create x bending springs
	for(int i = 0; i < rows; ++i) {
		for(int j = 0; j < cols-2; ++j) {
			int k0 = i*cols + j;
			int k2 = k0 + 2;
			springs.push_back(createSpring(particles[k0], particles[k2], bending));
		}
	}
	
	// Create y bending springs
	for(int j = 0; j < cols; ++j) {
		for(int i = 0; i < rows-2; ++i) {
			int k0 = i*cols + j;
			int k2 = k0 + 2*cols;
			springs.push_back(createSpring(particles[k0], particles[k2], bending));
		}
	}
	
	// Build vertex buffers
	posBuf.clear();
	norBuf.clear();
	texBuf.clear();
	eleBuf.clear();
	posBuf.resize(nVerts*3);
	norBuf.resize(nVerts*3);
	updatePosNor();
	// Texture coordinates (don't change)
	for(int i = 0; i < rows; ++i) {
		for(int j = 0; j < cols; ++j) {
			texBuf.push_back(i/(rows-1.0));
			texBuf.push_back(j/(cols-1.0));
		}
	}
	// Elements (don't change)
	for(int i = 0; i < rows-1; ++i) {
		for(int j = 0; j < cols; ++j) {
			int k0 = i*cols + j;
			int k1 = k0 + cols;
			// Triangle strip
			eleBuf.push_back(k0);
			eleBuf.push_back(k1);
		}
	}
}

Cloth::~Cloth()
{
}

void Cloth::tare()
{
	for(int k = 0; k < (int)particles.size(); ++k) {
		particles[k]->tare();
	}
}

void Cloth::reset()
{
	for(int k = 0; k < (int)particles.size(); ++k) {
		particles[k]->reset();
	}
	updatePosNor();
}

void Cloth::updatePosNor()
{
	// Position
	for(int i = 0; i < rows; ++i) {
		for(int j = 0; j < cols; ++j) {
			int k = i*cols + j;
			Vector3d x = particles[k]->x;
			posBuf[3*k+0] = x(0);
			posBuf[3*k+1] = x(1);
			posBuf[3*k+2] = x(2);
		}
	}
	// Normal
	///Make the V and F matrices here?
	for(int i = 0; i < rows; ++i) {
		for(int j = 0; j < cols; ++j) {
			// Each particle has four neighbors
			//
			//      v1
			//     /|\
			// u0 /_|_\ u1
			//    \ | /
			//     \|/
			//      v0
			//
			// Use these four triangles to compute the normal
			int k = i*cols + j;
			int ku0 = k - 1;
			int ku1 = k + 1;
			int kv0 = k - cols;
			int kv1 = k + cols;
			Vector3d x = particles[k]->x;
			Vector3d xu0, xu1, xv0, xv1, dx0, dx1, c;
			Vector3d nor(0.0, 0.0, 0.0);
			int count = 0;
			// Top-right triangle
			if(j != cols-1 && i != rows-1) {
				xu1 = particles[ku1]->x;
				xv1 = particles[kv1]->x;
				dx0 = xu1 - x;
				dx1 = xv1 - x;
				c = dx0.cross(dx1);
				nor += c.normalized();
				++count;
			}
			// Top-left triangle
			if(j != 0 && i != rows-1) {
				xu1 = particles[kv1]->x;
				xv1 = particles[ku0]->x;
				dx0 = xu1 - x;
				dx1 = xv1 - x;
				c = dx0.cross(dx1);
				nor += c.normalized();
				++count;
			}
			// Bottom-left triangle
			if(j != 0 && i != 0) {
				xu1 = particles[ku0]->x;
				xv1 = particles[kv0]->x;
				dx0 = xu1 - x;
				dx1 = xv1 - x;
				c = dx0.cross(dx1);
				nor += c.normalized();
				++count;
			}
			// Bottom-right triangle
			if(j != cols-1 && i != 0) {
				xu1 = particles[kv0]->x;
				xv1 = particles[ku1]->x;
				dx0 = xu1 - x;
				dx1 = xv1 - x;
				c = dx0.cross(dx1);
				nor += c.normalized();
				++count;
			}
			nor /= count;
			nor.normalize();
			norBuf[3*k+0] = nor(0);
			norBuf[3*k+1] = nor(1);
			norBuf[3*k+2] = nor(2);
		}
	}
}

void Cloth::step(double h, const Vector3d &grav, const vector< shared_ptr<Particle> > spheres)
{
	typedef Triplet<double> T;
	std::vector<T> A_; // triplet format
	SparseMatrix<double> A; // compressed row format
	VectorXd b;
	VectorXd v;
	Matrix3d I = Matrix3d::Identity();
	
	A.resize(n,n);
	b.resize(n);
	v.resize(n);
	b.setZero();
	v.setZero();
	
	// Mass, velocity, gravity
	for(int k = 0; k < (int)particles.size(); ++k) {
		auto p = particles[k];
		if(!p->fixed) {
			int i0 = p->i;
			for(int i = 0; i < 3; ++i) {
				A_.push_back(T(i0+i, i0+i, p->m*(1.0 + h*damping(0))));
			}
			b.segment<3>(p->i) += p->m*p->v + h*p->m*grav;
			v.segment<3>(p->i) = p->v;
		}
	}
	
	// Springs
	// Now loop through all the springs
	for(int k = 0; k < (int)springs.size(); ++k) {
		auto s = springs[k];
		auto p0 = s->p0;
		auto p1 = s->p1;
		int i0 = p0->i;
		int i1 = p1->i;
		Vector3d x0 = p0->x;
		Vector3d x1 = p1->x;
		Vector3d dx = x1 - x0;
		double dxtdx = dx.dot(dx);
		double l = sqrt(dxtdx);
		double L = s->L;
		Vector3d fs = s->E*(l-L)*dx/l;
		if(!p0->fixed) {
			b.segment<3>(i0) += h*fs;
		}
		if(!p1->fixed) {
			b.segment<3>(i1) -= h*fs;
		}
		Matrix3d dxdxt = dx*dx.transpose();
		double lLl = (l-L)/l;
		Matrix3d Ks = h*h*damping(1)*s->E/dxtdx*((1.0-lLl)*dxdxt + lLl*dxtdx*I);
		for(int i = 0; i < 3; ++i) {
			for(int j = 0; j < 3; ++j) {
				double Ksij = Ks(i,j);
				if(!p0->fixed && !p1->fixed) {
					A_.push_back(T(i0+i, i0+j, Ksij));
					A_.push_back(T(i0+i, i1+j, -Ksij));
					A_.push_back(T(i1+i, i0+j, -Ksij));
					A_.push_back(T(i1+i, i1+j, Ksij));
				} else if(!p0->fixed) {
					A_.push_back(T(i0+i, i0+j, Ksij));
				} else if(!p1->fixed) {
					A_.push_back(T(i1+i, i1+j, Ksij));
				}
			}
		}
	}
	A.setFromTriplets(A_.begin(), A_.end());
	
//	MatrixXd foo(A);
//	cout << foo << endl;
//	cout << b << endl;
	
	// Solve
//	SimplicialLDLT<SparseMatrix<double> > solver;
//	v = solver.compute(A).solve(b);
	ConjugateGradient< SparseMatrix<double> > cg;
	cg.setMaxIterations(25);
	cg.setTolerance(1e-3);
	cg.compute(A);
	v = cg.solveWithGuess(b, v);
	
	// Disassembly
	for(int k = 0; k < (int)particles.size(); ++k) {
		auto p = particles[k];
		if(!p->fixed) {
			p->v = v.segment<3>(p->i);
		}
	}
	for(int k = 0; k < (int)particles.size(); ++k) {
		auto p = particles[k];
		if(!p->fixed) {
			p->x += h*p->v;
		}
	}
	
	// Collisions
	for(int i = 0; i < (int)particles.size(); ++i) {
		auto p = particles[i];
		double rp = p->r;
		Vector3d xp = p->x;
		for(int j = 0; j < (int)spheres.size(); ++j) {
			auto s = spheres[j];
			double rs = s->r;
			Vector3d xs = s->x;
			Vector3d dx = xp - xs;
			double l = dx.norm();
			double penetration = l - (rs + rp);
			if(penetration < 0.0) {
				// Colliding
				Vector3d nor = dx/l;
				p->x = xs + (rp+rs)*nor;
				// Remove the normal component from the velocity
				Vector3d vp = p->v;
				Vector3d vproj = vp.dot(nor)*nor;
				Vector3d vtan = vp - vproj;
				double friction = 0.0;
				p->v = (1.0-friction)*vtan + s->v.dot(nor)*nor;
			}
		}
	}
	
	// Update position and normal buffers
	updatePosNor();
}

void Cloth::init()
{
	glGenBuffers(1, &posBufID);
	glBindBuffer(GL_ARRAY_BUFFER, posBufID);
	glBufferData(GL_ARRAY_BUFFER, posBuf.size()*sizeof(float), &posBuf[0], GL_DYNAMIC_DRAW);
	
	glGenBuffers(1, &norBufID);
	glBindBuffer(GL_ARRAY_BUFFER, norBufID);
	glBufferData(GL_ARRAY_BUFFER, norBuf.size()*sizeof(float), &norBuf[0], GL_DYNAMIC_DRAW);
	
	glGenBuffers(1, &texBufID);
	glBindBuffer(GL_ARRAY_BUFFER, texBufID);
	glBufferData(GL_ARRAY_BUFFER, texBuf.size()*sizeof(float), &texBuf[0], GL_STATIC_DRAW);
	
	glGenBuffers(1, &eleBufID);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eleBufID);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, eleBuf.size()*sizeof(unsigned int), &eleBuf[0], GL_STATIC_DRAW);
	
	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
	
	assert(glGetError() == GL_NO_ERROR);
}

void Cloth::draw(shared_ptr<MatrixStack> MV, const shared_ptr<Program> p) const
{
	// Draw mesh
	glUniform3fv(p->getUniform("kdFront"), 1, Vector3f(1.0, 0.0, 0.0).data());
	glUniform3fv(p->getUniform("kdBack"),  1, Vector3f(1.0, 1.0, 0.0).data());
	MV->pushMatrix();
	glUniformMatrix4fv(p->getUniform("MV"), 1, GL_FALSE, glm::value_ptr(MV->topMatrix()));
	int h_pos = p->getAttribute("aPos");
	glEnableVertexAttribArray(h_pos);
	glBindBuffer(GL_ARRAY_BUFFER, posBufID);
	glBufferData(GL_ARRAY_BUFFER, posBuf.size()*sizeof(float), &posBuf[0], GL_DYNAMIC_DRAW);
	glVertexAttribPointer(h_pos, 3, GL_FLOAT, GL_FALSE, 0, (const void *)0);
	int h_nor = p->getAttribute("aNor");
	glEnableVertexAttribArray(h_nor);
	glBindBuffer(GL_ARRAY_BUFFER, norBufID);
	glBufferData(GL_ARRAY_BUFFER, norBuf.size()*sizeof(float), &norBuf[0], GL_DYNAMIC_DRAW);
	glVertexAttribPointer(h_nor, 3, GL_FLOAT, GL_FALSE, 0, (const void *)0);
	int h_tex = p->getAttribute("aTex");
	glEnableVertexAttribArray(h_tex);
	glBindBuffer(GL_ARRAY_BUFFER, texBufID);
	glVertexAttribPointer(h_tex, 2, GL_FLOAT, GL_FALSE, 0, (const void *)0);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eleBufID);
	for(int i = 0; i < rows; ++i) {
		glDrawElements(GL_TRIANGLE_STRIP, 2*cols, GL_UNSIGNED_INT, (const void *)(2*cols*i*sizeof(unsigned int)));
	}
	glDisableVertexAttribArray(h_tex);
	glDisableVertexAttribArray(h_nor);
	glDisableVertexAttribArray(h_pos);
	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
	MV->popMatrix();
}

void Cloth::export(std::ofstream& outfile)
{
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
	for (int j = 0; j < rows*2-2; j = j+2) {
		///one row:
		for (int i = 0; i < cols*2-2; i++) {
			char facetri[50];
			int strt = cols*j;
			int v1, v2, v3;
			v1 = eleBuf[strt+ i] + 1;
			v2 = eleBuf[strt+ i + 1] + 1;
			v3 = eleBuf[strt+ i + 2] + 1;

			sprintf(facetri, "f %i/%i/%i %i/%i/%i %i/%i/%i\n", v1, v1, v1, v2, v2, v2, v3, v3, v3);
			outfile << facetri;
		}
	}		
}

std::string Cloth::getName()
{
	string ObjName = "Cloth1_OverwrittenName";
	return ObjName;
}
