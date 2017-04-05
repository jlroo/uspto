# USPTO - Trademark Parser

This application helps to parse XML files from the USPTO trademark public data that it is available in bulk form. From the XML files this packages generates python dictionaries that can be easily analyze or create CSV files to be work with other analytical tools. USPTO searchable data is viewable through a search interface on the Open Data site.

[https://developer.uspto.gov/product/trademark](https://developer.uspto.gov/product/trademark)

## Installing the package 

**System requirements**

* Python 3

**Python Hard Dependencies**

* xml
* zipfile
* gzip
* bz2

To install the package on the system located the source file and run:

`python setup install`

## USPTO Notebook

With this notebook and the uspto package you can parse the XML raw trademark data from the provided by USPTO.

### Loading packages 


```python
import pandas as pd
import uspto as pto
```

### Open USPTO File


```python
# Path to data
path = "/PATH_TO_DATA/uspto/apc161231-56.xml"
data = pto.openUSPTO(path)
```

### Get XML root

Getting the root might take a couple of minutes depending on size of the XML file and the RAM of your machine.


```python
data = pto.openUSPTO(path)
root = data.getroot()
```

### File Description

With the `pto.getDetails(root)` function we can extract useful information about the XML file also the volume of the trademark applications on the file.


```python
details = pto.getDetails(root)
pd.DataFrame.from_dict(details,orient='index')
```

# Extracting and Creating tables

## Case File Header 

Extract the case file header data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
file_header = pto.getFileHeader(root)
```


```python
table = pd.DataFrame.from_dict(file_header, orient='index')
table.head()
```


```python
table.to_csv("casefileHeader.csv")
```

## Case File Classification

Extract the case file classification data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
classifications = pto.getClassifications(root)
```

```python
data = []
for k in classifications.keys():
    for d in classifications[k]:
        data.append(classifications[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("classifications.csv")
```

## Case File Classification Codes

Extract the case file classification codes from the XML file, this table can also be obtanied from the classification table. This function creates a dictionary that can be transform as a table using Pandas.


```python
classification_codes = pto.getClassificationCodes(root)
```

```python
data = []
for k in classification_codes.keys():
    for d in classification_codes[k]:
        data.append(classification_codes[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("classification_codes.csv")
```

## Case File Design Search

Extract the case file Design Search data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
design = pto.getDesignSearch(root)
```

```python
data = []
for k in design.keys():
    for d in design[k]:
        data.append(design[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("designSearch.csv")
```

## Case File Owners

Extract the case file owners data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
owners = pto.getFileOwners(root)
```

```python
data = []
for k in owners.keys():
    for d in owners[k]:
        data.append(owners[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("fileOwners.csv")
```

## Case File Statements

Extract the case file statements data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
statements = pto.getFileStatements(root)
```

```python
data = []
for k in statements.keys():
    for d in statements[k]:
        data.append(statements[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("fileStatements.csv")
```

## Case File Foreign Applications

Extract the case file Foreign Applications data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
foreign = pto.getForeignApplications(root)
```

```python
data = []
for k in foreign.keys():
    for d in foreign[k]:
        data.append(foreign[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("foreignApplications.csv")
```

## Case File Prior Applications

Extract the case file Prior Applications data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
prior = pto.getPriorApplications(root)
```

```python
data = []
for k in prior.keys():
    for d in prior[k]:
        data.append(prior[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("priorApplications.csv")
```

## Case File Events

Extract the case file events data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
events = pto.getFileEvent(root)
```

```python
data = []
for k in events.keys():
    for d in events[k]:
        data.append(events[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("fileEvent.csv")
```

## Case File Correspondent

Extract the case file correspondent data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
correspondent = pto.getCorrespondent(root)
```

```python
data = []
for k in correspondent.keys():
        data.append(correspondent[k])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("correspondent.csv")
```

## Case File Madrid Filing

Extract the case file Madrid Filing data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.

```python
madrid_filing = pto.getMadridFiling(root)
```

```python
data = []
for k in madrid_filing.keys():
    data.append(madrid_filing[k])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("madridFiling.csv")
```

## Case File Madrid Events

Extract the case file Madrid Events data from the XML file. This function creates a dictionary that can be transform as a table using Pandas.


```python
madrid_events = pto.getMadridEvents(root)
```

```python
data = []
for k in madrid_events.keys():
    for d in madrid_events[k]:
        data.append(madrid_events[k][d])
```

```python
table = pd.DataFrame(data)
table.head()
```

```python
table.to_csv("madridEvents.csv")
```


## Tables 
The following table schema diagram from 2015 is a good example of what you can expect to be on the USPTO trademark data.

**case files schema high level 2015**
![](doc/case_files_schema.png)