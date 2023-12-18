# HPC Cluster Usage Dashboard Project

## 1. Collecting Data with `sacctmgr`

### Objective
Gather detailed usage data from your HPC cluster.

### Steps
- **Learn `sacctmgr`**: Understand the command options and outputs to extract relevant data.
- **Scripting Regular Data Collection**:
  - Create a script to run `sacctmgr` at regular intervals.
  - Extract data like user IDs, CPU/GPU usage hours per user, and other pertinent metrics.
- **Data Storage**:
  - Choose between CSV file or database for storage.
  - Implement data appending or updating mechanism.

## 2. Data Analysis with Python

### Objective
Process and analyze the collected data.

### Tools
- Python
- Pandas library

### Steps
- **Data Loading**: Write Python code to load data.
- **Data Processing**: Use Pandas for cleaning, sorting, and aggregating data.

## 3. Creating a Dashboard with Dash

### Objective
Build an interactive web dashboard to display the data.

### Tools
- Dash framework
- Plotly for charting

### Steps
- **Learn Dash**: Get familiar with Dash components and layout.
- **Designing the Dashboard**:
  - Plan layout and interactive elements.
  - Choose charts (bar, pie, etc.) for data representation.
- **Implementing the Dashboard**:
  - Code the dashboard using Dash.
  - Test and refine the user interface.

## 4. Creating the README.md File

### TODO: Key Elements To Add
- **Project Overview**: Explain the purpose and scope.
- **Technologies Used**: List technologies and reasons for choice.
- **Setup and Installation**: Guide on setup and running.
- **Usage Guide**: How to use the dashboard, with visuals.
