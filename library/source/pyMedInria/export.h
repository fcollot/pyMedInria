// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#ifdef WIN32
    #ifdef med_cpp_api_EXPORTS
        #define MED_EXPORT __declspec(dllexport)
    #else
        #define MED_EXPORT __declspec(dllimport)
    #endif
#else
    #define MED_EXPORT
#endif
