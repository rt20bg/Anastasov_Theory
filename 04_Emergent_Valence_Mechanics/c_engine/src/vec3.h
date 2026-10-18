#ifndef EVM_VEC3_H
#define EVM_VEC3_H

#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct {
    double x, y, z;
} Vec3;

static inline Vec3 vec3_add(Vec3 a, Vec3 b) {
    Vec3 r = { a.x + b.x, a.y + b.y, a.z + b.z };
    return r;
}

static inline Vec3 vec3_sub(Vec3 a, Vec3 b) {
    Vec3 r = { a.x - b.x, a.y - b.y, a.z - b.z };
    return r;
}

static inline Vec3 vec3_scale(Vec3 a, double s) {
    Vec3 r = { a.x * s, a.y * s, a.z * s };
    return r;
}

static inline double vec3_dot(Vec3 a, Vec3 b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

static inline double vec3_norm_sq(Vec3 a) {
    return vec3_dot(a, a);
}

static inline double vec3_norm(Vec3 a) {
    return sqrt(vec3_norm_sq(a));
}

static inline Vec3 vec3_zero(void) {
    Vec3 r = { 0.0, 0.0, 0.0 };
    return r;
}

#endif
