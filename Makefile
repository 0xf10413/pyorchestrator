###
# Variables to set
##################
# Output file name and directory
BIN=fclass.so
BUILD_DIR=./build

# Arguments to call the executable with
BIN_ARGS=

# C/C++ compiler (gcc/clang recommended)
CC=gcc
CXX=g++

# Debuger to use (gdb/cgdb recommended)
GDB=cgdb

# C/C++ compilation flags
CFLAGS=-std=c99 -g -pedantic -Wall -Wextra -Wshadow -Wpointer-arith \
       -Wcast-qual -Wstrict-prototypes -Wmissing-prototypes \
			 -Wconversion
CXXFLAGS=-std=c++11 -g -Wall -Wextra -pedantic -Wshadow -Weffc++ \
				 -Wconversion -I/usr/include/python3.7m -fPIC

# Linker flags
LDFLAGS=-lpython3.7m -lboost_python37

# Source files (adjust if needed)
SRC_CXX=$(wildcard src/*.cpp)
SRC_C=$(wildcard *.c)

###
# Automatic variables
#####################

# Object files
OBJ_CXX=$(SRC_CXX:%.cpp=$(BUILD_DIR)/%.o)
OBJ_C=$(SRC_C:%.c=$(BUILD_DIR)/%.o)
OBJ=$(OBJ_C)
OBJ+=$(OBJ_CXX)

# Dependencies
DEPS_CXX=$(OBJ_CXX:%.o=%.d)
DEPS_C=$(OBJ_C:%.o=%.d)
DEPS=$(DEPS_C)
DEPS+=$(DEPS_CXX)

###
# Rules
##################

# Main build target
all: check_source_exists $(BIN)

check_source_exists:
ifeq ($(SRC_CXX)$(SRC_C),)
	$(error "No source file. Build failed !")
endif

$(BIN): $(BUILD_DIR)/$(BIN)

# Add this rule to everything that needs
# to be rebuilt if this file changes
FORCE: Makefile


# Final linker call
$(BUILD_DIR)/$(BIN): $(OBJ)
	@mkdir -pv $(@D)
	$(CXX) -shared -o $@ $^ $(LDFLAGS)


# Include dependencies
-include $(DEPS)


# General build target
$(BUILD_DIR)/%.o: %.cpp FORCE
	@mkdir -pv $(@D)
	$(CXX) -o $@ -c $< $(CXXFLAGS) -MMD

$(BUILD_DIR)/%.o: %.c FORCE
	@mkdir -pv $(@D)
	$(CC) -o $@ -c $< $(CFLAGS) -MMD


# Clean-up targets
.PHONY: clean mrproper launch debug
clean:
	-rm -f $(OBJ) $(DEPS)

mrproper: clean
	-rm -rf $(BUILD_DIR)

# Launch targets
launch: all
	-$(BUILD_DIR)/$(BIN) $(BIN_ARGS)

debug: all
	-$(GDB) --quiet --args $(BUILD_DIR)/$(BIN) $(BIN_ARGS)

# Keep intermediate targets
# Needed for a functionnal FORCE
.SECONDARY:
