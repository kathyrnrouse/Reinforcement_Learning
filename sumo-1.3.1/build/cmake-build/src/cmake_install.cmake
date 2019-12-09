# Install script for directory: /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/src

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/bin/sumo-gui")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo-gui" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo-gui")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/opt/X11/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo-gui")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo-gui")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/X11R6/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo-gui")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/strip" -u -r "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo-gui")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/bin/sumo")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/opt/X11/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/X11R6/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/strip" -u -r "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sumo")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/bin/netconvert")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netconvert" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netconvert")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/opt/X11/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netconvert")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netconvert")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/X11R6/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netconvert")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/strip" -u -r "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/netconvert")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/bin/od2trips")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/od2trips" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/od2trips")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/opt/X11/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/od2trips")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/od2trips")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/usr/X11R6/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/od2trips")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/strip" -u -r "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/od2trips")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/activitygen/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/dfrouter/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/duarouter/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/foreign/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/jtrrouter/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/libsumo/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/marouter/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/mesosim/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/microsim/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netbuild/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netgen/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netimport/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netload/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netwrite/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/od/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/osgview/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/polyconvert/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/router/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/tools/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/traci-server/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/traci_testclient/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/utils/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/gui/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/guinetload/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/guisim/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/mesogui/cmake_install.cmake")
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/netedit/cmake_install.cmake")

endif()

