#!/usr/bin/make -f

NUMCPUS:=$(shell grep -c '^processor' /proc/cpuinfo)
ARCH_NAME:=$(shell '$(TRGT)gcc' -dumpmachine)

CURDIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
OBJ_DIR:=$(CURDIR)/$(ARCH_NAME)/obj

TRGT=

CC   = $(TRGT)gcc
CXX  = $(TRGT)g++
AS   = $(TRGT)gcc -x assembler-with-cpp

LD   = $(TRGT)g++
AR   = $(TRGT)ar rvc

RM= rm --force --verbose

PYTHON= python3
CYTHON= cython3
PKGCONFIG= pkg-config

#~ PYTHON= /opt/conda/bin/python3
#~ CYTHON= /opt/conda/bin/cython
#~ PKGCONFIG= PKG_CONFIG_PATH=/opt/conda/lib/pkgconfig/ pkg-config

PACKAGES= python3-embed

ifndef PACKAGES
PKG_CONFIG_CFLAGS=
PKG_CONFIG_LDFLAGS=
PKG_CONFIG_LIBS=
else
PKG_CONFIG_CFLAGS=`$(PKGCONFIG) --cflags $(PACKAGES)`
PKG_CONFIG_LDFLAGS=`$(PKGCONFIG) --libs-only-L $(PACKAGES)`
PKG_CONFIG_LIBS=`$(PKGCONFIG) --libs-only-l $(PACKAGES)`
endif

CFLAGS= \
	-Wall \
	-fwrapv \
	-fstack-protector-strong \
	-Wall \
	-Wformat \
	-Werror=format-security \
	-Wdate-time \
	-D_FORTIFY_SOURCE=2 \
	-fPIC

LDFLAGS= \
	-Wl,-O1 \
	-Wl,-Bsymbolic-functions \
	-Wl,-z,relro \
	-Wl,--as-needed \
	-Wl,--no-undefined \
	-Wl,--no-allow-shlib-undefined \
	-Wl,-Bsymbolic-functions \
	-Wl,--dynamic-list-cpp-new \
	-Wl,--dynamic-list-cpp-typeinfo

CYFLAGS= \
	-3 \
	--cplus \
	-X language_level=3 \
	-X boundscheck=False

CSTD=-std=gnu17
CPPSTD=-std=gnu++17

OPTS= -O2 -g

DEFS= \
	-DNDEBUG \
	-D_LARGEFILE64_SOURCE \
	-D_FILE_OFFSET_BITS=64

INCS= \
	-Iinclude

CYINCS= \
	-Icython

LIBS=

OBJS= \
	$(OBJ_DIR)/tmxlite.o \
	$(OBJ_DIR)/LayerGroup.o \
	$(OBJ_DIR)/Object.o \
	$(OBJ_DIR)/ImageLayer.o \
	$(OBJ_DIR)/ObjectGroup.o \
	$(OBJ_DIR)/ObjectTypes.o \
	$(OBJ_DIR)/Property.o \
	$(OBJ_DIR)/Tileset.o \
	$(OBJ_DIR)/Map.o \
	$(OBJ_DIR)/FreeFuncs.o \
	$(OBJ_DIR)/TileLayer.o \
	$(OBJ_DIR)/miniz.o \
	$(OBJ_DIR)/pugixml.o

PYX_NAMES= gonlet shaders tmxlite

PYX_SRCS= $(PYX_NAMES:%=src/%.pyx)
PYX_CPPS= $(subst .pyx,.cpp,$(PYX_SRCS))
PYX_OBJS= $(subst .pyx,.o,$(PYX_SRCS))

all: tmxlite.so

tmxlite.so: $(OBJS)

%.bin:
	$(LD) $(CPPSTD) $(CSTD) $(LDFLAGS) $(PKG_CONFIG_LDFLAGS) -o $@ $+ $(LIBS) $(PKG_CONFIG_LIBS)

%.so:
	$(LD) -shared $(CPPSTD) $(CSTD) $(LDFLAGS) $(PKG_CONFIG_LDFLAGS) -o $@ $+ $(LIBS) $(PKG_CONFIG_LIBS)

%.a:
	$(AR) $@ $+

$(OBJ_DIR)/%.o: ../tmxlite/src/%.cpp
	@mkdir -p "$$(dirname '$@')"
	$(CXX) $(CPPSTD) $(OPTS) -o $@ -c $< $(DEFS) $(INCS) $(CFLAGS) $(PKG_CONFIG_CFLAGS)

$(OBJ_DIR)/%.o: ../tmxlite/src/%.c
	@mkdir -p "$$(dirname '$@')"
	$(CC) $(CSTD) $(OPTS) -o $@ -c $< $(DEFS) $(INCS) $(CFLAGS) $(PKG_CONFIG_CFLAGS)

$(OBJ_DIR)/%.o: ../tmxlite/src/detail/%.cpp
	@mkdir -p "$$(dirname '$@')"
	$(CXX) $(CPPSTD) $(OPTS) -o $@ -c $< $(DEFS) $(INCS) $(CFLAGS) $(PKG_CONFIG_CFLAGS)

$(OBJ_DIR)/%.o: $(OBJ_DIR)/%.cpp
	@mkdir -p "$$(dirname '$@')"
	$(CXX) $(CPPSTD) $(OPTS) -o $@ -c $< $(DEFS) $(INCS) $(CFLAGS) $(PKG_CONFIG_CFLAGS)

$(OBJ_DIR)/%.cpp: %.pyx
	@mkdir -p "$$(dirname '$@')"
	$(CYTHON) $(CYFLAGS) $(CYINCS) -o $@ $<


clean:
	$(RM) $(OBJS) $(PYX_OBJS)
	$(RM) $(subst .pyx,.cpp,$(PYX_SRCS))
	$(RM) $(subst .pyx,_api.cpp,$(PYX_SRCS))
	$(RM) $(subst .pyx,.h,$(PYX_SRCS))
	$(RM) $(subst .pyx,_api.h,$(PYX_SRCS))
	@find . -name '*.o' -exec $(RM) {} +
	@find . -name '*.a' -exec $(RM) {} +
	@find . -name '*.so' -exec $(RM) {} +
	@find . -name '*.pyc' -exec $(RM) {} +
	@find . -name '*.pyo' -exec $(RM) {} +
	@find . -name '*.bak' -exec $(RM) {} +
	@find . -name '*~' -exec $(RM) {} +
	@$(RM) core
	@rmdir '$(OBJ_DIR)' '$(CURDIR)/$(ARCH_NAME)/' --verbose 2>/dev/null || true

.PHONY: all clean
