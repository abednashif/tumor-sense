<div style="font-size: 6ch; text-align: center"> TumorSense </div>

A deep learning-based project that utilizes artificial intelligence for the detection of brain tumors in medical images.

### Table of Contents
- [Introduction](#Introduction)
- [Dataset](#Dataset)
- [Model Architecture](#model-architecture)
- [Results](#results)
- [Contributing](#contribution)



# Introduction
<div style="font-family: Overpass, 'roboto',serif;">
    A brain tumor is a mass or growth of abnormal cells in your brain.
    Many different types of brain tumors exist. Some brain tumors are noncancerous (benign), and some brain tumors are cancerous (malignant). Brain tumors can begin in your brain (primary brain tumors), or cancer can begin in other parts of your body and spread to your brain as secondary (metastatic) brain tumors.
    
<div style="text-align: center; margin-top: 2em;">
    <img width="300px" src="https://www.mayoclinic.org/-/media/kcms/gbs/patient-consumer/images/2014/10/30/15/17/mcdc7_brain_cancer-8col.jpg" alt="brain_tumor_image"/>
</div>

### 1. Glioma
Glioma is a type of tumor that occurs in the brain and spinal cord. Gliomas begin in the gluey supportive cells (glial cells) that surround nerve cells and help them function. Three types of glial cells can produce tumors. A glioma can affect your brain function and be life-threatening depending on its location and rate of growth. Gliomas are one of the most common types of primary brain tumors.
<div style="text-align: center">
    <img width="300px" src="https://assets.cureus.com/uploads/figure/file/164887/lightbox_0a114f70280b11eb8f411b16d840121c-final-2.png" alt="giloma"/>
</div>

### 2. Meningioma
A meningioma is a tumor that arises from the meninges — the membranes that surround the brain and spinal cord. Although not technically a brain tumor, it is included in this category because it may compress or squeeze the adjacent brain, nerves and vessels. Meningioma is the most common type of tumor that forms in the head.
Most meningiomas grow very slowly, often over many years without causing symptoms. But sometimes, their effects on nearby brain tissue, nerves or vessels may cause serious disability.
<div style="text-align: center">
    <img width="600px" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTjOeFTen8qxZfMRwXKXQlwUN0TWkMPMvzfig&usqp=CAU" alt="meningioma">
</div>

### 3. Pituitary Tumors (Adenoma)
Pituitary tumors are abnormal growths that develop in your pituitary gland. Some pituitary tumors result in too much of the hormones that regulate important functions of your body. Some pituitary tumors can cause your pituitary gland to produce lower levels of hormones. Most pituitary tumors are noncancerous (benign) growths (adenomas). Adenomas remain in your pituitary gland or surrounding tissues and don't spread to other parts of your body.
<div style="text-align: center">
    <img width="400px" src="https://assets.cureus.com/uploads/figure/file/71851/lightbox_0e62470096cb11e989a2d7e4904c7be4-Figure-2a.png" alt="pituitary"/>
</div>

</div>


# Dataset
We collected a dataset of brain MRI images from openly available MRI datasets on Kaggle, HuggingFace,
we used ~10k images, 82% of the dataset is used for training, whereas 18% of the dataset is used for testing. <br>
Images are all scaled to 224 x 224, to improve the model's generalizability, data augmentation
stratagies can be used to increase the diversity of the training sample when the dataset volume is small.

- Data collection 
<table style="margin-left: 2rem">
<thead>
    <th>Class</th>
    <th>Training Total</th>
    <th>Testing Total</th>
</thead>
<tbody>
    <tr><td>Giloma</td><td></td></tr>
    <tr><td>Pituary</td><td></td></tr>
    <tr><td>Meningioma</td><td></td></tr>
    <tr><td>Normal</td><td></td></tr>
</tbody>
</table>

- Data Preprocessing and Augmentation


# Model Architecture

# Results


# Contribution


