"""
Create a the Supervisely-format dataset from Darknet-COCO format.
The standard Supervisely dataset format contains the images (*.jpg)
and the labels (*.json). This file converts the dataset as a folder
from another folder in Darket-COCO format.

References:
    - https://docs.supervise.ly/data-organization/import-export/supervisely-format
    - https://docs.supervise.ly/data-organization/import-export/upload
"""

import argparse
import glob
import json
import os
import random
import shutil

import cv2
# import numpy as np
from tqdm import tqdm

COLORS = ['#1abc9c', '#3498db', '#9b59b6', '#f1c40f', '#2ecc71', '#e67e22', '#e74c3c', '#ecf0f1', '#95a5a6']


def get_ann_boxes(path):
    """Get boxes from the annotation of one image: cls_id, cx, cy, w, h
    """
    boxes = []
    with open(path, 'r') as f:
        for line in f:
            line = line[:-1].split()
            line[0] = int(line[0])  # cls id
            line[1:] = [float(i) for i in line[1:]]  # x y w h
            boxes.append(line)
    return boxes


def make_supervisely_dataset(origin_path, project_path, dataset_name, labels):
    # Path configuration
    save_ann_path = os.path.join(project_path, dataset_name, 'ann')
    save_img_path = os.path.join(project_path, dataset_name, 'img')
    img_paths = sorted(glob.glob(origin_path + '/images/' + '*.jpg'))
    ann_paths = sorted(glob.glob(origin_path + '/labels/' + '*.txt'))

    # New folder
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    os.makedirs(save_ann_path)
    os.makedirs(save_img_path)

    # json for the whole project
    meta = {
        'classes': [],
        'tags': []
    }
    if len(labels) <= len(COLORS):
        for i, l in enumerate(labels):
            cls = {
                'title': l,
                'shape': 'rectangle',
                'color': COLORS[i],
                'geometry_config': {}
            }
            meta['classes'].append(cls)
    else:
        for i, l in enumerate(labels):
            cls = {
                'title': l,
                'shape': 'rectangle',
                'color': "#%06x" % random.randint(0, 0xFFFFFF),
                'geometry_config': {}
            }
            meta['classes'].append(cls)

    with open(os.path.join(project_path, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=True)

    # json for an image
    for i in tqdm(range(len(img_paths)), desc='Images'):
        ip = img_paths[i]
        ap = ann_paths[i]
        ann_json = {
            "description": "",
            "tags": [],
            "size": {},
            "objects": []
        }
        # Read image size
        img = cv2.imread(ip)
        h, w = img.shape[:2]
        ann_json['size']['height'] = h
        ann_json['size']['width'] = w

        # Read bounding boxes
        boxes = get_ann_boxes(ap)
        for b in boxes:  # b: (cls id, center x, center y, w, h)
            xmin = int(max(b[1] - b[3] / 2, 0) * w)
            ymin = int(max(b[2] - b[4] / 2, 0) * h)
            xmax = int(min(b[1] + b[3] / 2, 1) * w)
            ymax = int(min(b[2] + b[4] / 2, 1) * h)

            obj = {}
            obj['description'] = ''
            obj['geometryType'] = 'rectangle'
            obj['tags'] = []
            obj['classTitle'] = labels[int(b[0])]
            obj['points'] = {}
            obj['points']['exterior'] = []
            obj['points']['exterior'].append([xmin, ymin])
            obj['points']['exterior'].append([xmax, ymax])
            obj['points']['interior'] = []
            ann_json['objects'].append(obj)

        # Save json
        ann_json_path = os.path.join(save_ann_path, os.path.basename(ip) + '.json')
        with open(ann_json_path, 'w') as f:
            json.dump(ann_json, f, indent=True)

        # Copy image
        shutil.copy(ip, save_img_path)

    # Summary
    print('Done. Supervisely dataset saved to %s' % (project_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--origin', type=str, default='./dataset',
                        help='The name of original dataset in darknet format', required=True)
    parser.add_argument('-p', '--project', type=str, default='./superset',
                        help='The name of the output project folder.', required=True)
    parser.add_argument('-d', '--dataset', type=str, default='theset',
                        help='The name of the output dataset folder in supervisely format.', required=True)
    parser.add_argument('-l', '--label', action='append', help='Labels', required=True)
    opt = parser.parse_args()
    print(opt)

    make_supervisely_dataset(
        origin_path=opt.origin,
        project_path=opt.project,
        dataset_name=opt.dataset,
        labels=opt.label
    )
