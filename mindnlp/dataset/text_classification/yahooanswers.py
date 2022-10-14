# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
YahooAnswers dataset
"""
# pylint: disable=C0103

import os
import csv
from typing import Union, Tuple
from mindspore.dataset import GeneratorDataset
from mindnlp.utils.download import cache_file
from mindnlp.dataset.register import load
from mindnlp.configs import DEFAULT_ROOT
from mindnlp.utils import untar

URL = "https://drive.google.com/uc?export=download&id=0Bz8a_Dbh9Qhbd2JNdDBsQUdocVU&confirm=t"

MD5 = "f3f9899b997a42beb24157e62e3eea8d"


class Yahooanswers:
    """
    YahooAnswers dataset source
    """

    def __init__(self, path) -> None:
        self.path: str = path
        self._label, self._title_text = [], []
        self._load()

    def _load(self):
        csvfile = open(self.path, "r", encoding="utf-8")
        dict_reader = csv.reader(csvfile)
        for row in dict_reader:
            self._label.append(int(row[0]))
            self._title_text.append(f"{row[1]} {row[2]} {row[3]}")

    def __getitem__(self, index):
        return self._label[index], self._title_text[index]

    def __len__(self):
        return len(self._label)


@load.register
def YahooAnswers(
    root: str = DEFAULT_ROOT,
    split: Union[Tuple[str], str] = ("train", "test"),
    proxies=None,
):
    r"""
    Load the YahooAnswers dataset
    Args:
        root (str): Directory where the datasets are saved.
            Default:'~/.mindnlp'
        split (str|Tuple[str]): Split or splits to be returned.
            Default:('train', 'test').

    Returns:
        - **datasets_list** (list) -A list of loaded datasets.
            If only one type of dataset is specified,such as 'trian',
            this dataset is returned instead of a list of datasets.

    Examples:
        >>> dataset_train,dataset_test = YahooAnswers()
        >>> train_iter = dataset_train.create_tuple_iterator()
        >>> print(next(train_iter))

    """

    cache_dir = os.path.join(root, "datasets", "YahooAnswers")
    path_dict = {
        "train": "train.csv",
        "test": "test.csv",
    }
    column_names = ["label", "title_text"]
    path_list = []
    datasets_list = []
    path, _ = cache_file(
        None,
        cache_dir=cache_dir,
        url=URL,
        md5sum=MD5,
        download_file_name="yahoo_answers_csv.tar.gz",
        proxies=proxies,
    )

    untar(path, cache_dir)
    if isinstance(split, str):
        path_list.append(os.path.join(
            cache_dir, "yahoo_answers_csv", path_dict[split]))
    else:
        for s in split:
            path_list.append(os.path.join(
                cache_dir, "yahoo_answers_csv", path_dict[s]))
    for path in path_list:
        datasets_list.append(
            GeneratorDataset(
                source=Yahooanswers(path), column_names=column_names, shuffle=False
            )
        )
    if len(path_list) == 1:
        return datasets_list[0]
    return datasets_list