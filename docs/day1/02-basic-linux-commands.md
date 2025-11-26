---
hide:
  - toc
---

# Basic Linux Commands for VECTRI Users

This short, practical guide is written for people who have never (or barely) used Linux before but want to install and run VECTRI (or any scientific software).

!!! info "Cross-Platform Compatibility"
    Everything here works the same on Ubuntu, Linux Mint, WSL2 (Windows), Mac (Terminal) and most Linux servers.

## Opening the Terminal

=== "Ubuntu/Linux"
    Press **Ctrl + Alt + T**

=== "Mac"
    Press **Cmd + Space** → type "Terminal"

=== "Windows (WSL)"
    Type "wsl" in Windows search

---

## 1. Navigation & Seeing Where You Are

| Command | What it does | Example |
|---------|-------------|---------|
| `pwd` | Print Working Directory – shows your current folder | `pwd` → `/home/yourname` |
| `ls` | LiSt files and folders | `ls` |
| `ls -l` | Long listing (size, permissions, date) | `ls -l` |
| `ls -lh` | Long + human-readable sizes | `ls -lh` |
| `ls -a` | Show hidden files (start with .) | `ls -a` |
| `cd foldername` | Change Directory | `cd Documents` |
| `cd ..` | Go up one level | `cd ..` |
| `cd ~` or `cd` | Go to your home folder | `cd ~` |
| `cd -` | Go back to previous folder | `cd -` |

!!! tip "Quick Exercise"
    Try these commands in sequence:
    ```bash
    pwd
    cd /
    ls
    cd ~
    pwd
    ```

---

## 2. Creating & Removing Folders/Files

| Command | Meaning | Example |
|---------|---------|---------|
| `mkdir foldername` | MaKe DIRectory | `mkdir vectri_runs` |
| `mkdir -p a/b/c` | Create parent folders if needed | `mkdir -p ~/vectri_runs/test` |
| `touch filename` | Create empty file (or update timestamp) | `touch hello.txt` |
| `rm filename` | ReMove file | `rm hello.txt` |
| `rm -r foldername` | Remove folder and everything inside | `rm -r test` |
| `rm -rf foldername` | Force remove (no questions) – **dangerous!** | Use carefully! |

---

## 3. Copy, Move, Rename

| Command | Meaning | Example |
|---------|---------|---------|
| `cp file1 file2` | CoPy | `cp report.txt report_backup.txt` |
| `cp -r folder1 folder2` | Copy folder recursively | `cp -r oldrun newrun` |
| `mv file1 file2` | MoVe or rename | `mv old.txt new.txt` |
| `mv file folder/` | Move into folder | `mv *.nc results/` |

---

## 4. Viewing & Editing Files

| Command | Use | Example |
|---------|-----|---------|
| `cat file` | Show whole file | `cat .bashrc` |
| `less file` | View file page-by-page (q to quit) | `less bigfile.nc` |
| `head -n 20 file` | First 20 lines | `head -n 5 data.txt` |
| `tail -n 10 file` | Last 10 lines | `tail -f logfile` (follow live) |
| `nano filename` | Simple editor (Ctrl+O save, Ctrl+X exit) | `nano .bashrc` |
| `vim filename` | Powerful editor (press i to insert, Esc :wq to save+quit) | `vim config.txt` |

---

## 5. Installing Software (Ubuntu/Debian/WSL)

```bash
# Refresh package list
sudo apt update

# Install VECTRI dependencies
sudo apt install git gfortran libnetcdf-dev libnetcdff-dev netcdf-bin cdo ncview nco
```

---

## 6. Environment Variables & Aliases

```bash
# Temporary (only this terminal)
export MYVAR="hello"
echo $MYVAR

# Permanent – add to ~/.bashrc or ~/.zshrc
nano ~/.bashrc
```

Add these lines at the end of your `.bashrc`:

```bash
export VECTRI=$HOME/vectri
export NETCDF_LIB=$(nf-config --flibs)
export NETCDF_INCLUDE=$(nf-config --fflags)
export FC=$(nf-config --fc)
alias vectri="$VECTRI/vectri"
```

Apply changes:

```bash
source ~/.bashrc
```

---

## 7. Git – Getting & Updating Code

```bash
# First time only - clone the repository
git clone https://gitlab.com/tompkins/vectri.git

# Enter the directory
cd vectri

# Get latest version later
git pull
```

---

## 8. Finding Things

| Command | Example | Description |
|---------|---------|-------------|
| `find . -name "*.nc"` | `find . -name "*.nc"` | Find all netcdf files in current folder and subfolders |
| `grep "error" logfile` | `grep "error" logfile` | Search for text in file |
| `grep -r "VECTRI" .` | `grep -r "VECTRI" .` | Search recursively in all files |
| `history \| grep git` | `history \| grep git` | Search command history |

---

## 9. Pipes & Redirection

| Symbol | Meaning | Example |
|--------|---------|---------|
| `>` | Write output to file (overwrite) | `ls > list.txt` |
| `>>` | Append to file | `echo "done" >> log.txt` |
| `\|` | Pipe: send output of left command as input to right | `ls \| grep nc` |

**Example:**

```bash
# Show only lines with "eir"
ncdump -h vectri.nc | grep eir
```

---

## 10. Permissions

```bash
# View file permissions
ls -l
# output like: -rw-r--r--  1 user group  5K Nov 20  vectri.nc

# Make file executable
chmod +x script.sh

# Owner full rights, others read+execute
chmod 755 script.sh
```

---

## 11. Process Management & Killing Things

| Command | Meaning | Example |
|---------|---------|---------|
| `ps aux` | List all processes | `ps aux \| grep vectri` |
| `top` / `htop` | Interactive process viewer | `htop` |
| `kill PID` | Gentle kill | `kill 12345` |
| `kill -9 PID` | Force kill (use only when needed) | `kill -9 12345` |
| `pkill name` | Kill by name | `pkill -f vectri` |

---

## 12. Disk Space & Big Files

| Command | Meaning | Example |
|---------|---------|---------|
| `df -h` | Disk free (human readable) | `df -h` |
| `du -sh *` | Size of every file/folder in current directory | `du -sh *` |
| `du -sh .` | Total size of current directory | `du -sh .` |
| `ncdu` | Interactive disk usage explorer | `ncdu ~/vectri_runs` |

!!! tip "Installing ncdu"
    ```bash
    sudo apt install ncdu
    ```

---

## 13. Compressing & Archiving

| Command | Meaning | Example |
|---------|---------|---------|
| `tar -czvf name.tar.gz folder/` | Create gzipped tarball | `tar -czvf run1.tar.gz run1` |
| `tar -xzvf name.tar.gz` | Extract | `tar -xzvf run1.tar.gz` |
| `zip -r name.zip folder/` | Create zip | `zip -r run1.zip run1` |
| `unzip name.zip` | Extract zip | `unzip run1.zip` |

---

## 14. Downloading Files from the Web

| Command | Meaning | Example |
|---------|---------|---------|
| `wget URL` | Download file | `wget https://data.worldpop.org/.../population.nc` |
| `curl -O URL` | Same as wget | `curl -O https://example.com/file.nc` |
| `wget -r -np -k -L -p URL` | Download entire webpage (careful!) | Use with caution |

---

## 15. Symbolic Links

```bash
# Create a symbolic link
ln -s /path/to/real/file_or_folder linkname

# Example: Link climate data
cd ~/vectri_runs/run_africa
ln -s /data/era5_africa_2000_2020.nc climate.nc
ln -s /data/population_2020.nc data.nc
```

---

## 16. Bash Scripting Basics

Here's a simple script to analyze VECTRI output:

```bash
#!/bin/bash
set -euo pipefail

echo "Run   Mean_EIR   Peak_EIR"
echo "-----------------------------------"

for dir in run_*; do
  [ -d "$dir" ] || continue
  cd "$dir"

  mean_eir=$(cdo -s output -timmean -fldmean -selname,eir vectri.nc)
  peak_eir=$(cdo -s output -timmax -fldmean -selname,eir vectri.nc)

  printf "%-12s  %.2f    %.2f\n" "$dir" "$mean_eir" "$peak_eir"

  cd ..
done | tee eir_summary.txt
```

---

## Quick Reference Cheat-Sheet

```bash
pwd                  # where am I?
ls -lh               # list files nicely
cd folder            # go into folder
cd ..                # go up
cd ~                 # go home
mkdir newfolder      # make folder
cp file1 file2       # copy
mv old new           # move/rename
rm file              # delete file
rm -r folder         # delete folder
cat file             # view small file
less file            # view large file (q to quit)
nano file            # edit file
git clone URL        # download code
git pull             # update code
export VAR=value     # set environment variable
source ~/.bashrc     # reload bash settings
```

!!! tip "Save the Cheat-Sheet"
    You can save this to a file for quick reference:
    ```bash
    # Copy the commands above to ~/linux_cheat_sheet.txt
    ```

---

## Hands-On Practice

Try this complete workflow:

```bash
mkdir -p ~/vectri_training
cd ~/vectri_training
touch demo.txt
echo "Hello VECTRI" > demo.txt
cat demo.txt
cp demo.txt backup.txt
mkdir results
mv backup.txt results/
ls -l results/
rm -r results
```

---

## 🎉 Congratulations!

You now speak basic Linux! Happy computing! 🚀

## 📝 Test Your Knowledge

Ready to test your understanding of basic Linux commands? Take the interactive quiz to assess your knowledge and reinforce what you've learned.

[Take the Linux Commands Quiz →](../quizzes/linux-commands-quiz.md){ .md-button .md-button--primary }

