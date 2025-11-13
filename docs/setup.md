# Setup

## 🧬 VECTRI Modular Installation Guide  


**Target OS:** Ubuntu 22.04 LTS  
**Purpose:** Install and manage all libraries for the VECTRI malaria model using Lua-based Lmod modules  

---

## 1️⃣ Install Lua and Lmod (Environment Modules)

```bash
# Create a workspace for source downloads
cd ~
mkdir -p ~/download_lib && cd ~/download_lib

sudo apt update

# 1. Install Tcl/Tk (optional utilities some modules still use)
sudo apt install -y tcl tcl-dev tk tk-dev

# 2. Install Lua and headers (for Lmod)
sudo apt install -y lua5.3 lua5.3-dev liblua5.3-dev

# 3. Build Lua 5.1.4.9 from source (Lmod’s embedded Lua)
wget https://sourceforge.net/projects/lmod/files/lua-5.1.4.9.tar.bz2
tar xf lua-5.1.4.9.tar.bz2 && cd lua-5.1.4.9

./configure --prefix=/opt/apps/lua/5.1.4.9   # installation prefix
make -j$(nproc)
sudo make install

# 4. Symlink binaries so lua is found system-wide
sudo ln -s /opt/apps/lua/5.1.4.9/bin/lua /usr/local/bin/lua
cd ~
```

**Configure your shell to find Lua and Lmod**

```bash
# Append to ~/.bashrc
echo 'export PATH=/opt/apps/lua/5.1.4.9/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 2️⃣ Install Lmod (8.7)

```bash
cd ~/download_lib
wget https://sourceforge.net/projects/lmod/files/Lmod-8.7.tar.bz2
tar xf Lmod-8.7.tar.bz2 && cd Lmod-8.7

# Configure and install Lmod into /opt/apps/lmod/8.7
./configure --prefix=/opt/apps/lmod/8.7
make -j$(nproc)
sudo make install
```

### Activate Lmod for your shell

```bash
# Add to ~/.bashrc for automatic initialization
echo 'source /opt/apps/lmod/8.7/init/bash' >> ~/.bashrc
echo 'export MODULEPATH=/opt/apps/modulefiles/lib:/opt/apps/modulefiles/mpi' >> ~/.bashrc
source ~/.bashrc

# Verify installation
module --version
lmod --version
```

---

## 3️⃣ Set Compilers and Flags

```bash
which gcc g++ gfortran
gcc --version
gfortran --version

# Export compiler environment variables
export CC=gcc
export CXX=g++
export FC=gfortran
export F77=gfortran

# Enable Fortran-10+ argument compatibility flags
gcc_version=$(gcc -dumpversion | cut -d. -f1)
if [ "$gcc_version" -ge 10 ]; then
  export fallow_argument="-fallow-argument-mismatch"
  export boz_argument="-fallow-invalid-boz"
else
  export fallow_argument=""
  export boz_argument=""
fi
export FFLAGS="$fallow_argument $boz_argument"
export FCFLAGS="$fallow_argument $boz_argument"
```

---

## 4️⃣ Create installation prefix directories

```bash
sudo mkdir -p /opt/apps/libs
BASE_DIR=/opt/apps/libs

# Shared prefix for most libs
ZPFX=$BASE_DIR/zlib/1.2.12
SPFX=$BASE_DIR/szip/2.1.1
JPFX=$BASE_DIR/jasper/1.900.1
HPFX=$BASE_DIR/hdf5/1.12.2
NPFX=$BASE_DIR/netcdf/4.9.0

sudo mkdir -p $ZPFX $SPFX $JPFX $HPFX $NPFX
```

---

## 5️⃣ Download Sources

```bash
cd ~/download_lib

# ZLIB
wget -c -4 https://github.com/madler/zlib/archive/refs/tags/v1.2.12.tar.gz

# SZIP
wget -c -4 https://support.hdfgroup.org/ftp/lib-external/szip/2.1.1/src/szip-2.1.1.tar.gz

# JasPer (JPEG-2000)
wget -c -4 https://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.1.zip

# HDF5
wget -c -4 https://github.com/HDFGroup/hdf5/archive/refs/tags/hdf5-1_12_2.tar.gz

# NetCDF C and Fortran
wget -c -4 https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.9.0.tar.gz
wget -c -4 https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.6.0.tar.gz
```

---

## 6️⃣ Build and Install Each Library

### 🔹 ZLIB
```bash
tar xf v1.2.12.tar.gz
cd zlib-1.2.12
./configure --prefix=$ZPFX
make -j$(nproc)
sudo make install
cd ..
```

### 🔹 SZIP
```bash
tar xf szip-2.1.1.tar.gz
cd szip-2.1.1
./configure --prefix=$SPFX
make -j$(nproc)
sudo make install
cd ..
```

### 🔹 JasPer
```bash
unzip jasper-1.900.1.zip
cd jasper-1.900.1
autoreconf -i            # regenerate configure scripts
./configure --prefix=$JPFX
make -j$(nproc)
sudo make install
cd ..
```

### 🔹 HDF5 (Serial build)
```bash
tar xf hdf5-1_12_2.tar.gz
cd hdf5-hdf5-1_12_2

CPPFLAGS="-I$ZPFX/include -I$SPFX/include" LDFLAGS="-L$ZPFX/lib -L$SPFX/lib" ./configure --prefix=$HPFX             --enable-hl --enable-fortran             --with-zlib=$ZPFX --with-szlib=$SPFX

make -j$(nproc)
sudo make install
cd ..
```

### 🔹 NetCDF-C
```bash
tar xf v4.9.0.tar.gz
cd netcdf-c-4.9.0

CPPFLAGS="-I$HPFX/include" LDFLAGS="-L$HPFX/lib -L$ZPFX/lib -L$SPFX/lib" ./configure --prefix=$NPFX --enable-netcdf-4 --disable-dap

make -j$(nproc)
sudo make install
cd ..
```

### 🔹 NetCDF-Fortran
```bash
tar xf v4.6.0.tar.gz
cd netcdf-fortran-4.6.0

CPPFLAGS="-I$NPFX/include" LDFLAGS="-L$NPFX/lib -Wl,-rpath,$NPFX/lib" ./configure --prefix=$NPFX
make -j$(nproc)
sudo make install
cd ..
```

---

## 7️⃣ Create Modulefiles

```bash
sudo mkdir -p /opt/apps/modulefiles/lib/{zlib,szip,jasper,hdf5,netcdf-c,netcdf-fortran}
```

Example: `/opt/apps/modulefiles/lib/hdf5/1.12.2.lua`

```lua
help([[HDF5 1.12.2 (serial build)]])
whatis("Name: hdf5")
whatis("Version: 1.12.2")

local root = "/opt/apps/libs/hdf5/1.12.2"

depends_on("zlib/1.2.12")
depends_on("szip/2.1.1")

prepend_path("PATH",            pathJoin(root, "bin"))
prepend_path("CPATH",           pathJoin(root, "include"))
prepend_path("LIBRARY_PATH",    pathJoin(root, "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(root, "lib"))
prepend_path("PKG_CONFIG_PATH", pathJoin(root, "lib/pkgconfig"))
setenv("HDF5_HOME", root)
```

### Example: `/opt/apps/modulefiles/lib/netcdf-c/4.9.0.lua`
```lua
help([[NetCDF-C 4.9.0]])
whatis("Name: netcdf-c")
whatis("Version: 4.9.0")

local root = "/opt/apps/libs/netcdf/4.9.0"
depends_on("hdf5/1.12.2")

prepend_path("PATH",            pathJoin(root, "bin"))
prepend_path("CPATH",           pathJoin(root, "include"))
prepend_path("LIBRARY_PATH",    pathJoin(root, "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(root, "lib"))
setenv("NETCDF_C_HOME", root)
```

### Example: `/opt/apps/modulefiles/lib/netcdf-fortran/4.6.0.lua`
```lua
help([[NetCDF-Fortran 4.6.0]])
whatis("Name: netcdf-fortran")
whatis("Version: 4.6.0")

local root = "/opt/apps/libs/netcdf/4.9.0"
depends_on("netcdf-c/4.9.0")

prepend_path("PATH",            pathJoin(root, "bin"))
prepend_path("CPATH",           pathJoin(root, "include"))
prepend_path("LIBRARY_PATH",    pathJoin(root, "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(root, "lib"))
setenv("NETCDF_FORTRAN_HOME", root)
```

### Load and verify
```bash
module purge
module use /opt/apps/modulefiles/lib
module load netcdf-fortran/4.6.0

which nc-config
which nf-config
nc-config --version
nf-config --version
```

---

## 8️⃣ Add Paths to `.bashrc`

```bash
cat <<'EOF' >> ~/.bashrc
# HPC module system
source /opt/apps/lmod/8.7/init/bash
module use /opt/apps/modulefiles/lib /opt/apps/modulefiles/mpi
EOF

source ~/.bashrc
```

---

## 9️⃣ VECTRI Model Installation (Ref: ICTP Prerequisites)

### Download and build VECTRI

```bash
cd ~
git clone https://github.com/ICTP/vectri.git
cd vectri

# Example compile with NetCDF and HDF5 support
make clean
make NETCDF_HOME=/opt/apps/libs/netcdf/4.9.0 HDF5_HOME=/opt/apps/libs/hdf5/1.12.2
```

### Run a sample simulation

```bash
# Navigate to example data directory
cd ~/vectri
./vectri -c data/example_sys5.nc -d data/example_data.nc

# Or run via module environment (recommended)
module load netcdf-fortran/4.6.0
$VECTRI/vectri -c $VECTRI/data/example_sys5.nc -d $VECTRI/data/example_data.nc
```

---

## 🔟 Verification and Troubleshooting

- `which nc-config` → `/opt/apps/libs/netcdf/4.9.0/bin/nc-config`  
- `ldd vectri | grep netcdf` → ensures it links to your local libraries  
- `module list` → shows all loaded modules  
- To unload: `module unload netcdf-fortran/4.6.0`

---

### ✅ You now have a fully modular, Lua/Lmod-managed scientific environment for VECTRI on Ubuntu 22.04 LTS.
