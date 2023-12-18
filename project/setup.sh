#!/bin/bash

chmod +x db.py
chmod +x getInfo.sh
chmod +x data_analysis.py
chmod +x dashboard.py
module purge
module load slurm/17.11.12
module load python-3.9.10-gcc-4.8.5-knkivo6
module load py-pip-21.3.1-gcc-4.8.5-qge5kol 

echo "Do not forget to setup the crontab (crontab -e) and set db.py and getInfo.sh"
