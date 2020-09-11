# semantic-similarity-stm

This repository contains scripts for systematic review on the semantic similarity effect on short-term memory.
The article will be publised soon.

Ishiguro, S., & Saito, S. (in press). The Detrimental Effect of Semantic Similarity in Short-Term Memory Tasks: A Meta-Regression Approach. *Psychonomic Bulletin & Review*

## Workflow

### OPTIONAL Modify Summary Table of previous studies
In case you want to include/exclude studies. It should contain effect sizes and file paths for the materials.

### Prepare for Materials and Norms
[English affective norms](https://link.springer.com/article/10.3758/s13428-012-0314-x)
Downloda 13428_2012_314_MOESM1_ESM.zip and place a file, BRM-emot-submit.csv in AffectiveNorms folder.

[Free association norms](https://smallworldofwords.org/en/project/research)
Download SWOW-EN2008 assoc. strengths (R123) [8Mb] and place a file, strength.SWOW-EN.R123.csv in AssociationNorms folder.

[French affective norms](https://link.springer.com/article/10.3758/s13428-013-0431-1)
Download ESM 2 (XLSX 284 kb) and place 13428_2013_431_MOESM2_ESM.xlsx in AffectiveNormsFrench folder.

### Materials in previous studies
Please contact the aurthor (ishiguro.sho.grocio@gmail.com). I will not distribute files of materials for copyright protection. Alternatively, manually fetch words from articles and create xlsx files.

### Do data Cleansing
Remove " and ' in strength.SWOW-EN.R123.csv (the original file)
```
cd Scripts/
bash data_cleansing.sh
```
Note. Locate where you save semantic-similarity-stm folder (e.g., ~/Downloads/semantic-similarity-stm).

### Create Association Matrix
Create association_matrix.csv.
```
python free_association_matrix_creator.py
```

### Run Main program
Main program loads the summary table and calculate Similarity and Connectivity.
```
python main_cal.py
```

### Do preprocess for analysis
```
cd ../StatisticalAnalysis/
python preprocess_forR.py
```

### Analyse data
```
Rscript meta_analysis.R
```

### Create tables of results with Similarity and Connectivity indexes (optional)
```
python table_construction.py
```

## Note
Below, `mean_dist_from_centroid` calculated (dis)similarity value for an example list (i.e., 'diamond, ... ,sapphire') and `connectivity_calc` calculated connectivity (or association stregnth) for another example list (i.e., 'apple, banana, orange'). These examples are used in my manuscript. Note that you should run `free_association_matrix_creator.py` and get a cue-response matrix containing words that you target before using `connectivity_calc` function.

I hope that these functions facilitate psychological studies!
```
>>> from grocio_utils import *
>>> mean_dist_from_centroid(['diamond', 'emerald', 'opal','pearl','ruby','sapphire'])
1.0449535299761725
>>> connectivity_calc(['apple','banana','orange'])
0.03786311822026108
```

## Dependencies
Python libraries: scipy, pandas, numpy, matplotlib, seaborn, xlrd, gensim, tqdm

R libraries: meta, metafor, dmetar, grid
