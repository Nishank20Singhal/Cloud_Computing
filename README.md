# Cloud_Computing
# CND System

Horizontal Scaling for an Embarrassingly Parallel Task: Blockchain Proof-of-Work in the Cloud



## Deploy CND system


   ```
1. awscli connect using Assess key and password and the region name
2. Create any one instance on the amazon cloud manualy.
3. Install 'conda envirnment' `Boto3` and `paramiko`

   ```shell
   conda create -n cloud_computing python=3.6 anaconda
   pip install Boto3
   pip install paramiko
   pip install threaded
   ```

3. Run the following command:
  for Stage 1:
  ```shell
  python Local_BPOW.py
  ```
  stage 2
  ```shell
  python Run_single_instance_on_cloud.py
  ```
  stage 3
   ```shell
   python Cloud_BPOW.py
   ```