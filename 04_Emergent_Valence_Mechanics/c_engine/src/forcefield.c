#include "forcefield.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void forcefield_defaults(ForceField *ff) {
    memset(ff, 0, sizeof(*ff));
    ff->spin_pairing = 0.12;
    ff->U_0 = 10.0;
    ff->nn_steric = 0.001;
    /* H=1, C=6, N=7, O=8, F=9 -- same as core/evm_forcefield.json */
    ff->R[1] = 0.39; ff->Excl[1] = 0.0;
    ff->R[6] = 0.17; ff->Excl[6] = 2.0;
    ff->R[7] = 0.16; ff->Excl[7] = 2.0;
    ff->R[8] = 0.14; ff->Excl[8] = 2.0;
    ff->R[9] = 0.14; ff->Excl[9] = 2.0;
}

/* Finds the next occurrence of `key` (as a quoted JSON key) and returns a
 * pointer just past the following ':' , or NULL if not found. Scans only
 * forward from `from` so repeated calls walk through the file in order. */
static const char *find_key(const char *from, const char *key) {
    char pattern[64];
    snprintf(pattern, sizeof(pattern), "\"%s\"", key);
    const char *p = strstr(from, pattern);
    if (!p) return NULL;
    p = strchr(p + strlen(pattern), ':');
    return p ? p + 1 : NULL;
}

static int parse_double_after(const char *from, const char *key, double *out) {
    const char *p = find_key(from, key);
    if (!p) return -1;
    *out = strtod(p, NULL);
    return 0;
}

int forcefield_load(const char *path, ForceField *ff) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;

    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *buf = (char *)malloc((size_t)len + 1);
    if (!buf) { fclose(f); return -1; }
    size_t nread = fread(buf, 1, (size_t)len, f);
    buf[nread] = '\0';
    fclose(f);

    forcefield_defaults(ff); /* start from defaults, override with whatever the file has */

    parse_double_after(buf, "spin_pairing", &ff->spin_pairing);
    parse_double_after(buf, "U_0", &ff->U_0);
    parse_double_after(buf, "nn_steric", &ff->nn_steric);

    const char *elements = strstr(buf, "\"elements\"");
    if (elements) {
        const char *p = elements;
        for (int z = 0; z < FF_MAX_Z; z++) {
            char zkey[8];
            snprintf(zkey, sizeof(zkey), "%d", z);
            const char *zp = find_key(p, zkey);
            /* Guard against matching z=1 inside "10", "12" etc. by requiring
             * the key to appear before the next element block or end. This
             * fixed schema only has single/double-digit Z keys as object
             * keys "N": {...}, so a plain substring search is sufficient
             * given FF_MAX_Z <= 10 (single-digit keys only). */
            if (zp) {
                double r, excl;
                if (parse_double_after(zp, "R", &r) == 0) ff->R[z] = r;
                if (parse_double_after(zp, "Excl", &excl) == 0) ff->Excl[z] = excl;
            }
        }
    }

    free(buf);
    return 0;
}
