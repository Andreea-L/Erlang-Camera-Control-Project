# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "rosorbitcamera: 1 messages, 0 services")

set(MSG_I_FLAGS "-Irosorbitcamera:/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg;-Istd_msgs:/opt/ros/jade/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rosorbitcamera_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg" NAME_WE)
add_custom_target(_rosorbitcamera_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rosorbitcamera" "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(rosorbitcamera
  "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosorbitcamera
)

### Generating Services

### Generating Module File
_generate_module_cpp(rosorbitcamera
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosorbitcamera
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rosorbitcamera_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rosorbitcamera_generate_messages rosorbitcamera_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg" NAME_WE)
add_dependencies(rosorbitcamera_generate_messages_cpp _rosorbitcamera_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosorbitcamera_gencpp)
add_dependencies(rosorbitcamera_gencpp rosorbitcamera_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosorbitcamera_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(rosorbitcamera
  "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosorbitcamera
)

### Generating Services

### Generating Module File
_generate_module_eus(rosorbitcamera
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosorbitcamera
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rosorbitcamera_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rosorbitcamera_generate_messages rosorbitcamera_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg" NAME_WE)
add_dependencies(rosorbitcamera_generate_messages_eus _rosorbitcamera_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosorbitcamera_geneus)
add_dependencies(rosorbitcamera_geneus rosorbitcamera_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosorbitcamera_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(rosorbitcamera
  "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosorbitcamera
)

### Generating Services

### Generating Module File
_generate_module_lisp(rosorbitcamera
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosorbitcamera
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rosorbitcamera_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rosorbitcamera_generate_messages rosorbitcamera_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg" NAME_WE)
add_dependencies(rosorbitcamera_generate_messages_lisp _rosorbitcamera_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosorbitcamera_genlisp)
add_dependencies(rosorbitcamera_genlisp rosorbitcamera_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosorbitcamera_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(rosorbitcamera
  "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosorbitcamera
)

### Generating Services

### Generating Module File
_generate_module_py(rosorbitcamera
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosorbitcamera
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rosorbitcamera_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rosorbitcamera_generate_messages rosorbitcamera_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreea/Documents/catkin_ws/src/rosorbitcamera/msg/Int32Numpy.msg" NAME_WE)
add_dependencies(rosorbitcamera_generate_messages_py _rosorbitcamera_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosorbitcamera_genpy)
add_dependencies(rosorbitcamera_genpy rosorbitcamera_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosorbitcamera_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosorbitcamera)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosorbitcamera
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(rosorbitcamera_generate_messages_cpp std_msgs_generate_messages_cpp)

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosorbitcamera)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosorbitcamera
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
add_dependencies(rosorbitcamera_generate_messages_eus std_msgs_generate_messages_eus)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosorbitcamera)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosorbitcamera
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(rosorbitcamera_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosorbitcamera)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosorbitcamera\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosorbitcamera
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(rosorbitcamera_generate_messages_py std_msgs_generate_messages_py)
