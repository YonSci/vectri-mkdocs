---
hide:
  - toc
---

# Basic Linux Commands for VECTRI Users

This is a hands-on, practical guide for people who have never (or barely) used Linux before but want to install and run VECTRI (or any scientific software).

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

## Getting Started: Create Your Training Directory

Let's start by creating a dedicated folder for practicing these commands. Copy and paste each command below into your terminal.

**Show your current location**

```bash
pwd
```

**Go to your home directory**

```bash
cd ~
```

**Create a training directory**

```bash
mkdir linux_training
```

**Enter the training directory**

```bash
cd linux_training
```

**Verify you're in the right place**

```bash
pwd
```

You should see something like `/home/yourname/linux_training` or `/Users/yourname/linux_training`

---

## 1. Navigation Commands

### pwd - Print Working Directory

**Show where you are right now**

```bash
pwd
```

### ls - List Files and Folders

**List files in current directory**

```bash
ls
```

**List files with detailed information (long format)**

```bash
ls -l
```

**List files with human-readable sizes (KB, MB, GB)**

```bash
ls -lh
```

**List all files including hidden ones (starting with .)**

```bash
ls -a
```

### cd - Change Directory

**Go to home directory**

```bash
cd ~
```

**Go back to training directory**

```bash
cd ~/linux_training
```

**Go up one level (to parent directory)**

```bash
cd ..
```

**Check where you are now**

```bash
pwd
```

**Go back to training directory**

```bash
cd ~/linux_training
```

**Go back to previous directory**

```bash
cd -
```

---

## 2. Creating Folders and Files

Let's create some practice files and folders in your training directory.

**Make sure you're in the training directory**

```bash
cd ~/linux_training
```

### mkdir - Make Directory

**Create a folder called "vectri_runs"**

```bash
mkdir vectri_runs
```

**List to see the new folder**

```bash
ls
```

**Create nested folders (parent folders created automatically with -p)**

```bash
mkdir -p data/raw/temperature
```

**Create multiple folders at once**

```bash
mkdir results scripts output
```

**List all folders**

```bash
ls
```

### touch - Create Empty Files

**Create a new empty file**

```bash
touch hello.txt
```

**Create multiple files at once**

```bash
touch data1.txt data2.txt data3.txt
```

**Create a file in a subfolder**

```bash
touch results/summary.txt
```

**List files to see what you created**

```bash
ls -lh
```

---

## 3. Copying, Moving, and Renaming

### cp - Copy Files

**Copy a file**

```bash
cp hello.txt hello_backup.txt
```

**List to see both files**

```bash
ls
```

**Copy a file to another directory**

```bash
cp hello.txt results/
```

**Copy a folder and all its contents (recursive with -r)**

```bash
cp -r vectri_runs vectri_runs_backup
```

**List to see the copied folder**

```bash
ls
```

### mv - Move or Rename

**Rename a file**

```bash
mv hello_backup.txt hello_copy.txt
```

**Move a file into a folder**

```bash
mv data1.txt data/
```

**Move multiple files into a folder**

```bash
mv data2.txt data3.txt data/
```

**Rename a folder**

```bash
mv vectri_runs_backup old_runs
```

**List to see changes**

```bash
ls
```

### rm - Remove Files and Folders

!!! warning "Be Careful!"
    The `rm` command permanently deletes files. There is no trash/recycle bin!

**Remove a single file**

```bash
rm hello_copy.txt
```

**Remove a folder and all its contents (recursive with -r)**

```bash
rm -r old_runs
```

**Force remove without confirmation (-rf) - USE WITH EXTREME CAUTION!**

```bash
# Don't run this unless you're sure!
# rm -rf dangerous_folder
```

---

## 4. Viewing and Editing Files

Let's create a file with some content and practice viewing it.

**Create a file with content using echo and >**

```bash
echo "Temperature data for Nairobi" > data/temperature.txt
```

**Add more lines using >>**

```bash
echo "Date: 2025-01-15" >> data/temperature.txt
echo "Morning: 18°C" >> data/temperature.txt
echo "Afternoon: 26°C" >> data/temperature.txt
echo "Evening: 22°C" >> data/temperature.txt
```

### cat - Show Entire File

**Display the whole file**

```bash
cat data/temperature.txt
```

### head - Show First Lines

**Show first 3 lines**

```bash
head -n 3 data/temperature.txt
```

### tail - Show Last Lines

**Show last 2 lines**

```bash
tail -n 2 data/temperature.txt
```

### less - View File Page by Page

**View file with scrolling (press q to quit)**

```bash
less data/temperature.txt
```

!!! tip "Less Navigation"
    - Press **Space** to go down one page
    - Press **b** to go back one page
    - Press **q** to quit
    - Press **/** to search

### nano - Simple Text Editor

**Edit a file with nano**

```bash
nano data/temperature.txt
```

!!! tip "Nano Commands"
    - **Ctrl + O** to save
    - **Ctrl + X** to exit
    - **Ctrl + K** to cut a line
    - **Ctrl + U** to paste

---

## 5. Finding and Searching

Let's practice finding files and searching for text.

**Create more files for practice**

```bash
cd ~/linux_training
touch results/output1.nc results/output2.nc results/data.csv
```

### find - Find Files by Name

**Find all .txt files in current directory and subdirectories**

```bash
find . -name "*.txt"
```

**Find all .nc files**

```bash
find . -name "*.nc"
```

**Find directories only**

```bash
find . -type d
```

### grep - Search Text in Files

**Search for a word in a file**

```bash
grep "Temperature" data/temperature.txt
```

**Search for a word (case-insensitive with -i)**

```bash
grep -i "temperature" data/temperature.txt
```

**Search recursively in all files (-r)**

```bash
grep -r "Nairobi" .
```

**Search command history**

```bash
history | grep "mkdir"
```

---

## 6. Pipes and Redirection

Pipes and redirection let you combine commands and save output.

### > - Redirect Output (Overwrite)

**Save directory listing to a file**

```bash
ls -lh > file_list.txt
```

**View the created file**

```bash
cat file_list.txt
```

### >> - Redirect Output (Append)

**Add more content to the file**

```bash
echo "--- End of List ---" >> file_list.txt
```

**View the updated file**

```bash
cat file_list.txt
```

### | - Pipe Output to Another Command

**List files and filter for .txt files**

```bash
ls -l | grep ".txt"
```

**Count how many files/folders are in current directory**

```bash
ls | wc -l
```

**Show disk usage and display only the top 5**

```bash
du -sh * | sort -hr | head -5
```

---

## 7. Permissions

Let's create a script and make it executable.

**Create a simple shell script**

```bash
cat > scripts/hello.sh << 'EOF'
#!/bin/bash
echo "Hello from VECTRI training!"
echo "Today is $(date)"
EOF
```

**Try to run it (it will fail because it's not executable)**

```bash
./scripts/hello.sh
```

### chmod - Change File Permissions

**Make the script executable**

```bash
chmod +x scripts/hello.sh
```

**Now run it**

```bash
./scripts/hello.sh
```

**View file permissions**

```bash
ls -l scripts/hello.sh
```

!!! info "Permission Notation"
    - `r` = read (4)
    - `w` = write (2)
    - `x` = execute (1)
    - `chmod 755` = owner can read/write/execute, others can read/execute
    - `chmod +x` = add execute permission for everyone

---

## 8. Installing Software (Ubuntu/Debian/WSL)

**Update package list**

```bash
sudo apt update
```

**Install VECTRI dependencies**

```bash
sudo apt install git gfortran libnetcdf-dev libnetcdff-dev netcdf-bin cdo ncview nco
```

**Install other useful tools**

```bash
sudo apt install ncdu tree htop
```

---

## 9. Environment Variables

Environment variables store configuration that programs can use.

### Temporary Variables (Current Session Only)

**Set a temporary variable**

```bash
export MYVAR="hello"
```

**Display the variable**

```bash
echo $MYVAR
```

**Display your home directory variable**

```bash
echo $HOME
```

### Permanent Variables (Add to ~/.bashrc)

**Open your .bashrc file**

```bash
nano ~/.bashrc
```

**Add these lines at the end (for VECTRI):**

```bash
export VECTRI=$HOME/vectri
export NETCDF_LIB=$(nf-config --flibs)
export NETCDF_INCLUDE=$(nf-config --fflags)
export FC=$(nf-config --fc)
alias vectri="$VECTRI/vectri"
```

**Save and exit nano (Ctrl+O, then Ctrl+X)**

**Apply the changes immediately**

```bash
source ~/.bashrc
```

**Test the variable**

```bash
echo $VECTRI
```

---

## 10. Git - Version Control

Git helps you download and update code repositories.

### Clone a Repository (First Time)

**Clone the VECTRI repository**

```bash
cd ~
git clone https://gitlab.com/tompkins/vectri.git
```

**Enter the repository**

```bash
cd vectri
```

**List the contents**

```bash
ls -la
```

### Update an Existing Repository

**Make sure you're in the repository directory**

```bash
cd ~/vectri
```

**Get the latest updates**

```bash
git pull
```

**Check the status**

```bash
git status
```

---

## 11. Process Management

Learn how to view and manage running programs.

### View Running Processes

**List all running processes**

```bash
ps aux
```

**View processes in real-time (press q to quit)**

```bash
top
```

**Better process viewer (if htop is installed)**

```bash
htop
```

**Find specific processes (e.g., python)**

```bash
ps aux | grep python
```

### Stop Processes

**Kill a process by ID (replace 12345 with actual process ID)**

```bash
# kill 12345
```

**Force kill a process (use only when normal kill doesn't work)**

```bash
# kill -9 12345
```

**Kill processes by name**

```bash
# pkill -f vectri
```

---

## 12. Disk Space Management

Check how much space you're using.

**Show disk space usage (human-readable format)**

```bash
df -h
```

**Show size of current directory**

```bash
du -sh .
```

**Show size of each item in current directory**

```bash
du -sh *
```

**Show size of training directory**

```bash
cd ~
du -sh linux_training
```

**Interactive disk usage explorer (if installed)**

```bash
ncdu ~/linux_training
```

---

## 13. Compressing and Archiving

Save space by compressing files and folders.

**Create a compressed archive of results folder**

```bash
cd ~/linux_training
tar -czvf results_backup.tar.gz results/
```

!!! info "tar flags explained"
    - `c` = create
    - `z` = compress with gzip
    - `v` = verbose (show progress)
    - `f` = file name follows

**List contents of archive without extracting**

```bash
tar -tzvf results_backup.tar.gz
```

**Extract the archive**

```bash
mkdir extracted
tar -xzvf results_backup.tar.gz -C extracted/
```

**Create a zip archive**

```bash
zip -r data_backup.zip data/
```

**Extract a zip file**

```bash
mkdir unzipped
unzip data_backup.zip -d unzipped/
```

---

## 14. Downloading Files

Download files from the internet.

### wget - Download Files

**Download a file**

```bash
cd ~/linux_training
wget https://raw.githubusercontent.com/python/cpython/main/README.rst
```

**Download with a custom name**

```bash
wget -O python_readme.txt https://raw.githubusercontent.com/python/cpython/main/README.rst
```

### curl - Another Download Tool

**Download a file**

```bash
curl -O https://raw.githubusercontent.com/python/cpython/main/LICENSE
```

**View file without downloading**

```bash
curl https://raw.githubusercontent.com/python/cpython/main/README.rst | head -20
```

---

## 15. Symbolic Links

Create shortcuts to files or folders in other locations.

**Create a symbolic link to a folder**

```bash
cd ~/linux_training
ln -s ~/linux_training/data data_link
```

**List to see the link (arrow shows where it points)**

```bash
ls -lh
```

**Access files through the link**

```bash
ls data_link/
```

**Remove the link (not the original folder!)**

```bash
rm data_link
```

---

## 16. Bash Scripting Basics

Create a simple script to automate tasks.

**Create an analysis script**

```bash
cat > scripts/analyze_data.sh << 'EOF'
#!/bin/bash
# VECTRI Data Analysis Script

echo "========================================"
echo "VECTRI Training Data Analysis"
echo "========================================"
echo ""
echo "Date: $(date)"
echo "User: $USER"
echo "Location: $(pwd)"
echo ""
echo "Files in data directory:"
ls -lh ~/linux_training/data/
echo ""
echo "Total disk space used:"
du -sh ~/linux_training
echo ""
echo "Analysis complete!"
EOF
```

**Make it executable**

```bash
chmod +x scripts/analyze_data.sh
```

**Run the script**

```bash
./scripts/analyze_data.sh
```

---

## 17. Useful Shortcuts and Tips

### Command Line Shortcuts

**Clear the terminal screen**

```bash
clear
```

Or press: `Ctrl + L`

**Cancel current command**

Press: `Ctrl + C`

**Search command history**

Press: `Ctrl + R` then start typing

**Auto-complete file/folder names**

Type first few letters and press: `Tab`

**View command history**

```bash
history
```

**Run the last command again**

```bash
!!
```

**Go to beginning of line**

Press: `Ctrl + A`

**Go to end of line**

Press: `Ctrl + E`

---

## 18. Quick Reference Cheat-Sheet

**Create a cheat sheet file**

```bash
cat > ~/linux_cheat_sheet.txt << 'EOF'
=== LINUX COMMAND CHEAT SHEET ===

Navigation:
  pwd              - where am I?
  ls -lh           - list files nicely
  cd folder        - go into folder
  cd ..            - go up one level
  cd ~             - go home

Files/Folders:
  mkdir folder     - create folder
  touch file       - create empty file
  cp file1 file2   - copy file
  mv old new       - move/rename
  rm file          - delete file
  rm -r folder     - delete folder

Viewing Files:
  cat file         - show entire file
  less file        - view page by page
  head file        - first 10 lines
  tail file        - last 10 lines
  nano file        - edit file

Finding:
  find . -name "*.txt"  - find files
  grep "word" file      - search in file

Redirection:
  cmd > file       - save output
  cmd >> file      - append output
  cmd1 | cmd2      - pipe commands

System:
  df -h            - disk space
  du -sh folder    - folder size
  ps aux           - show processes
  top              - monitor processes
  chmod +x file    - make executable

Git:
  git clone URL    - download repo
  git pull         - update repo
  git status       - check status

Package Management (Ubuntu/Debian):
  sudo apt update           - update package list
  sudo apt install package  - install software
EOF
```

**View your cheat sheet**

```bash
cat ~/linux_cheat_sheet.txt
```

**Always keep it handy**

```bash
less ~/linux_cheat_sheet.txt
```

---

## 19. Complete Hands-On Practice Workflow

Let's put everything together! Copy and run these commands one by one.

**Go to your training directory**

```bash
cd ~/linux_training
```

**Create a project structure**

```bash
mkdir -p vectri_project/{data,scripts,results,logs}
```

**Create some data files**

```bash
echo "Station,Date,Temperature,Humidity" > vectri_project/data/weather.csv
echo "Nairobi,2025-01-15,26,60" >> vectri_project/data/weather.csv
echo "Nairobi,2025-01-16,28,55" >> vectri_project/data/weather.csv
echo "Mombasa,2025-01-15,32,75" >> vectri_project/data/weather.csv
```

**Create a processing script**

```bash
cat > vectri_project/scripts/process.sh << 'EOF'
#!/bin/bash
echo "Processing weather data..."
echo "Date: $(date)" > vectri_project/logs/process.log
echo "Processing complete" >> vectri_project/logs/process.log
cat vectri_project/data/weather.csv
EOF
```

**Make script executable and run it**

```bash
chmod +x vectri_project/scripts/process.sh
./vectri_project/scripts/process.sh
```

**View the log file**

```bash
cat vectri_project/logs/process.log
```

**Create a compressed backup**

```bash
tar -czvf vectri_project_backup.tar.gz vectri_project/
```

**Check the backup size**

```bash
ls -lh vectri_project_backup.tar.gz
```

**View the project structure**

```bash
tree vectri_project/
```

Or if tree is not installed:

```bash
find vectri_project/ -type f -o -type d | sort
```

**Clean up (optional)**

```bash
# Uncomment to remove the project
# rm -r vectri_project
# rm vectri_project_backup.tar.gz
```

---

## 20. Troubleshooting Common Issues

### Permission Denied

**If you get "Permission denied" when running a script:**

```bash
chmod +x your_script.sh
```

### Command Not Found

**If you get "command not found":**

```bash
# For apt-based systems (Ubuntu/Debian)
sudo apt update
sudo apt install package-name

# Check if it's in your PATH
echo $PATH
```

### No Space Left on Device

**Check disk space:**

```bash
df -h
```

**Find large files:**

```bash
du -sh * | sort -hr | head -10
```

### File Already Exists

**To force overwrite when copying:**

```bash
cp -f source destination
```

**To force overwrite when moving:**

```bash
mv -f source destination
```

---

## 🎉 Congratulations!

You now speak basic Linux! You've learned:

✅ Navigation and file management  
✅ Creating, editing, and viewing files  
✅ Copying, moving, and removing files  
✅ Searching and finding files  
✅ Using pipes and redirection  
✅ Managing permissions  
✅ Installing software  
✅ Version control with Git  
✅ Basic scripting  
✅ Troubleshooting common issues

Keep practicing these commands, and they'll become second nature! Happy computing! 🚀

---

## 📝 Test Your Knowledge

Ready to test your understanding of basic Linux commands? Take the interactive quiz to assess your knowledge and reinforce what you've learned.

[Take the Linux Commands Quiz →](../quizzes/linux-commands-quiz.md){ .md-button .md-button--primary }

---

## 🔗 Additional Resources

- [Ubuntu Command Line Tutorial](https://ubuntu.com/tutorials/command-line-for-beginners)
- [The Linux Command Line (Free Book)](http://linuxcommand.org/tlcl.php)
- [ExplainShell](https://explainshell.com/) - Explains any shell command

