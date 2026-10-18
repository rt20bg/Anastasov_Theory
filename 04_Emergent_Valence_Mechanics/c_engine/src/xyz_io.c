#include "xyz_io.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int element_symbol_to_Z(const char *symbol) {
    /* Only the elements the EVM 4.0 forcefield actually defines (see
     * core/evm_forcefield.json / forcefield.c): H, C, N, O, F. */
    if (strcmp(symbol, "H") == 0) return 1;
    if (strcmp(symbol, "C") == 0) return 6;
    if (strcmp(symbol, "N") == 0) return 7;
    if (strcmp(symbol, "O") == 0) return 8;
    if (strcmp(symbol, "F") == 0) return 9;
    return -1;
}

const char *element_Z_to_symbol(int Z) {
    switch (Z) {
        case 1: return "H";
        case 6: return "C";
        case 7: return "N";
        case 8: return "O";
        case 9: return "F";
        default: return "X";
    }
}

int xyz_read_first_frame(const char *path, XYZAtom **atoms_out) {
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "error: cannot open input XYZ '%s'\n", path);
        return -1;
    }

    char line[1024];
    if (!fgets(line, sizeof(line), f)) { fclose(f); return -1; }
    int n = atoi(line);
    if (n <= 0) {
        fprintf(stderr, "error: invalid atom count in XYZ header\n");
        fclose(f);
        return -1;
    }

    if (!fgets(line, sizeof(line), f)) { fclose(f); return -1; } /* comment line, discarded */

    XYZAtom *atoms = (XYZAtom *)malloc(sizeof(XYZAtom) * (size_t)n);
    if (!atoms) { fclose(f); return -1; }

    for (int i = 0; i < n; i++) {
        char sym[16];
        double x, y, z;
        if (fscanf(f, "%15s %lf %lf %lf", sym, &x, &y, &z) != 4) {
            fprintf(stderr, "error: malformed XYZ line %d\n", i + 3);
            free(atoms);
            fclose(f);
            return -1;
        }
        int Z = element_symbol_to_Z(sym);
        if (Z < 0) {
            fprintf(stderr, "error: unsupported element '%s' (this forcefield only "
                             "defines H, C, N, O, F)\n", sym);
            free(atoms);
            fclose(f);
            return -1;
        }
        atoms[i].Z = Z;
        atoms[i].pos.x = x;
        atoms[i].pos.y = y;
        atoms[i].pos.z = z;
    }

    fclose(f);
    *atoms_out = atoms;
    return n;
}

int xyz_append_frame(const char *path, const Vec3 *positions, const int *Zs,
                      int n_atoms, int step, double time_arb_units) {
    FILE *f = fopen(path, "a");
    if (!f) {
        fprintf(stderr, "error: cannot open trajectory output '%s'\n", path);
        return -1;
    }
    fprintf(f, "%d\n", n_atoms);
    fprintf(f, "step=%d t=%.6f\n", step, time_arb_units);
    for (int i = 0; i < n_atoms; i++) {
        fprintf(f, "%s %.6f %.6f %.6f\n", element_Z_to_symbol(Zs[i]),
                positions[i].x, positions[i].y, positions[i].z);
    }
    fclose(f);
    return 0;
}
