# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.15

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.15.3/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.15.3/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build

# Utility rule file for distcheck.

# Include the progress variables for this target.
include CMakeFiles/distcheck.dir/progress.make

CMakeFiles/distcheck:
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && rm -rf sumo-1.3.1
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && unzip -q sumo-src-1.3.1.zip
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && cd sumo-1.3.1 && mkdir _cmake_build _cmake_install && cd _cmake_build && cmake -DCMAKE_INSTALL_PREFIX=../_cmake_install .. || ( echo ERROR:\ the\ cmake\ configuration\ failed. && false ) && make -j8 || ( echo ERROR:\ the\ compilation\ failed. && false ) && make test || ( echo ERROR:\ the\ test\ suite\ failed. && false ) && make install || ( echo ERROR:\ the\ install\ target\ failed. && false )
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && rm -rf sumo-1.3.1

distcheck: CMakeFiles/distcheck
distcheck: CMakeFiles/distcheck.dir/build.make

.PHONY : distcheck

# Rule to build all files generated by this target.
CMakeFiles/distcheck.dir/build: distcheck

.PHONY : CMakeFiles/distcheck.dir/build

CMakeFiles/distcheck.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/distcheck.dir/cmake_clean.cmake
.PHONY : CMakeFiles/distcheck.dir/clean

CMakeFiles/distcheck.dir/depend:
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/CMakeFiles/distcheck.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/distcheck.dir/depend

