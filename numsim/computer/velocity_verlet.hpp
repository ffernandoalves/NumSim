/**
 * Book: Numerical Simulation in Molecular Dynamics: 
 *       Numerics, Algorithms, Parallelization, Applications
 * Author: Michael Griebel, Stephan Knapek, Gerhard Zumbusch
 * Date:   September, 2007 (moved to new file on October 29, 2020)
 * Adapted by Fernando Ribeiro Alves, October 29, 2020.
 **/

#ifndef VERLET_HPP
#define VERLET_HPP

#include <cmath>

#define DIM 2
#define sqr(x) ((x)*(x))

typedef double real;

typedef struct {
    real m;         // mass
    real x[DIM];    // position
    real v[DIM];    // velocity
    real F[DIM];    // force
} Particle;

class GravitationStoermerVerletParticle: public Particle{
    private:
        real F_old[DIM];

    public:
        GravitationStoermerVerletParticle();
        void updateX(real delta_t);
        void updateV(real delta_t);
        void force(GravitationStoermerVerletParticle *j);
};

void GravitationStoermerVerletParticle::updateX(real delta_t){
    real a = delta_t * .5 / m;
    
    for (int d = 0; d < DIM; d++){
        x[d] += delta_t * (v[d] + a * F[d]);
        F_old[d] = F[d];
    }
}

void GravitationStoermerVerletParticle::updateV(real delta_t){
    real a = delta_t * .5 / m;

    for (int d = 0; d < DIM; d++){
        v[d] += a * (F[d] + F_old[d]);
    }
}

void GravitationStoermerVerletParticle::force(GravitationStoermerVerletParticle *j){
    real r = 0;

    for (int d = 0; d < DIM; d++){
        r += sqr(j->x[d] - x[d]);
    }

    real f = m * j->m / (sqrt(r) * r);

    for (int d = 0; d < DIM; d++){
        F[d] += f * (j->x[d] - x[d]);
        j->F[d] -= f * (j->x[d] - x[d]);
    }
}
#endif //VERLET_HPP