----------Step 1----------

> CMakeLists.txt

    cmake_minimum_required (VERSION 2.6)
    project (Tutorial)
    
    # The version number.
    set (Tutorial_VERSION_MAJOR 1)
    set (Tutorial_VERSION_MINOR 0)
    
    # configure a header file to pass some of the CMake settings
    # to the source code
    configure_file (
    "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
    "${PROJECT_BINARY_DIR}/TutorialConfig.h"
    )
  
      # add the binary tree to the search path for include files
      # so that we will find TutorialConfig.h
      include_directories("${PROJECT_BINARY_DIR}")
    
      # add the executable
      add_executable(Tutorial tutorial.cxx)

> tutorial.cxx

      // A simple program that computes the square root of a number
      #include <stdio.h>
      #include <stdlib.h>
      #include <math.h>
      #include "TutorialConfig.h"
      
      int main (int argc, char *argv[])
      {
        if (argc < 2)
          {
          fprintf(stdout,"%s Version %d.%d\n",
                  argv[0],
                  Tutorial_VERSION_MAJOR,
                  Tutorial_VERSION_MINOR);
          fprintf(stdout,"Usage: %s number\n",argv[0]);
          return 1;
          }
        double inputValue = atof(argv[1]);
        double outputValue = sqrt(inputValue);
        fprintf(stdout,"The square root of %g is %g\n",
                inputValue, outputValue);
        return 0;
      }
![screen shot 2016-03-24 at 10 06 41 pm](https://cloud.githubusercontent.com/assets/4596631/14036328/413d6138-f20e-11e5-869e-43cb65fb77e9.png)

----------Step 2----------

> CMakeLists

      cmake_minimum_required (VERSION 2.6)
      project (Tutorial)
      
      # The version number.
      set (Tutorial_VERSION_MAJOR 1)
      set (Tutorial_VERSION_MINOR 0)
      
      # should we use our own math functions
      option(USE_MYMATH "Use tutorial provided math implementation" ON)
      
      # configure a header file to pass some of the CMake settings
      # to the source code
      configure_file (
        "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
        "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        )
      
      # add the binary tree to the search path for include files
      # so that we will find TutorialConfig.h
      include_directories ("${PROJECT_BINARY_DIR}")
      
      # add the MathFunctions library?
      if (USE_MYMATH)
        include_directories ("${PROJECT_SOURCE_DIR}/MathFunctions")
        add_subdirectory (MathFunctions)
        set (EXTRA_LIBS ${EXTRA_LIBS} MathFunctions)
      endif ()
      
      # add the executable
      add_executable (Tutorial tutorial.cxx)
      target_link_libraries (Tutorial  ${EXTRA_LIBS})

> tutorial.cxx

      // A simple program that computes the square root of a number
      #include <stdio.h>
      #include <stdlib.h>
      #include <math.h>
      #include "TutorialConfig.h"
      
      #ifdef USE_MYMATH
      #include "MathFunctions.h"
      #endif
      
      int main (int argc, char *argv[])
      {
        if (argc < 2)
          {
          fprintf(stdout,"%s Version %d.%d\n",
                  argv[0],
                  Tutorial_VERSION_MAJOR,
                  Tutorial_VERSION_MINOR);
          fprintf(stdout,"Usage: %s number\n",argv[0]);
          return 1;
          }
      
        double inputValue = atof(argv[1]);
        double outputValue = 0;
      
        if(inputValue >= 0)
          {
      #ifdef USE_MYMATH
          outputValue = mysqrt(inputValue);
      #else
          outputValue = sqrt(inputValue);
      #endif
          }
      
        fprintf(stdout,"The square root of %g is %g\n",
                inputValue, outputValue);
        return 0;
      }
![screen shot 2016-03-24 at 10 13 49 pm](https://cloud.githubusercontent.com/assets/4596631/14036329/42ea586a-f20e-11e5-9d29-178944df4bd7.png)

----------Step 3----------

> CMakeLists

      cmake_minimum_required (VERSION 2.6)
      project (Tutorial)
      
      # The version number.
      set (Tutorial_VERSION_MAJOR 1)
      set (Tutorial_VERSION_MINOR 0)
      
      # should we use our own math functions
      option(USE_MYMATH "Use tutorial provided math implementation" ON)
      
      # configure a header file to pass some of the CMake settings
      # to the source code
      configure_file (
        "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
        "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        )
      
      # add the binary tree to the search path for include files
      # so that we will find TutorialConfig.h
      include_directories ("${PROJECT_BINARY_DIR}")
      
      # add the MathFunctions library?
      if (USE_MYMATH)
        include_directories ("${PROJECT_SOURCE_DIR}/MathFunctions")
        add_subdirectory (MathFunctions)
        set (EXTRA_LIBS ${EXTRA_LIBS} MathFunctions)
      endif ()
      
      # add the executable
      add_executable (Tutorial tutorial.cxx)
      target_link_libraries (Tutorial  ${EXTRA_LIBS})
      
      # add the install targets
      install (TARGETS Tutorial DESTINATION bin)
      install (FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        DESTINATION include)
      
      
      # enable testing
      enable_testing ()
      
      # does the application run
      add_test (TutorialRuns Tutorial 25)
      
      # does it sqrt of 25
      add_test (TutorialComp25 Tutorial 25)
      set_tests_properties (TutorialComp25
        PROPERTIES PASS_REGULAR_EXPRESSION "25 is 5"
        )
      
      # does it handle negative numbers
      add_test (TutorialNegative Tutorial -25)
      set_tests_properties (TutorialNegative
        PROPERTIES PASS_REGULAR_EXPRESSION "-25 is 0"
        )
      
      # does it handle small numbers
      add_test (TutorialSmall Tutorial 0.0001)
      set_tests_properties (TutorialSmall
        PROPERTIES PASS_REGULAR_EXPRESSION "0.0001 is 0.01"
        )
      
      # does the usage message work?
      add_test (TutorialUsage Tutorial)
      set_tests_properties (TutorialUsage
        PROPERTIES
        PASS_REGULAR_EXPRESSION "Usage:.*number"
        )

> tutorial.cxx

      // A simple program that computes the square root of a number
      #include <stdio.h>
      #include <stdlib.h>
      #include <math.h>
      #include "TutorialConfig.h"
      
      #ifdef USE_MYMATH
      #include "MathFunctions.h"
      #endif
      
      int main (int argc, char *argv[])
      {
        if (argc < 2)
          {
          fprintf(stdout,"%s Version %d.%d\n",
                  argv[0],
                  Tutorial_VERSION_MAJOR,
                  Tutorial_VERSION_MINOR);
          fprintf(stdout,"Usage: %s number\n",argv[0]);
          return 1;
          }
      
        double inputValue = atof(argv[1]);
        double outputValue = 0;
      
        if(inputValue >= 0)
          {
      #ifdef USE_MYMATH
          outputValue = mysqrt(inputValue);
      #else
          outputValue = sqrt(inputValue);
      #endif
          }
      
        fprintf(stdout,"The square root of %g is %g\n",
                inputValue, outputValue);
        return 0;
      }
![screen shot 2016-03-24 at 10 20 06 pm](https://cloud.githubusercontent.com/assets/4596631/14036384/a16e6ba6-f20e-11e5-8b16-3312f46a05a2.png)

----------Step 4----------

> CMakeLists

      cmake_minimum_required (VERSION 2.6)
      project (Tutorial)
      
      # The version number.
      set (Tutorial_VERSION_MAJOR 1)
      set (Tutorial_VERSION_MINOR 0)
      
      # does this system provide the log and exp functions?
      include (${CMAKE_ROOT}/Modules/CheckFunctionExists.cmake)
      check_function_exists (log HAVE_LOG)
      check_function_exists (exp HAVE_EXP)
      
      # should we use our own math functions
      option(USE_MYMATH "Use tutorial provided math implementation" ON)
      
      # configure a header file to pass some of the CMake settings
      # to the source code
      configure_file (
        "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
        "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        )
      
      # add the binary tree to the search path for include files
      # so that we will find TutorialConfig.h
      include_directories ("${PROJECT_BINARY_DIR}")
      
      # add the MathFunctions library?
      if (USE_MYMATH)
        include_directories ("${PROJECT_SOURCE_DIR}/MathFunctions")
        add_subdirectory (MathFunctions)
        set (EXTRA_LIBS ${EXTRA_LIBS} MathFunctions)
      endif ()
      
      # add the executable
      add_executable (Tutorial tutorial.cxx)
      target_link_libraries (Tutorial  ${EXTRA_LIBS})
      
      # add the install targets
      install (TARGETS Tutorial DESTINATION bin)
      install (FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        DESTINATION include)
      
      # enable testing
      enable_testing ()
      
      # does the application run
      add_test (TutorialRuns Tutorial 25)
      
      # does the usage message work?
      add_test (TutorialUsage Tutorial)
      set_tests_properties (TutorialUsage
        PROPERTIES
        PASS_REGULAR_EXPRESSION "Usage:.*number"
        )
      
      #define a macro to simplify adding tests
      macro (do_test arg result)
        add_test (TutorialComp${arg} Tutorial ${arg})
        set_tests_properties (TutorialComp${arg}
          PROPERTIES PASS_REGULAR_EXPRESSION ${result}
          )
      endmacro ()
      
      # do a bunch of result based tests
      do_test (25 "25 is 5")
      do_test (-25 "-25 is 0")
      do_test (0.0001 "0.0001 is 0.01")

> tutroial.cxx

      // A simple program that computes the square root of a number
      #include <stdio.h>
      #include <stdlib.h>
      #include <math.h>
      #include "TutorialConfig.h"
      
      #ifdef USE_MYMATH
      #include "MathFunctions.h"
      #endif
      
      int main (int argc, char *argv[])
      {
        if (argc < 2)
          {
          fprintf(stdout,"%s Version %d.%d\n",
                  argv[0],
                  Tutorial_VERSION_MAJOR,
                  Tutorial_VERSION_MINOR);
          fprintf(stdout,"Usage: %s number\n",argv[0]);
          return 1;
          }
      
        double inputValue = atof(argv[1]);
        double outputValue = 0;
      
        if(inputValue >= 0)
          {
      #ifdef USE_MYMATH
          outputValue = mysqrt(inputValue);
      #else
          outputValue = sqrt(inputValue);
      #endif
          }
      
        fprintf(stdout,"The square root of %g is %g\n",
                inputValue, outputValue);
        return 0;
      }
![screen shot 2016-03-24 at 10 21 33 pm](https://cloud.githubusercontent.com/assets/4596631/14036412/eb5e74cc-f20e-11e5-901f-e81a32ea41ac.png)

----------Step 5----------

> CMakeLists

      cmake_minimum_required (VERSION 2.6)
      project (Tutorial)
      
      # The version number.
      set (Tutorial_VERSION_MAJOR 1)
      set (Tutorial_VERSION_MINOR 0)
      
      # does this system provide the log and exp functions?
      include (${CMAKE_ROOT}/Modules/CheckFunctionExists.cmake)
      check_function_exists (log HAVE_LOG)
      check_function_exists (exp HAVE_EXP)
      
      # should we use our own math functions
      option(USE_MYMATH "Use tutorial provided math implementation" ON)
      
      # configure a header file to pass some of the CMake settings
      # to the source code
      configure_file (
        "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
        "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        )
      
      # add the binary tree to the search path for include files
      # so that we will find TutorialConfig.h
      include_directories ("${PROJECT_BINARY_DIR}")
      
      # add the MathFunctions library?
      if (USE_MYMATH)
        include_directories ("${PROJECT_SOURCE_DIR}/MathFunctions")
        add_subdirectory (MathFunctions)
        set (EXTRA_LIBS ${EXTRA_LIBS} MathFunctions)
      endif ()
      
      # add the executable
      add_executable (Tutorial tutorial.cxx)
      target_link_libraries (Tutorial  ${EXTRA_LIBS})
      
      # add the install targets
      install (TARGETS Tutorial DESTINATION bin)
      install (FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        DESTINATION include)
      
      # enable testing
      enable_testing ()
      
      # does the application run
      add_test (TutorialRuns Tutorial 25)
      
      # does the usage message work?
      add_test (TutorialUsage Tutorial)
      set_tests_properties (TutorialUsage
        PROPERTIES
        PASS_REGULAR_EXPRESSION "Usage:.*number"
        )
      
      #define a macro to simplify adding tests
      macro (do_test arg result)
        add_test (TutorialComp${arg} Tutorial ${arg})
        set_tests_properties (TutorialComp${arg}
          PROPERTIES PASS_REGULAR_EXPRESSION ${result}
          )
      endmacro ()
      
      # do a bunch of result based tests
      do_test (4 "4 is 2")
      do_test (9 "9 is 3")
      do_test (5 "5 is 2.236")
      do_test (7 "7 is 2.645")
      do_test (25 "25 is 5")
      do_test (-25 "-25 is 0")
      do_test (0.0001 "0.0001 is 0.01")

> tutorial.cxx

      // A simple program that computes the square root of a number
      #include <stdio.h>
      #include <stdlib.h>
      #include <math.h>
      #include "TutorialConfig.h"
      
      #ifdef USE_MYMATH
      #include "MathFunctions.h"
      #endif
      
      int main (int argc, char *argv[])
      {
        if (argc < 2)
          {
          fprintf(stdout,"%s Version %d.%d\n",
                  argv[0],
                  Tutorial_VERSION_MAJOR,
                  Tutorial_VERSION_MINOR);
          fprintf(stdout,"Usage: %s number\n",argv[0]);
          return 1;
          }
      
        double inputValue = atof(argv[1]);
        double outputValue = 0;
      
        if(inputValue >= 0)
          {
      #ifdef USE_MYMATH
          outputValue = mysqrt(inputValue);
      #else
          outputValue = sqrt(inputValue);
      #endif
          }
      
        fprintf(stdout,"The square root of %g is %g\n",
                inputValue, outputValue);
        return 0;
      }
![screen shot 2016-03-24 at 10 23 41 pm](https://cloud.githubusercontent.com/assets/4596631/14036424/198eddc8-f20f-11e5-87ed-aa216b6eba95.png)
