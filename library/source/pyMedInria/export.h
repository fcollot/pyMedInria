// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#ifdef WIN32
    #ifdef pyMedInria_library_EXPORTS
        #define PYMED_EXPORT __declspec(dllexport)
    #else
        #define PYMED_EXPORT __declspec(dllimport)
    #endif
#else
    #define PYMED_EXPORT
#endif
