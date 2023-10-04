# Access the Result.
The results produced by the surge process are stored in the Google Cloud Storage bucket that was created during the third step. To access and download these surge results, please follow the steps below:
1. Install `gsutil` by following the documentation [here](https://cloud.google.com/storage/docs/gsutil_install).
2. To access the bucket, click on "Cloud Storage" >> "Buckets." Choose the "surge-results" bucket and verify the existence of the created folder. Next, click the "DOWNLOAD" button at the top and execute the gsutil command locally to initiate the data download.

<img  src="/gke/access-result.1.png" alt="Access the result" style="width: 100vw">
<img  src="/gke/access-result.2.png" alt="Access the result" style="width: 100vw">
<img  src="/gke/access-result.3.png" alt="Access the result" style="width: 100vw">