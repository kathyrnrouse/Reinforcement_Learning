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

# Utility rule file for dist.

# Include the progress variables for this target.
include CMakeFiles/dist.dir/progress.make

CMakeFiles/dist:
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && rm -rf sumo-1.3.1 sumo-1.3.1.zip sumo-src-1.3.1.tar.gz sumo-src-1.3.1.zip sumo-all-1.3.1.tar.gz sumo-all-1.3.1.zip
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && /usr/bin/git archive --prefix sumo-1.3.1/ -o sumo-1.3.1.zip HEAD
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && unzip -q sumo-1.3.1.zip
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && cp -a docs/tutorial docs/examples sumo-1.3.1/docs
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && find tools/contributed/saga/ tools/contributed/*matlab -type f | grep -v .git | xargs cp --parents --target-dir sumo-1.3.1
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && zip -rq sumo-src-1.3.1.zip sumo-1.3.1
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && tar czf sumo-src-1.3.1.tar.gz sumo-1.3.1
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && cp -a docs/userdoc docs/pydoc docs/javadoc docs/man sumo-1.3.1/docs
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && cp bin/*.jar sumo-1.3.1/bin
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && cp -a tests sumo-1.3.1
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && zip -rq sumo-all-1.3.1.zip sumo-1.3.1
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && tar czf sumo-all-1.3.1.tar.gz sumo-1.3.1
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 && rm -rf sumo-1.3.1 sumo-1.3.1.zip

dist: CMakeFiles/dist
dist: CMakeFiles/dist.dir/build.make

.PHONY : dist

# Rule to build all files generated by this target.
CMakeFiles/dist.dir/build: dist

.PHONY : CMakeFiles/dist.dir/build

CMakeFiles/dist.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/dist.dir/cmake_clean.cmake
.PHONY : CMakeFiles/dist.dir/clean

CMakeFiles/dist.dir/depend:
	cd /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1 /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build/CMakeFiles/dist.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/dist.dir/depend

