# Create Service Account and Secret.
We aim to store the final results in ZIP format in a Google Cloud Bucket. To achieve this, you will need to create a Service Account for authentication. Below, you'll find step-by-step instructions on how to create a Service Account and add the credentials as a secret.
1. Open the IAM and Admin Page by clicking on the navigation menu (the three horizontal lines at the top left), then navigate to IAM & Admin > Service accounts.
2. Click the "Create Service Account" button and provide a name and optional description for the service account.
<img  src="/public/gke/service-account.1.png" alt="Service Account" style="width: 100vw">
<img  src="/public/gke/service-account.2.png" alt="Service Account" style="width: 100vw">
<img  src="/public/gke/service-account.3.png" alt="Service Account" style="width: 100vw">
<img  src="/public/gke/service-account.4.png" alt="Service Account" style="width: 100vw">

3. The next step is to generate and download the key. Locate the service account, then click on the "KEYS" tab at the top. Choose "ADD KEY" > "Create new key." Ensure that the key type remains as JSON, and click the "CREATE" button at the bottom. Once you've created the key, it will be automatically downloaded to your local computer.
<img  src="/public/gke/service-account-create-key.1.png" alt="Create Key" style="width: 100vw">

4. Encode the key as base64 by running the below command in your terminal.
```bash
    cat <key-file-name>.json | base64
```
<img  src="/public/gke/service-account-create-key.2.png" alt="Create Key" style="width: 100vw">

5. To generate the secret file, open your cloud editor and navigate to the 'cloud-surge' repository. Duplicate the 'secrets.yaml.example' file and rename it as 'secrets.yml.' Then, replace the value of 'sa_json' with the generated key in the previous step.
<img  src="/public/gke/create-secret.1.png" alt="Create Secret" style="width: 100vw">
6. And then create the file by running the below command in the gcloud terminal

```bash
kubectl apply -f ./secrets.yml
```
<img  src="/public/gke/create-secret.2.png" alt="Create Secret" style="width: 100vw">

:::info

Follow the link [here](https://developers.google.com/workspace/guides/create-credentials#service-account) for more reference.

:::
