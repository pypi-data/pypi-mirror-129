# vdataset

![python](https://img.shields.io/static/v1?logo=python&labelColor=3776AB&color=ffffff&logoColor=ffffff&style=flat-square&label=%20&message=Python3)
![pytorch](https://img.shields.io/static/v1?logo=pytorch&labelColor=EE4C2C&color=ffffff&logoColor=ffffff&style=flat-square&label=%20&message=Pytorch)

## Description

Load video datasets to PyTorch DataLoader. (Custom Video Data set for PyTorch DataLoader)
</br>
**VDataset can be use to load 20BN-Jester dataset to the PyTorch DataLoader**

## Required Libraries

- torch
- Pillow
- pandas

## Arguments

### LableMap Constructor

| Argument        | Type      | Required | Default | Description                                                                        |
| --------------- | --------- | -------- | ------- | ---------------------------------------------------------------------------------- |
| labels_csv      | str       | False    | None    | The path to the csv file containing the labels and ids.                            |
| labels_col_name | str       | False    | None    | The name of the column containing the labels. (Required if labels_csv is not None) |
| ids_col_name    | str/ None | False    | None    | The name of the column containing the ids.                                         |
| id_type         | type      | False    | int     | The type of the ids.                                                               |

### VDataset Constructor

| Argument              | Type          | Required | Default  | Description                                                                                          |
| --------------------- | ------------- | -------- | -------- | ---------------------------------------------------------------------------------------------------- |
| csv_file              | str           | True     | -        | Path to .csv file                                                                                    |
| root_dir              | str           | True     | -        | Root Directory of the video dataset                                                                  |
| file_format           | str           | False    | jpg      | File type of the frame images (ex: .jpg, .jpeg, .png)                                                |
| id_col_name           | str           | False    | video_id | Column name, where id/name of the video on the .csv file                                             |
| label_col_name        | str           | False    | label    | Column name, where label is on the .csv file                                                         |
| frames_limit_mode     | str/None      | False    | None     | Mode of the frame count detection ("manual", "csv" or else it auto detects all the frames available) |
| frames_limit          | int           | False    | 1        | Number of frames in a video (required if frames_count_mode set to "manual")                          |
| frames_limit_col_name | str           | False    | frames   | Column name, where label is on the .csv file (required if frames_count_mode set to "csv")            |
| video_transforms      | tuple/None    | False    | None     | Video Transforms (Refer: <https://github.com/hassony2/torch_videovision>)                            |
| label_map             | LabelMap/None | False    | None     | Label Map of the Dataset                                                                             |

## Usage

```python
from vdataset import LabelMap, VDataset

from torch.utils.data import DataLoader

from torchvideotransforms.volume_transforms import ClipToTensor # https://github.com/hassony2/torch_videovision
from torchvideotransforms import video_transforms, volume_transforms # https://github.com/hassony2/torch_videovision

# Create Label Map
label_map = LabelMap(labels_csv="/path-to-csv/csv_file.csv", labels_col_name="label")

print(label_map)
print(label_map.get_dict())

# Use Video Transformers
video_transform_list = [video_transforms.RandomRotation(30),
            video_transforms.Resize((100, 100)),
            volume_transforms.ClipToTensor()]
video_transforms = video_transforms.Compose(video_transform_list)

# Create Vdataset
dataset = VDataset(csv_file='/path-to-csv/csv_file.csv', root_dir='/path-to-root/', video_transforms=video_transforms, label_map=label_map)

dataloader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=2, pin_memory=True)
print(dataloader)

for image, label in dataloader: # Do what do you want in dataset
    print(image, label)
    break

```
