/* -*- c++ -*- */
#ifndef CPU_DENSEGRAPHANNEALER_H__
#define CPU_DENSEGRAPHANNEALER_H__

#include <common/Common.h>
#include <cpu/Random.h>

namespace sqaod {

template<class real>
class CPUDenseGraphAnnealer {

    typedef EigenMatrixType<real> EigenMatrix;
    typedef EigenRowVectorType<real> EigenRowVector;
    typedef MatrixType<real> Matrix;
    typedef VectorType<real> Vector;

public:
    CPUDenseGraphAnnealer();
    ~CPUDenseGraphAnnealer();

    void seed(unsigned long seed);

    void getProblemSize(int *N, int *m) const;

    void setProblem(const Matrix &W, OptimizeMethod om);

    void setNumTrotters(int m);

    real get_minE() const;

    const Vector &get_E() const;

    const BitsArray &get_x() const;

    const BitsArray &get_q() const;

    void get_hJc(Vector *h, Matrix *J, real *c) const;

    void randomize_q();

    void calculate_E();

    void initAnneal();

    void finAnneal();

    void annealOneStep(real G, real kT);
    
private:    
    void syncBits();
    
    Random random_;
    int N_, m_;
    OptimizeMethod om_;
    Vector E_;
    BitsArray bitsX_;
    BitsArray bitsQ_;
    EigenMatrix matQ_;
    EigenRowVector h_;
    EigenMatrix J_;
    real c_;

};

}

#endif