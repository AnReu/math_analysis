# Code for "Investigating the Use of Formulae in Math AR"

This repository contains the code to replicate the experiments for our paper "Investigating the Use of Formulae in Math AR".

## Website

The website for this project can be found here: [http://anreu.github.io/math_analysis/](http://anreu.github.io/math_analysis/).

## Fine-Tunining for Math AR

### Data Preparation

In order to prepare the data for crating the fine-tuning and evaluation data, call:

```
cd math_analysis/ft_datasets/
```

### Fine-Tuning
To create the fine-tuning data set, call:

```
cd math_analysis/ft_datasets/reusch/
python create_training_data_task1_parts.py

```

### Evaluation
To create the evaluation data sets (default, no-formulae, dummy-formulae, sorted), call:
```
cd math_analysis/ft_datasets/evaluation_data/scripts/
python create_topic_answer_files.py
```

## Fine-Tuning for Variable Overlap Prediction

The scripts to evaluate the variable overlap prediction task, please refer to the folder `var_pred`.

## Fine-Tuning for Math Structures

The scripts to evaluate the variable overlap prediction task, please refer to the folder `math_structures`.
