<!-- Davis Rig Documentation -->

# Katz Lab Davis Rig Documentation

## Overview

The Davis Rig is a brief-access task rig designed for rats, primarily for the purpose of investigating behavioral responses. This documentation provides an overview of the hardware setup, software configuration, experimental protocols, data exporting, and data analysis.

---

## Table of Contents
- [Overview](#overview)
- [Hardware](#hardware)
- [Software](#software)
- [Experimental Protocols](#experimental-protocols)
- [Data Exporting](#data-exporting)
- [Data Analysis](#data-analysis)

---

## Hardware

The Davis Rig consists of several key components:
- Nosepoke detection system
- Reward delivery mechanism
- Data acquisition module
- Rat chamber

Further details on hardware assembly and configuration can be found in the [Building](building/) section.

---

## Software

### Overview

The Davis Rig is powered by the **Bpod** software, a versatile tool for controlling behavioral experiments. 

### Installation

To install the software:
1. Download the Bpod software from [Sanworks](https://sanworks.io/).
2. Follow the setup guide provided in the Bpod documentation.

---

## Experimental Protocols

### Setting Up an Experiment

1. Ensure that all hardware is properly connected and powered.
2. Open the Bpod software and configure the task parameters.
3. Use the protocol template provided by the Katz Lab to structure the task.

---

## Data Exporting

### Exporting Data from the Rig

Data collected from the Davis Rig can be exported in the following formats:
- CSV
- JSON

To export data:
1. Navigate to the data export section in the Bpod software.
2. Select the desired format and download.

---

## Data Analysis

### Analyzing Behavioral Responses

Data analysis can be performed using Python or MATLAB. The following libraries are recommended:
- **Pandas** (Python) for data manipulation.
- **MATLAB** for in-depth statistical analysis.

Check out our example analysis scripts in the [Github Repository](https://github.com/thomasrgray/turbulator-olfactometer).

---

## Building

This section includes detailed instructions on how to assemble the Davis Rig from scratch.

Next: [Building](building/)

---

<!-- Footer -->

<footer>
    Copyright &copy; 2024 Thomas Gray
    Made with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
</footer>
