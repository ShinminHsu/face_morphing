# face_morphing
Data Augmentation via Face Morphing for Recognizing Intensities of Facial Emotions.

This repo is the implementaion of our [paper](https://ieeexplore.ieee.org/document/9484732).
If you use the code, please cite the paper:

```
T. -R. Huang, S. -M. Hsu and L. -C. Fu,
"Data Augmentation via Face Morphing for Recognizing Intensities of Facial Emotions,"
in IEEE Transactions on Affective Computing,
doi: 10.1109/TAFFC.2021.3096922.
```

# Overview
The structure of the repository is the following:

- `human_validation`: data and analysis code using in human validation part.
- `machine_validation`: codes using for morphing images, train and testing.
- `images`: images that our raters saw and rated.

## Human validation

Files are described as follows:

1. Human rating
Raw rating scores from both Caucasian and Taiwanese raters.
- human_rating_caucasian.csv
- human_rating_taiwanese.csv

2. Summary
The mean and standard deviation of rating scores of each image.
- caucasian_summary.csv
- taiwanese_summary.csv

3. Raters information
These files contain information of our raters, including age, gender, and nationality.
- raters_info_caucasian.csv
- raters_info_taiwanese.csv

## Machine validation

For face morpher we use, please refer to this [repo](https://github.com/alyssaq/face_morpher).

Our input database stored in `pickle`.
For more implementaion details, please refer to our paper.




