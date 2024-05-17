#!/bin/bash

#To Run this Script
#chmod +x setup_project.sh
#./setup_project.sh

# Step 1: Create a temporary virtual environment
python3 -m venv temp_env

# Step 2: Activate the virtual environment
source temp_env/bin/activate  # On Windows use: temp_env\Scripts\activate

# Step 3: Upgrade pip
pip install --upgrade pip

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Run the project
python main.py

# Step 6: Initialize a Git repository
git init

# Step 7: Create .gitignore file
cat <<EOL > .gitignore
temp_env/
__pycache__/
*.pyc
*.pyo
*.pyd
*.csv
*.log
*.DS_Store
EOL

# Step 8: Add all files to Git and commit
git add .
git commit -m "Initial commit with project structure and scripts"

# Optional: Deactivate the virtual environment
deactivate
