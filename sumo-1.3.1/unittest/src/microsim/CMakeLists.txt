add_executable(testmicrosim
        MSEventControlTest.cpp
        MSCFModelTest.cpp
        MSCFModel_IDMTest.cpp
        )
set_property(TARGET testmicrosim PROPERTY FOLDER "test_exe")
add_test(NAME testmicrosim COMMAND $<TARGET_FILE:testmicrosim>)
set_target_properties(testmicrosim PROPERTIES OUTPUT_NAME_DEBUG testmicrosimD)

if (MSVC OR APPLE)
    target_link_libraries(testmicrosim microsim microsim_actions microsim_devices microsim_cfmodels microsim_lcmodels microsim_pedestrians microsim_trigger microsim_traffic_lights mesosim traciserver libsumostatic netload microsim_output microsim_engine mesosim ${commonvehiclelibs} ${GTEST_BOTH_LIBRARIES} ${GRPC_LIBS})
else ()
    target_link_libraries(testmicrosim -Wl,--start-group microsim microsim_actions microsim_devices microsim_cfmodels microsim_lcmodels microsim_pedestrians microsim_trigger microsim_traffic_lights mesosim traciserver libsumostatic netload microsim_output microsim_engine mesosim ${commonvehiclelibs} -Wl,--end-group ${GTEST_BOTH_LIBRARIES} ${GRPC_LIBS})
endif ()
