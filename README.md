# 🚀 **ml-cloud-project**: Scale the Skies with AWS 🌐

Welcome to **ml-cloud-project**! This repository contains a powerful RESTful API designed to manage your files seamlessly in AWS S3. Whether you're building a cloud-native app or scaling your infrastructure, this API will help you upload, list, download, and delete files with ease. 🚀

This project follows **Twelve-Factor App** principles and leverages **FastAPI**, **Boto3**, and the power of AWS to provide a scalable and maintainable file management solution 🌍.

## ✨ **Key Features**
- 📤 **Upload Files:** Upload new files or update existing ones in your S3 bucket.
- 🗂️ **List Files:** Retrieve a paginated list of files in your S3 bucket.
- 📝 **Retrieve Metadata:** Get metadata for each file (size, last modified, etc.).
- 📥 **Download Files:** Stream files directly from S3 for easy access.
- ❌ **Delete Files:** Securely remove files from your S3 bucket.

## 📜 **Quick Start**

Install the project as a package:
```bash
pip install ml-cloud-project
```

## Then, import and use it like so:
```bash
from files_api import ...
```

## 🛠️ System Requirements
To develop and contribute to this project, ensure you have the following tools installed:

make (or cmake):

- For Windows/macOS: Install CMake from the official site.
- For Linux (using Homebrew or package managers):
```bash
brew install cmake
# or
sudo apt-get install cmake
```
- Python 3.7+ (ideally using pyenv to manage Python versions).
- git.

## 🏗️ Setting Up the Development Environment
- Clone the Repo
- Clone this repository to your local machine:

```bash
git clone https://github.com/<your github username>/ml-cloud-project.git
```

## Install Development Dependencies
- It’s recommended to use a virtual environment. To set up and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Set Up Environment Variables
- Create a .env file in the root of the project with your AWS credentials (for local testing with Moto):

```bash
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
S3_BUCKET_NAME=your-bucket-name
```
## Running the Application Locally
To run the app locally, you will use a script (run.sh) in conjunction with a Makefile.

Start the FastAPI app using Makefile commands:
```bash
make run
```
This command will trigger the script in run.sh, which will start the app via Uvicorn. The app will be accessible at http://127.0.0.1:8000.

Running Tests Locally
For testing, Moto is used to mock AWS services like S3, so you can test your application locally without hitting actual AWS.

Run the tests with:
```bash
make test
```
Running the run.sh Script Manually
If you want to directly execute the run.sh script, you can do so by running:

```bash
sh run.sh
```

## 📝 **API Endpoints**

### 📤 `PUT /files/{file_path:path}`
Upload a file to your S3 bucket (updates if the file already exists).

- **Request Body:**
  - `file`: The file to upload.
  
- **Response:**
  - `file_path`: The path of the uploaded file.
  - `message`: Status message (file uploaded or updated).

### 🗂️ `GET /files`
List files in your S3 bucket with pagination support.

- **Query Params:**
  - `page_size`: Number of files per page (default: 10).
  - `directory`: Filter by directory (optional).
  - `page_token`: Token for pagination (optional).
  
- **Response:**
  - `files`: List of file metadata (path, last modified, size).
  - `next_page_token`: Token for the next page (if available).

### 📝 `HEAD /files/{file_path:path}`
Retrieve metadata for a specific file.

- **Response:**
  - `Content-Type`: The file's content type.
  - `Content-Length`: The file's size.
  - `Last-Modified`: The file's last modified date.

### 📥 `GET /files/{file_path:path}`
Download a file from the S3 bucket.

- **Response:** Streams the file’s content.

### ❌ `DELETE /files/{file_path:path}`
Delete a file from the S3 bucket.

- **Response:** HTTP status `204 No Content` on success.

---

## 📈 **Scalability & Deployment**

This project is designed to scale 🚀 using the **Twelve-Factor App** methodology, making it perfect for cloud environments 🌐.

For deployment:
- **AWS**: Deploy to services like **AWS EC2**, **AWS Lambda**, or **Kubernetes**.
- **CI/CD**: Automate testing and deployment with **GitHub Actions**, **CircleCI**, or **Jenkins** 🔧.

## ⚙️ **DevOps Considerations**
- **Infrastructure as Code**: Use **Terraform** or **AWS CloudFormation** for easy infrastructure management 🔨.
- **Monitoring**: Set up **CloudWatch** for performance monitoring 📊.
- **Security**: Leverage **IAM roles** for secure access to AWS resources 🔐.
