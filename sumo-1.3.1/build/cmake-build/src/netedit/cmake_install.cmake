# Install script for directory: /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/src/netedit

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/bin/netedit")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netedit" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netedit")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/opt/X11/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netedit")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netedit")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/X11R6/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netedit")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/strip" -u -r "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netedit")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netedit/additionals/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netedit/changes/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netedit/dialogs/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netedit/frames/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netedit/netelements/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netedit/demandelements/cmake_install.cmake")

endif()

