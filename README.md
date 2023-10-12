# Association Rule Mining on Different Dataset

## Overview

This README provides a guide on how to install the required libraries and apply association rule mining with a comparison between Brute-force and Apriori on different dataset 

## Installation

Before running the project, make sure you have Python installed on your system. Python 3.11 is required.

## Running the Project

Now that you have installed the required libraries, you can run the Random Forest Classifier project. Follow these
steps:

1. **Clone the Repository**:
   ```bash
   https://github.com/JindiHu/association-rule-mining.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd association-rule-mining
   ```

3. **Create a Virtual Environment (Optional but Recommended)**:

   Creating a virtual environment helps isolate project dependencies from your system-wide Python installation. To
   create a virtual environment, open your terminal/command prompt and run:

   ```bash
   python3 -m venv myenv
   ```
   Activate the virtual environment:

    - **On Windows**:

      ```bash
      myenv\Scripts\activate
      ```

    - **On macOS and Linux**:

      ```bash
      source myenv/bin/activate
      ```

4. **Install Required Libraries**:

   Install the necessary libraries using `pip3`:

   ```bash
   pip3 install -r requirements.txt
   ```

5. **Execute the Python Script**:
   ```bash
   python3 main.py
   ```

6. **View the Results**:

   The script will display figures (collected under `/figures` directory) performance metrics in terms of execution time for different association rule mining algorithm.



