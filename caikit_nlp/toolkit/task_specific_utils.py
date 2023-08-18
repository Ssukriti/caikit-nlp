# Copyright The Caikit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# First Party
from caikit.core.toolkit import error_handler
import alog

# Local
from ..data_model import ClassificationTrainRecord, GenerationTrainRecord

log = alog.use_channel("TASK_UTILS")
error = error_handler.get(log)


def convert_to_generation_record(train_record):
    if isinstance(train_record, GenerationTrainRecord):
        return train_record
    if isinstance(train_record, ClassificationTrainRecord):
        text = train_record.text
        labels = labels = ",".join(str(label) for label in train_record.labels)
        return GenerationTrainRecord(input=text, output=labels)
    error(
        "<NLP12517812E>",
        TypeError(
            "Unsupported instance type. \
            Only instances of datamodels ClassificationTrainRecord \
            and GenerationTrainRecord are supported"
        ),
    )


def get_sorted_unique_class_labels(data_stream):
    """Get the list of sorted unique class labels from a data stream of ClassificationTrainRecord.

    Args:
        data_stream: DataStream[ClassificationTrainRecord]
            Data stream of ClassificationTrainRecord from which to extract unique class labels
    Returns:
        unique_labels
            Sorted list containing the unique set of classes discovered in the data stream
    """
    labels_data_stream = data_stream.map(lambda item: item.labels)
    unique_labels = set()
    for label_list in labels_data_stream:
        for label in label_list:
            unique_labels.add(label)

    return sorted(unique_labels)
