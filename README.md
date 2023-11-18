# M.A.T.R.I.X - Multi-purpose Automated Testing and Reconnaissance Interface for eXploits

This guide will walk you through the steps required to set up the Pentest Builder project. Please follow the steps as outlined below:

- Keep in mind this is still heavily in progress. If you have any ideas or want to contribute just let me know.

![Image GIF](https://github.com/HFScripts/pentest-builder/blob/main/MATRIX2023.gif)

## Pre-requisites
- Kali Linux (Headless) on WSL.
- RustScan version 2.0.1.

## Note:
- The terminal size matters. If you resize it too small for the text to fit, it will simply exit the application.
- All files created from your scans will be in the output folder.

### Step-by-step Setup Guide

1. Installing Kali Linux (Headless) using WSL
Install Kali Linux (Headless) using the command below:
    ```bash
    wsl --install kali-linux-headless
    ```

2. Updating Package Lists
Update the package lists for upgrades and new package installations:
    ```bash
    sudo apt update
   ```

3. Full System Upgrade
Perform a full system upgrade:
    ```bash
    sudo apt full-upgrade -y
    ```

4. Installing Kali Linux (Headless)
Install Kali Linux (Headless):
    ```bash
    sudo apt install -y kali-linux-headless
    ```

5. Running `run.sh` Script
    Run the `run.sh` script:
    ```bash
    sudo bash run.sh
    ```

6. Cloning the Repository
Clone this repository:
    ```bash
    git clone https://github.com/HFScripts/M.A.T.R.I.X.git
    ```

7. Changing Directory to Project Folder
Change directory into the project folder:
    ```bash
    cd M.A.T.R.I.X
    ```

8. Installing RustScan (version 2.0.1)
Download and install RustScan:
    ```bash
    wget https://github.com/RustScan/RustScan/releases/download/2.0.1/rustscan_2.0.1_amd64.deb
    sudo dpkg -i rustscan_2.0.1_amd64.deb
    rm rustscan_2.0.1_amd64.deb
    ```

9. Extracting HTTPX
If you want HTTPX to work, you need to extract it in the folder `utilities/tools/scripts/httpx.rar`. It was too large to upload to GitHub unzipped, but once the project setup is complete, this won't be a concern.


10. Now you can simply run the main.py file
    ```bash
    python main.py
    ```

## Post Setup

Once all the above steps are complete, your project setup is finished! You can now proceed with your development or testing tasks.

## To-Do List
- Configure the wordlist folder for tools such as `wfuzz`, `dnsrecon`, and `dirsearch`.
  - Display the wordlists in the selection to choose from as a number rather than word to stop typos.
- Fix the issue with `dirsearch` not being found.
- Remove color from `wpscan` output.
- Enclose the `sqlmap` command for the target in quotes.
- Ensure the target URLs are correctly specified; some tools may prefer URLs without the protocol (`http://` or `https://`) or `www.` prefix. This may require further testing, particularly for `wpscan`.
- Automate user interaction for `sqlmap` by answering "yes" to any prompts.
