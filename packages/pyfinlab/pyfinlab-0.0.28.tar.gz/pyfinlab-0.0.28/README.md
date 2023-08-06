







# PyFinanceLab

PyFinanceLab is a library which brings together various financial applications into one package for research and portfolio management. Navigate to the jupyter folder of the pyfinlab repository to see usage examples. 

PyFinanceLab is in pre-alpha development. 


## Features

* **Data API Wrapper**
	 The data API wrapper makes it easy to switch between [yfinance](https://github.com/ranaroussi/yfinance) (free to use) and [tia](https://github.com/PaulMest/tia) ([Bloomberg Professional Services](https://www.bloomberg.com/professional/) subscription) Python libraries for pulling financial data. 

* **Portfolio Optimization**
	Compute an efficient frontier of portfolios based on any one of 7 risk models and 3 return models from the [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/en/latest/) library.

* **Multifactor Scoring Model**
	Analyze and rank stocks according to factors assumed to have excess returns and violate the efficient market hypothesis. 

* **Optimizer Backtest**
	Backtest optimized portfolios and compute performance charts, efficient frontier plots, and performance statistics. 

* **Excel Report Generation**
	Show your optimizer results and backtest in a nicely formatted Excel file for further analysis. 
    

## Installation

It is recommended you use Anaconda for this installation process. [Anaconda Individual Edition](https://www.anaconda.com/products/individual) is appropriate for most users. Make sure you have installed [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed on your computer. If you encounter any errors with, "Microsoft Visual C++ 14.0 is required", try following [these instructions](https://stackoverflow.com/a/55370133/16367225) to download and install Microsoft Visual C++ 14.0. If you get an error installing any of the packages below, try to install the problematic package separately. 

### Setting Up Anaconda Environment for PyFinLab

Open Anaconda Prompt and create a new environment called pyfinlab. 
```
conda create -n pyfinlab python=3.8 git
```

Activate the new pyfinlab environment. 
```
conda activate pyfinlab
```

Install the following conda packages using conda-forge channel. 
```
conda install -c conda-forge blpapi jupyterlab xlsxwriter tqdm
```

Install the following conda packages using anaconda channel. 
```
conda install -c anaconda xlsxwriter statsmodels
```
Install the following GitHub repositories one at a time. 
```
pip install git+https://github.com/PaulMest/tia.git#egg=tia
```
```
pip install git+https://github.com/nathanramoscfa/ffn.git
``` 
Install the following packages using pip. 
```
pip install --upgrade-strategy only-if-needed yfinance tqdm openpyxl patsy openpyxl bt PyPortfolioOpt
```


### Installing PyFinLab

Install pyfinlab to your environment's site-packages folder with the following command. 
```
pip install pyfinlab
``` 
Clone the GitHub repository to a project directory of your choosing. 
```
git clone git+https://github.com/nathanramoscfa/pyfinlab.git
``` 


## Roadmap

Future development will include:
    
* **Documentation and Testing**

    Documentation and testing will be published as this Python library is further developed. 

