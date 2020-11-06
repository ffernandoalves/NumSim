/**
 * Book: Numerical Simulation in Molecular Dynamics: 
 *       Numerics, Algorithms, Parallelization, Applications
 * Author: Michael Griebel, Stephan Knapek, Gerhard Zumbusch
 * Date:   September, 2007 (moved to new file on October 29, 2020)
 * Adapted by Fernando Ribeiro Alves, October 29, 2020.
 **/

#define VELOCITY_VERLET_MODULE
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "velocity_verlet.hpp"

#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include <cstdlib>


real compoutputStatistic_basis(GravitationStoermerVerletParticle *p, int N, real t) {
    real e = 0;
    for (int i = 0; i < N; i++){
        real v = 0;
        for (int d = 0; d < DIM; d++){
            v += sqr(p[i].v[d]);
        }
        e += .5 * p[i].m * v;
    }
    return e;
}

void compX_basis(GravitationStoermerVerletParticle *p, int N, real delta_t) {
    for (int i = 0; i < N; i++){
        p[i].updateX(delta_t);
    }
}

void compV_basis(GravitationStoermerVerletParticle *p, int N, real delta_t) {
    for (int i = 0; i < N; i++){
        p[i].updateV(delta_t);
    }
}

void compF_basis(GravitationStoermerVerletParticle *p, int N) {
    for (int i = 0; i < N; i++) {
        for (int d = 0; d < DIM; d++) {
            p[i].F[d] = 0;
        }
    }
    
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (i != j) {
                p[i].force(&p[j]);
            }
        }
    }
}

void out_headers_cvs(std::ofstream &outputData, const char *sep) {
    //Inicia o cabeçalho do arquivo de resultados
    int quant_header = 12;
    const char *column[quant_header] = {"names", "mass", "x0", "x1", "v0", "v1", "f0", "f1", "time", "kinetic_energy", "delta_t", "N"};
    
    for (int i = 0; i < quant_header; i++) {
        if ( i == quant_header - 1 ) { outputData << column[i] << std::endl; }
        else { outputData << column[i] << *sep; }
    }
}

void out_pull_data_cvs(GravitationStoermerVerletParticle *p, std::ofstream &outputData, std::string *list_body, int N, real t, real delta_t, real kinetic_energy, const char *sep) {
    //Armazena os resultados em um arquivo csv
    for (int i = 0; i < N; i++) {
        outputData << list_body[i]    << *sep 
                   << p[i].m          << *sep
                   << p[i].x[0]       << *sep 
                   << p[i].x[1]       << *sep
                   << p[i].v[0]       << *sep
                   << p[i].v[1]       << *sep
                   << p[i].F[0]       << *sep 
                   << p[i].F[1]       << *sep
                   << t               << *sep 
                   << kinetic_energy  << *sep
                   << delta_t         << *sep 
                   << N               << std::endl;
    }
}

void outputResults_basis(GravitationStoermerVerletParticle *p, int N, real t, int count_iter, real delta_t, real kinetic_energy, const char *data_output, std::string *list_body) {
    const char *sep = "&";
    std::ofstream outPutData;
    outPutData.open(data_output, std::ios::app);

    if (count_iter == 0) { out_headers_cvs(outPutData, sep); }

    out_pull_data_cvs(p, outPutData, list_body, N, t, delta_t, kinetic_energy, sep);

    outPutData.close();
}

void timeIntegration_basic(real t, real delta_t, real t_end, GravitationStoermerVerletParticle *p, int N, const char *data_output, std::string *list_body) {
    int count_iter = 0;
    real kinetic_energy = 0.0f;
    
    outputResults_basis(p, N, t, count_iter, delta_t, kinetic_energy, data_output, list_body);
    count_iter++;

    compF_basis(p, N);
    while (t < t_end) {
        t += delta_t;
        compX_basis(p, N, delta_t);
        compF_basis(p, N);
        compV_basis(p, N, delta_t);
        kinetic_energy = compoutputStatistic_basis(p, N, t);
        outputResults_basis(p, N, t, count_iter, delta_t, kinetic_energy, data_output, list_body);
        count_iter++;
    }
}

void string_to_real(GravitationStoermerVerletParticle *p, std::string massa, std::string value_x, std::string value_v, int c_pos) {
    /*TODO: Melhorar essa função*/
    
    size_t idx, idv;
    idx = value_x.find("(");
    if (idx == std::string::npos) {
        std::cout << "ERRO: Tipo não identificado." << std::endl;
        abort();
    }

    std::string value_x0 = "", value_x1 = "", value_v0 = "", value_v1 = ""; 
    
    idx = value_x.find(",") - 1;

    size_t c_x = 0;
    for (std::string::iterator iter_x = value_x.begin() + 1; iter_x < value_x.end() - 1; ++iter_x) {
        if (c_x < idx) { value_x0 += *iter_x; }
        else if (c_x > idx) { value_x1 +=  *iter_x; }
        c_x += 1;
    }

    idv = value_v.find(",") - 1;

    size_t c_v = 0;

    for (std::string::iterator iter_v = value_v.begin() + 1; iter_v < value_v.end() - 1; ++iter_v) {
        if (c_v < idv) { value_v0 += *iter_v; }
        else if (c_v > idv) { value_v1 +=  *iter_v; }
        c_v += 1;
    }

    p[c_pos].m    = std::stod(massa);
    p[c_pos].x[0] = std::stod(value_x0);
    p[c_pos].x[1] = std::stod(value_x1);
    p[c_pos].v[0] = std::stod(value_v0);
    p[c_pos].v[1] = std::stod(value_v1);
}

void initData_basis(GravitationStoermerVerletParticle *p, int N, const char *data_input, std::string *list_body) {
    std::string m, x, v, body;
    std::ifstream inData;
    inData.open(data_input, std::ios::in);

    if (!inData) {
        std::cout << "Não foi possível inicializar o arquivo: " << data_input << std::endl;
        abort();
    }

    std::string line, total;     // ignora
    std::getline(inData, line);  // as duas primeiras
    std::getline(inData, total); // linhas do arquivo

    int c = 0;
    while(inData.good()) {
        if (c >= N) { break; }

        std::getline(inData, body, '&');
        list_body[c] = body;
        std::getline(inData, m   , '&');
        std::getline(inData, x   , '&');
        std::getline(inData, v   , '\n');

        string_to_real(p, m, x, v, c);

        c += 1;
    }
    
    inData.close();
}

void inputParameters_basis(real *delta_t, real *t_end, int *N, const char *data_input) {
    std::string delt, t_en, total_particles;
    std::ifstream inData;
    inData.open(data_input, std::ios::in);

    if (!inData) {
        std::cout << "Não foi possível inicializar o arquivo: " << data_input << std::endl;
        abort();
    }

    std::getline(inData, delt, '&');
    std::getline(inData, t_en, '\n');
    std::getline(inData, total_particles);

    if (*delta_t == 0) { *delta_t = std::stod(delt); }
    if (*t_end   == 0) { *t_end = std::stod(t_en); }
    *N = std::stoi(total_particles);

    inData.close();
}

bool checkout_file(const char *data_output) {
    std::fstream FILE;
    FILE.open(data_output);
    bool fail = (FILE.fail()) ? true : false;
    FILE.close();
    return fail;
}

static PyObject * init_verlet(PyObject *self, PyObject *args, PyObject *kwargs) {
    int N;
    real delta_t = 0;
    real t_end = 0;

    PyObject *data_input_obj = Py_None;
    const char *data_input;
    PyObject *data_output_obj = Py_None;
    const char *data_output;

    const char *keywords[5] = {"data_input_obj", "data_output_obj", "delta_t", "t_end", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O&O&|dd", const_cast<char **>(keywords),
                                    PyUnicode_FSConverter, &data_input_obj, PyUnicode_FSConverter, 
                                    &data_output_obj, &delta_t, &t_end)) {
        return NULL;
    }

    if (data_input_obj == Py_None) { return NULL; }

    data_input = PyBytes_AsString(data_input_obj);
    data_output = PyBytes_AsString(data_output_obj);

    if (!checkout_file(data_output)) {
        std::cout << "Warning: Já existe um arquivo de resultados no caminho de saida repassado." << std::endl;
        std::cout << "PATH_FILE: " << data_output << std::endl;
        std::cout << "Tentando carregar dados a partir desse arquivo." << std::endl;
        Py_RETURN_NONE;
    }

    inputParameters_basis(&delta_t, &t_end, &N, data_input);
    GravitationStoermerVerletParticle *p = (GravitationStoermerVerletParticle*)malloc(N * sizeof(*p));
    std::string list_body[N];
    initData_basis(p, N, data_input, list_body);
    timeIntegration_basic(0, delta_t, t_end, p, N, data_output, list_body);
    free(p);
    
    Py_RETURN_NONE;
}

//======================================================
 
static PyMethodDef VelocityVerletMethods[] = {
    {"init_verlet", (PyCFunction) init_verlet, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef VelocityVerletModule = {
    PyModuleDef_HEAD_INIT,
    "velocity_verlet",      /* m_name     */
    "sem doc",              /* m_doc      */
    -1,                     /* m_size     */
    VelocityVerletMethods,  /* m_methods  */
    NULL,                   /* m_reload   */
    NULL,                   /* m_traverse */
    NULL,                   /* m_clear    */
    NULL,                   /* m_free     */
};

PyMODINIT_FUNC PyInit_velocity_verlet(void){
    Py_Initialize();
    return PyModule_Create(&VelocityVerletModule);
}