## Modes of Operation

I have provided two options: one with an upload to an AWS S3 bucket and another one without.

1. **Without Cloud:**
   - Follow the steps to build and run the Docker image directly (see below).

2. **Using AWS:**
   - In this mode, you need to set up an AWS account and configure AWS credentials. Follow the steps to set up your AWS account and local environment, then build and run the Docker image (see details below).

## Option 1: Build and Run Immediately (no cloud)

### Step 1: Build the Docker Image

1. **Open a terminal:**
   - Navigate to the directory containing the `Dockerfile`.

2. **Build the Docker image:**
   - Run the following command to create a new Docker image named `taxi-duration`:
     ```
     docker build -t taxi-duration .
     ```

### Step 2: Run the Docker Container

1. **Run the Docker container:**
   - Use the following command to start a new container from the `taxi-duration` image:
     ```
     docker run taxi-duration
     ```

## Option 2: Using AWS

### Step 1: Set Up AWS and Local Environment

1. **Log in to your AWS account:**
   - Visit [AWS Management Console](https://aws.amazon.com/console/) and log in with your credentials.

2. **Create a new IAM user with S3 access:**
   - Navigate to the [IAM dashboard](https://console.aws.amazon.com/iam/).
   - Click on "Users" and then "Add user".
   - Enter a user name and select "Programmatic access".
   - Click "Next: Permissions".
   - Choose "Attach policies directly" and search for "AmazonS3FullAccess". Select it.
   - Complete the creation steps and make sure to download the `CSV` file containing the **Access Key ID** and **Secret Access Key**. Store these credentials securely.

3. **Create a new S3 bucket:**
   - Go to the [S3 dashboard](https://s3.console.aws.amazon.com/s3/).
   - Click on "Create bucket".
   - Enter a unique name for your bucket and select your preferred region.
   - Complete the bucket creation steps.

4. **Set up your local environment:**
   - Create a file named `.env` in your project directory.
   - Open the `.env` file and add the following lines, replacing `<value>` with your actual AWS credentials and bucket name:
     ```
     AWS_ACCESS_KEY_ID=<your_access_key_id>
     AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
     AWS_DEFAULT_REGION=<region_where_bucket_was_created>
     BUCKET_NAME=<your_bucket_name>
     ```

### Step 2: Build the Docker Image

1. **Open a terminal:**
   - Navigate to the directory containing the `Dockerfile`.

2. **Build the Docker image:**
   - Run the following command to create a new Docker image named `taxi-duration`:
     ```
     docker build -t taxi-duration .
     ```

### Step 3: Run the Docker Container

1. **Ensure you are in the project directory and the `.env` file is present:**
   - Confirm that the `.env` file is present in the current directory.

2. **Run the Docker container:**
   - Use the following command to start a new container from the `taxi-duration` image, passing the environment variables defined in the `.env` file:
     ```
     docker run --env-file .env taxi-duration
     ```