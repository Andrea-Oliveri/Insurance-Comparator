# Swiss Health Insurance Comparator, by Andrea Oliveri

## Project Overview

The goal of the project is to implement a simple Streamlit app which can help in deciding which LAMal (base) health insurance offer is most convenient depending on the amount of money you expect to spend in the upcoming year.

<a href="https://lamal-swiss-insurance-comparator.streamlit.app/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" class="logo" alt="Streamlit App" width=200>
</a>

## Repository Structure

This directory contains the following files and directories:

* [**.streamlit**](.streamlit): Fodler containing streamlit configuration files.
* [**src**](src): Directory collecting all additional Python scripts and custom packages needed to run the application.
* [**insurance_comparator.py**](insurance_comparator.py): Main Python script used to run the Streamlit application.


## Getting Started

### 0) Python Environment

The Python enviroment used for this project was kept as simple as possible to prevent the size of the executable from increasing too much.

An environment containing the required packages with compatible versions can be created as follows:

```bash
conda create -n insurance python=3.13.9
conda activate insurance
pip install -r requirements.txt
```

### 1) Run

To run the Streamlit app, simply activate the correct conda environment and, from the same directory as the [**insurance_comparator.py**](insurance_comparator.py) file run:

```bash
streamlit run insurance_comparator.py
```