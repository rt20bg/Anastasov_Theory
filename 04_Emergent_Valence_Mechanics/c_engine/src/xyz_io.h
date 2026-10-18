#ifndef EVM_XYZ_IO_H
#define EVM_XYZ_IO_H

#include "vec3.h"

typedef struct {
    int Z;
    Vec3 pos; /* Angstrom */
} XYZAtom;

/* Reads the FIRST frame of a (possibly multi-frame) XYZ file.
 * *atoms is malloc'd by this function; caller must free() it.
 * Returns the atom count, or -1 on error (bad format / unsupported element). */
int xyz_read_first_frame(const char *path, XYZAtom **atoms);

/* Element symbol <-> atomic number, for the elements this engine's
 * forcefield actually supports (H, C, N, O, F -- see forcefield.h). */
int element_symbol_to_Z(const char *symbol);
const char *element_Z_to_symbol(int Z);

/* Appends one frame to a multi-frame XYZ trajectory file (standard
 * "N \n comment \n El x y z [...]" blocks concatenated -- the convention
 * VMD/PyMOL/ASE/OVITO all read). Opens in append mode, writes, closes. */
int xyz_append_frame(const char *path, const Vec3 *positions, const int *Zs,
                      int n_atoms, int step, double time_arb_units);

#endif
