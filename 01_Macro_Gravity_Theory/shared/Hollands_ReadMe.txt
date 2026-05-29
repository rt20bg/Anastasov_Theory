J/MNRAS/467/4970    Cool DZ white dwarfs. I.                 (Hollands+, 2017)
================================================================================
Cool DZ white dwarfs. I. Identification and spectral analysis.
    Hollands M.A., Koester D., Alekseev V., Herbert E.L., Gansicke B.T.
   <Mon. Not. R. Astron. Soc., 467, 4970-5000 (2017)>
   =2017MNRAS.467.4970H    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Stars, white dwarf ; Photometry, SDSS ; Abundances
Keywords: planets and satellites: composition - stars: abundances -
          stars: atmospheres - white dwarfs

Abstract:
    White dwarfs with metal lines in their spectra act as signposts for
    post-main-sequence planetary systems. Searching the Sloan Digital Sky
    Survey (SDSS) Data Release 12, we have identified 231 cool (<9000K)
    DZ white dwarfs with strong metal absorption, extending the DZ cooling
    sequence to both higher metal abundances and lower temperatures, and
    hence longer cooling ages. Of these 231 systems, 104 are previously
    unknown white dwarfs. Compared with previous work, our spectral
    fitting uses improved model atmospheres with updated line profiles and
    line-lists, which we use to derive effective temperatures and
    abundances for up to eight elements. We also determine spectroscopic
    distances to our sample, identifying two halo members with tangential
    space velocities >300km/s. The implications of our results on
    remnant planetary systems are to be discussed in a separate paper.

Description:
    The catalogue contains parameters for a sample of 231 cool DZ white
    dwarfs, identified in the Sloan Digital Sky Survey (SDSS) Data Release
    12, and showing strong photospheric absorption features in their
    spectra.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
table3.dat       112      231   SDSS PSF photometry for all white dwarfs
                                 in our sample
table6.dat        74      230   Derived parameters from atmospheric modelling of
                                 the SDSS and WHT spectra
table7.dat        50      230   The mass fraction of the convection zone, q, and
                                 logarithm of the diffusion time-scale in years
                                 for each element
table8.dat        62      230   Distances, proper motions, transverse motions
                                 and white dwarf cooling ages for our DZ sample
--------------------------------------------------------------------------------

See also:
   V/147 : The SDSS Photometric Catalogue, Release 12 (Alam+, 2015)

Byte-by-byte Description of file: table3.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1- 18  A18   ---     SDSS      SDSS name (HHMMSS.ss+DDMMSS.s)
  20- 33  A14   ---     PMF       SDSS Plate-MJD-Fiber
      35  I1    ---     Nsdss     Number of SDSS spectra available per object
  37- 42  F6.3  mag     umag      SDSS u magnitude
  44- 48  F5.3  mag   e_umag      rms uncertainty on umag
  50- 55  F6.3  mag     gmag      SDSS g magnitude
  57- 61  F5.3  mag   e_gmag      rms uncertainty on gmag
  63- 68  F6.3  mag     rmag      SDSS r magnitude
  70- 74  F5.3  mag   e_rmag      rms uncertainty on rmag
  76- 81  F6.3  mag     imag      SDSS i magnitude
  83- 87  F5.3  mag   e_imag      rms uncertainty on imag
  89- 94  F6.3  mag     zmag      SDSS z magnitude
  96-100  F5.3  mag   e_zmag      rms uncertainty on zmag
     102  A1    ---     Note      [*] * for the source not in other tables
 104-112  A9    ---     SName     SDSS short name (HHMM+DDMM)
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table6.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---     SName     SDSS short name (HHMM+DDMM)
  11- 14  I4    K       Teff      Effective temperature
  16- 18  I3    K     e_Teff      rms uncertainty on Teff
  20- 25  F6.2  [-]     [Ca/He]   Abundance [Ca/He]
  27- 32  F6.2  [-]     [Mg/He]   Abundance [Mg/He]
  34- 39  F6.2  [-]     [Fe/He]   Abundance [Fe/He]
  41- 46  F6.2  [-]     [Na/He]   ? Abundance [Na/He]
  48- 53  F6.2  [-]     [Cr/He]   ? Abundance [Cr/He]
  55- 60  F6.2  [-]     [Ti/He]   ? Abundance [Ti/He]
  62- 67  F6.2  [-]     [Ni/He]   ? Abundance [Ni/He]
  69- 70  A2    ---   l_[H/He]    [<= ] Limit flag on [H/He]
  71- 74  F4.1  [-]     [H/He]    ? Abundance [H/He]
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table7.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---     SName     SDSS short name (HHMM+DDMM)
  11- 15  F5.2  [-]     logq      Mass fraction of the convection zone
  17- 20  F4.2  [yr]    tCa       logarithm of the diffusion time-scale for Ca
  22- 25  F4.2  [yr]    tMg       logarithm of the diffusion time-scale for Mg
  27- 30  F4.2  [yr]    tFe       logarithm of the diffusion time-scale for Fe
  32- 35  F4.2  [yr]    tNa       logarithm of the diffusion time-scale for Na
  37- 40  F4.2  [yr]    tCr       logarithm of the diffusion time-scale for Cr
  42- 45  F4.2  [yr]    tTi       logarithm of the diffusion time-scale for Ti
  47- 50  F4.2  [yr]    tNi       logarithm of the diffusion time-scale for Ni
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table8.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label     Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---       SName     SDSS short name (HHMM+DDMM)
  12- 16  F5.1  pc        Dist      Distance
  18- 21  F4.1  pc      e_Dist      rms uncertainty on Dist
  23- 27  F5.1  mas/yr    pm        ? Total proper motion
  30- 33  F4.1  mas/yr  e_pm        ? rms uncertainty on pm
  35- 39  F5.1  km/s      vperp     ? Perpendicular velocity
  45- 48  F4.1  km/s    e_vperp     ? rms uncertainty on vperp
  50- 52  F3.1  Gyr       tau       Age
  55- 57  F3.1  Gyr     E_tau       Error on tau (upper value)
  60- 62  F3.1  Gyr     e_tau       Error on tau (lower value)
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                                      Patricia Vannier [CDS]    29-Nov-2019
