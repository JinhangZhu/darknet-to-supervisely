<h2 align="center">darknet-to-supervisely</h2>
<p align="center"><b>Conversion of Dataset from Darknet Format into Supervisely Format via Python</b></p>

<br>

<h2>Table of Contents</h2>

<!-- TOC -->

- [Introduction](#introduction)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [References](#references)
- [License](#license)

<!-- /TOC -->


### Introduction

This repository shows a quick method to convert the dataset in the Darknet format into the JSON-based format required by Supervisely annotation tool in python language. Check it out!

### Usage

Clone the repository to your local path:

```bash
git clone https://github.com/JinhangZhu/darknet-to-supervisely.git
```

Copy the `convert.py` file into your local folder where the darknet dataset is located. Open the terminal on Linux or command window in Windows and run command like:

```bash
python convert.py -o ./ego-hand -p ./new-project -d new-set -l left_hand -l right_hand
```

help:

- `-o`, `--origin`: The name of original data downloaded from Supervisely. `type=str`
- `-p`, `--project`: The name of the output dataset folder. `type=str`
- `-d`, `--dataset`: The name of the meta file of the data. `type=str`
- `-l`, `--label`: Whether to randomly split image set. `action='append'`

For example, I have a folder called: "ego-hand" in the current path, I want to create a dataset folder called "epichands" under the directory of project "epichhands", with labels: `left_hand`, `right_hand`. I run:

```bash
python convert.py -o ./ego-hand -p ./epichands -d epichands -l left_hand -l right_hand
Namespace(dataset='epichands', label=['left_hand', 'right_hand'], origin='./ego-hand', project='./epichands')
Images:   3%|██▌                                                                             | 415/12846 [00:13<06:29, 31.90it/s]
```

Results:

```
└───datasets                                                                   		
		├───ego-hand
		├───epichhands
				├───meta.json
				├───ann
					├───xxx.jpg.json
				├───img
					├───xxx.jpg
```


### Maintainers

[Jinhang Zhu](https://github.com/JinhangZhu)



### References

- https://docs.supervise.ly/data-organization/import-export/supervisely-format

- https://docs.supervise.ly/data-organization/import-export/upload



### License

- [MIT](https://opensource.org/licenses/MIT)
