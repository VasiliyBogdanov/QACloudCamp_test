# This is test task for QACloudCamp by Cloud.ru
```test_strategy.doc``` - first part of this test task
## Installation
#### Required python version ```^3.5``` - found out using [Vermin](https://github.com/netromdk/vermin)
### Manually
- clone or download this repository
- from project root directory:
    - create virtual environment. For example ```python -m venv .venv```
    - activate it ```source .venv/bin/activate```
    - install dependencies ```pip install -r requirements.txt```
### Docker
- from project root directory:
    - docker build -t qacodecamp_vb:01 .
    - docker run qacodecamp_vb:01

### Running tests
From the root project directory run ```pytest```\
Or ```make run_tests```
### Useful pytest flags
```-v``` verbose output\
```-vv``` even more verbose output\
```-k``` select tests by some keyword expression. Refer to pytest docs for more detailed explanation