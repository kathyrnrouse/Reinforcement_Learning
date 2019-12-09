# CMake generated Testfile for 
# Source directory: /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1
# Build directory: /Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/build/cmake-build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(exampletest "/usr/local/bin/python" "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/docs/examples/runAll.py")
set_tests_properties(exampletest PROPERTIES  _BACKTRACE_TRIPLES "/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/CMakeLists.txt;476;add_test;/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/CMakeLists.txt;0;")
subdirs("src")
