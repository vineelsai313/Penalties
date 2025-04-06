# Traffic Norms Simulation in AOPL and ASP

## Overview
This repository contains the implementation of a traffic norms simulation designed to explore how agents react in various traffic scenarios, particularly focusing on emergency vs. non-emergency situations. The simulation is developed using AOPL (Agent-Oriented Programming Language) and ASP (Answer Set Programming).

## Description
The simulation models a traffic domain that includes various traffic signs, lights, and other regulatory elements. It defines policies for vehicular behavior in response to these elements under different circumstances, including emergency responses.

### Files and Directories
- **AOPLtranslation4.txt**: Contains AOPL translations necessary for setting up the simulation environment.
- **dynamic_domain.txt**: Includes code and data for the traffic norms domain, detailing traffic lights, signs, pedestrian crossings, and other domain-specific elements.
- **penalty_and_time.txt**: Manages penalties and time calculations within the simulation. It includes penalty priorities and time adjustments based on the traffic norms.
- **policies11.txt**: Defines the policies and obligations that vehicles must adhere to within the traffic domain, detailing operational rules under various scenarios.
- **test1scenario1.txt**: Describes specific test scenarios including starting points, goals, and whether the situation is an emergency or non-emergency.

## Installation
Before running the simulation, ensure that the Clingo solver is installed on your system. Clingo is an ASP (Answer Set Programming) solver used for logic-based reasoning. Follow these steps to install Clingo:

### For Ubuntu/Linux:
```bash
sudo apt-get install gringo

### For macOS:
Clingo can be installed using Homebrew:
```bash
brew install clingo

### For Windows:
Clingo can be installed on Windows using the binary releases provided by the Potassco team. Follow these steps:
1. Visit the Potassco GitHub releases page: [Potassco Clingo Releases](https://github.com/potassco/clingo/releases)
2. Download the latest release suitable for Windows.
3. Extract the downloaded files to a directory of your choice.
4. Optionally, add the directory where you extracted Clingo to your system's PATH to run it from the command line.

After installing Clingo, no further setup is required for the simulation files.

## Usage
To run the simulation, follow these steps:

1. Ensure all simulation files are in your working directory.
2. Open a command line interface in the directory.
3. Execute the simulation using Clingo with the main AOPL and ASP files. For example (this is an example command, adjust as necessary based on your file configuration):
   ```bash
   clingo AOPLtranslation4.txt dynamic_domain.txt penalty_and_time.txt policies11.txt test1scenario1.txt
4. Review the output that Clingo returns, which will detail the results of the simulation based on the test scenarios provided in test1scenario1.txt.

## AOPL to ASP Translator

### Overview
To facilitate the integration of AOPL policies into our ASP-based framework, we have developed `AOPL_to_ASP_translator.py`, a Python-based translator. This tool automates the translation of policies encoded in AOPL into ASP, enhancing the efficiency of policy implementation and execution within the system.

### Functionality
The translator takes a text file containing AOPL policies as input. These policies include details on associated penalties, as defined in the extended AOPL version presented in Section 4.1 of our documentation. Utilizing the reified logic programming encoding technique introduced by Inclezan (2023), the translator outputs ASP encodings for all provided policies and penalties.

### Usage
To use the AOPL to ASP translator, follow these steps:

1. Ensure that `AOPL_to_ASP_translator.py` is located in your working directory.
2. Prepare a text file containing the AOPL policies for your specific domain. Ensure that this file adheres to the syntax and structure outlined in Section 4.1.
3. Execute the translator via the command line by running the following command:
   ```bash
   python AOPL_to_ASP_translator.py your_policy_file.txt
Replace your_policy_file.txt with the name of your file containing the AOPL policies.
4. The translator will generate the corresponding ASP code for the policies and penalties specified in the input file. The output will be saved in the same directory, typically with a naming convention that reflects the input file name appended with _ASP_output.

