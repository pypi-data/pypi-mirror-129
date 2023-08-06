# Learning Certifiably Optimal Checklists

## Environment and Prerequisites
Run the following commands to create the Conda environment:

```
cd IP_Checklists/
conda env create -f environment.yml
conda activate ip_checklists
```

You will have to separately download and install [CPLEX Optimization Studio](https://www.ibm.com/ca-en/products/ilog-cplex-optimization-studio) (we use version 12.10) and install the provided Python package.

## Training a Single Checklist

To train a single checklist using the MIP formulation in an ad-hoc fashion, we provide a demonstration on the CRRT dataset in [notebooks/demo.ipynb](notebooks/demo.ipynb).

## Training a Grid of Checklists

To reproduce the experiments in the paper which involve training a grid of checklists using different methods, use sweep.py as follows:

```
python sweep.py launch \
    --experiment {experiment_name} \
    --output_dir {output_root} \
    --command_launcher {launcher} 
```

where:
- `experiment_name` corresponds to experiments defined as classes in `experiments.py`
- `output_root` is a directory where experimental results will be stored
- `launcher` is a string corresponding to a launcher defined in `launchers.py` (i.e. `slurm` or `local`).

We provide our notebook for aggregating results and creating figures in [notebooks/agg_results.ipynb](notebooks/agg_results.ipynb).