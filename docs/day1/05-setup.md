# Setup

## 🧬 VECTRI Installation Guide  

**Target OS:** Ubuntu 22.04 LTS  
**Purpose:** Install all required libraries and build the VECTRI malaria model  

---

## 1️⃣ Set Compilers and Flags

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

## 2️⃣ Create Installation Prefix Directories

```bash
# Create a workspace for source downloads
cd ~
mkdir -p ~/download_lib && cd ~/download_lib

sudo apt update

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

## 3️⃣ Download Sources

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

## 4️⃣ Build and Install Each Library

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

## 5️⃣ Set Environment Variables

Add the following to your `~/.bashrc` to make the libraries available:

```bash
cat <<'EOF' >> ~/.bashrc
# NetCDF libraries for VECTRI
export PATH=/opt/apps/libs/netcdf/4.9.0/bin:$PATH
export LD_LIBRARY_PATH=/opt/apps/libs/netcdf/4.9.0/lib:/opt/apps/libs/hdf5/1.12.2/lib:/opt/apps/libs/zlib/1.2.12/lib:/opt/apps/libs/szip/2.1.1/lib:$LD_LIBRARY_PATH
export CPATH=/opt/apps/libs/netcdf/4.9.0/include:$CPATH
EOF

source ~/.bashrc
```

### Verify Installation

```bash
which nc-config
which nf-config
nc-config --version
nf-config --version
```

---

## 6️⃣ VECTRI Model Installation

### Download and build VECTRI

```bash
cd ~
git clone https://gitlab.com/tompkins/vectri.git  
cd vectri
ls 
```

### Set environment variables (one-time; add to your shell startup)

```bash
export VECTRI="$HOME/vectri"
export NETCDF_LIB="$(nf-config --flibs)"
export NETCDF_INCLUDE="$(nf-config --fflags)"
export FC="$(nf-config --fc)"   # usually gfortran

# sanity:
echo $VECTRI
nc-config --version && nf-config --version
```

### Persist across logins

Append to `~/.bashrc` (or `~/.bash_profile` on some systems):

```bash
cat <<'EOF' >> ~/.bashrc
export VECTRI="$HOME/vectri"
export NETCDF_LIB="$(nf-config --flibs)"
export NETCDF_INCLUDE="$(nf-config --fflags)"
export FC="$(nf-config --fc)"
EOF

source ~/.bashrc
```

### Create a separate workspace and run the simulation  

Why separate? Running inside the repo pollutes the git tree and makes future git pull painful. VECTRI's run wrapper will also try to guard against this.

```bash
cd ~

mkdir -p ~/run
# go to your run workspace
cd run

# To get list of command line options
$VECTRI/vectri

# Example Simulation
$VECTRI/vectri -c $VECTRI/data/example_sys5.nc -d $VECTRI/data/example_data.nc
```

If the model compiles successfully there should then be a number of messages about the options chosen.

You should see:

  - a compile phase (make: Entering directory '/…/input') that produces vectri.exe 

  - then runtime logs (vector/disease, climate variable aliases, etc.) 
  
  - The output will show the simulation progress and completion status.

  ![simulation progress and completion status](../assets/img/vectri-test-run.png)

  - If your simulation has ended correctly 🎉 and if you type ls, you should find the output file vectri.nc has appeared.
  
  ![vectri output file](../assets/img/vectri-test-dir.png)

---

## 7️⃣ Verification and Troubleshooting

- `which nc-config` → `/opt/apps/libs/netcdf/4.9.0/bin/nc-config`  
- `ldd vectri | grep netcdf` → ensures it links to your local libraries  
- Check environment: `echo $LD_LIBRARY_PATH`
- If libraries not found: verify paths in `~/.bashrc` and `source ~/.bashrc`

---

### ✅ You now have a fully configured scientific environment for VECTRI on Ubuntu 22.04 LTS.
