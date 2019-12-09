# Install script for directory: /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sumo/data" TYPE DIRECTORY FILES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/data/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sumo/tools" TYPE DIRECTORY FILES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/tools/" USE_SOURCE_PERMISSIONS REGEX "/calibration$" EXCLUDE REGEX "/lisum\\-core$" EXCLUDE REGEX "/lisum\\-gui$" EXCLUDE REGEX "/sumolib4matlab\\/src$" EXCLUDE REGEX "/traas$" EXCLUDE REGEX "/traci4matlab\\/src$" EXCLUDE REGEX "/\\.git$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND /usr/local/Cellar/cmake/3.15.3/bin/cmake -E create_symlink ../../bin $ENV{DESTDIR}/usr/local/share/sumo/bin)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xpysumolibx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND /usr/local/bin/python /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/tools/build/setup-sumolib.py clean --all install --root=$ENV{DESTDIR}/ --prefix=/usr/local --optimize=1)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xpytracix" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND /usr/local/bin/python /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/tools/build/setup-traci.py clean --all install --root=$ENV{DESTDIR}/ --prefix=/usr/local --optimize=1)
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/src/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
