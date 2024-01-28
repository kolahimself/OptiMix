# OptiMix

## Project Description

OptiMix is an interactive software developed with the goal of simplifying concrete mix design.

With specified targets for compressive strength, workability, durability, OptiMix determines the right proportions of cement, aggregates, water and optional substitute binders (fly-ash or slag) — all in a few clicks.

OptiMix is not intended to supplant or compete with commercially available software packages. Rather, it's a passion project built mainly for exhibition & demonstration's sakes.

## Key Features 

- OptiMix, which utilizes the British `DOE ` design method, generates the required proportions for:
	- Normal concrete mixes,
	- Air-entrained concrete mixes,
	- Portland cement/pulverised fuel-ash concrete mixes,
	- Portland cement/ground granulated blastfurnace slag concrete mixes.
- It features an interactive front-end interface that enables users to provide required information in five stages.
- Users can track results for each stage in real-time, as well as view the final mix proportions. Summaries of the mix design can also be saved as `.pdf`, `.xlsx` and `.docx`.

## Getting Started

Ensure that you have python installed before proceeding. Then, follow these steps to install and launch OptiMix:

### Installation
Get started with OptiMix by either cloning the repository with `git clone https://github.com/kolahimself/OptiMix.git` (or manually extracting the downloaded zip file), navigating to the `OptiMix` directory, and installing dependencies with `pip install -r requirements.txt`. 

```bash
git clone https://github.com/kolahimself/OptiMix.git
cd OptiMix
pip install -r requirements.txt
```
### Launching OptiMix
Once ready, simply run the launcher script:

```bash
python optimix_launcher.py
```
### Usage
OptiMix's usage guide is available [here](assets/readme/Usage.md)
## Important Considerations
- OptiMix is not applicable for high Portland cement/ggbs mixes (>40%). Refer to detailed information from cement manufacturer's or the supplier of ggbs.
- OptiMix does not currently handle specialty materials like lightweight aggregates or special concrete mixes.
- Trial mixing remains essential, you should check whether constituent materials selected for use will behave as designed and adjust accordingly.
## Disclaimer
While every effort has been made to ensure the accuracy and reliability of this tool, users are responsible for exercising their professional judgement and conducting quality control procedures.

