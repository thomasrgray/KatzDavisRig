# Experimental Data Storage

## File Naming Convention

When saving experiment data files, use the following naming format:

Date-AnimalID-Experiment

## File Components:
1. **Date**: The date of the experiment, formatted as MMDD (e.g., 0924 for September 24).
2. **AnimalID**: The unique identifier for the animal (e.g., TG100).
3. **Experiment**: The type of experiment. Choose one from the following options:
###
   - `_prettest`
   - `_D1`
   - `_D2`
   - `_D3`
   - `_D4`
   - `_D5`
   - `_D6`
   - `_posttest`
   - `_posttest2`

### Example File Names:
- `0924TG100_D1.ms8.txt`
- `0924TG100_posttest.ms8.txt`

## Folder Structure

Files should be organized into the following directory structure:

``` { .sh .no-copy }
├─ Thomas/
│  ├─ Ortho/
│  │  ├─ Enriched/
│  │  │  ├─ TG100-101_Training/
│  │  │  ├─ TG100-101_Hab/
│  │  │  └─ TG100-101_Tests/
│  │  └─ Unenriched/
│  │     ├─ TG102-103_Training/
│  │     ├─ TG102-103_Hab/
│  │     └─ TG102-103_Tests/
│  ├─ Retro/
│  │  ├─ Enriched/
│  │  │  ├─ TG104-105_Training/
│  │  │  ├─ TG104-105_Hab/
│  │  │  └─ TG104-105_Tests/
│  │  └─ Unenriched/
│  │     ├─ TG106-107_Training/
│  │     ├─ TG106-107_Hab/
│  │     └─ TG106-107_Tests/
│  └─ Combined/
│     ├─ Enriched/
│     │  ├─ TG108-109_Training/
│     │  ├─ TG108-109_Hab/
│     │  └─ TG108-109_Tests/
│     └─ Unenriched/
│        ├─ TG110-111_Training/
│        ├─ TG110-111_Hab/
│        └─ TG110-111_Tests/
```


### Steps to Save Files:
1. **Navigate to the relevant experiment folder**:
   - Choose `Ortho`, `Retro`, or `Combined`.
   - Within the chosen experiment folder, select `Enriched` or `Unenriched`.

2. **Find the appropriate condition folder**:
   - Choose from `TG100-101_Training`, `TG100-101_Hab`, or `TG100-101_Tests`.

3. **Save the file using the naming convention**.

### Example Path:
For a posttest experiment on September 24 for animal TG100, the file should be saved as follows:

/Thomas/Ortho/Enriched/TG100-101_Tests/0924TG100_posttest


### Breakdown:
- **Thomas**: Base folder for user data.
- **Ortho**: Modality folder.
- **Enriched**: Condition folder.
- **TG100-101_Tests**: Folder for tests.
- **0924TG100_posttest**: Filename, where:
  - **0924** is the date of the experiment.
  - **TG100** is the Animal ID.
  - **_posttest** is the experiment type.

###

Once all files are stored you can export the data for analysis by emailing it to yourself.

