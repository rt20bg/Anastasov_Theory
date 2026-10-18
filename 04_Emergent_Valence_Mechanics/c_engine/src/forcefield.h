#ifndef EVM_FORCEFIELD_H
#define EVM_FORCEFIELD_H

/* Matches evm_forcefield.json from the Python EVM 4.0 harness (core/evm_forcefield.json).
 * Indexed directly by atomic number Z (0..MAX_Z-1); unsupported Z entries are zeroed. */
#define FF_MAX_Z 10

typedef struct {
    double R[FF_MAX_Z];     /* steric radius per element */
    double Excl[FF_MAX_Z];  /* phase-exclusion strength per element */
    double spin_pairing;
    double U_0;
    double nn_steric;
} ForceField;

/* Loads a forcefield from the known JSON schema (see forcefield/evm_forcefield.json).
 * This is a tiny hand-rolled parser for that one fixed schema, not a general JSON parser.
 * Returns 0 on success, -1 on failure (file not found / malformed). */
int forcefield_load(const char *path, ForceField *ff);

/* Fills ff with the exact defaults baked into evm_forcefield.json, for when no
 * file is supplied (keeps the tool usable with zero external files). */
void forcefield_defaults(ForceField *ff);

#endif
