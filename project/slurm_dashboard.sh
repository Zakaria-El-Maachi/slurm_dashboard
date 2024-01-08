#!/bin/bash

# Define SSH connection and credentials
SSH_HOST="mohieddine.farid@simlab-cluster.um6p.ma"
SSH_PORT=8050

# Establish an SSH connection and set up port forwarding
ssh -L $SSH_PORT:localhost:$SSH_PORT $SSH_HOST << 'EOF'
  
# Navigate to the project directory
cd /home/mohieddine.farid/project || exit

# Load necessary modules
module purge
module load slurm/17.11.12
module load Python/3.8.2-GCCcore-9.3.0

# Create and/or activate the virtual environment
python3 -m venv newVirtual
source newVirtual/bin/activate

# Ensure pip is updated and install required libraries
pip install --upgrade pip
pip install pandas dash dash_bootstrap_components

# Run the dashboard script
python3 dashboard.py

EOF
