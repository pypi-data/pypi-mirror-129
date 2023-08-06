# redbrick-sagemaker

This package is an integration between RedBrick AI and AWS sagemaker to allow end-to-end Active Learning on computer vision datasets.

The objective of Active Learning is to label your data in order of information gain to your model. Following this strategy can drastically reduce the amount of data you have to label by only labeling those images that help your model improve.

This package will help you run a full end-to-end process where you will be able to iteratively label your dataset and train your model in true Active Learning fashion.

## Setup

Install the redbrick_sagemaker package:

```bash
pip install redbrick_sagemaker
```

Standard RedBrick AI set up:

```python
api_key="TODO"
org_id="TODO"
project_id="TOOD"

# The bucket where sagemaker will read/write predictions and training input/outputs.
s3_bucket_name="TODO"
s3_bucket_prefix="TODO"

# OPTIONAL: only required if you are not running redbrick_sagemaker in an AWS sagemaker notebook instance. If running outside, you have to create a IAM role with full sagemaker access.
role="TODO"
```

Create a RedBrick AI Active Learning object:

```python
import redbrick_sagemaker

active_learner = redbrick_sagemaker.ActiveLearner(
    api_key, org_id, project_id,
    s3_bucket=bucket, s3_bucket_prefix=bucket_prefix,
    url=url, iam_role=role
)
```

Begin an Active Learning cycle. Running this for the first time will start a hyperparameter optimization job to train your model.

```python
active_learner.run()
```

Check on the status of your hyperparameter job.

```python
active_learner.describe()
```

Once your hyperparameter job is complete, you can re-run to perform inference and update Active Learning priorities.

```python
active_learning.run()
```

If your hyperparameter job is still processing, but there is a model job that has completed, you can force run an inference.

```python
active_learning.run(force_run=True)
```

If you want to run training, and inference in one go synchronously, you can simply do:

```python
active_learning.run(wait=True)
```

Please see the flowchart below for an explanation of the different states and flows.

<figure>
    <img src="readme.png"/>
    <figcaption> RedBrick Sagemaker active learning flow. </figcaption>
</figure>
