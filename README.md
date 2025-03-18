# Python Application with Docker and Terraform

This is a basic Python application that can be containerized using Docker and deployed to AWS using Terraform.

## Prerequisites

- Python 3.11+
- Docker
- Terraform
- AWS CLI configured with appropriate credentials

## Local Development

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application locally:
```bash
python app.py
```

## Docker Build and Run

1. Build the Docker image:
```bash
docker build -t python-app .
```

2. Run the container:
```bash
docker run -p 5000:5000 python-app
```

## Terraform Deployment

1. Initialize Terraform:
```bash
terraform init
```

2. Review the infrastructure plan:
```bash
terraform plan
```

3. Apply the infrastructure:
```bash
terraform apply
```

4. When finished, destroy the infrastructure:
```bash
terraform destroy
```

## Project Structure

- `app.py` - Main Python application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `main.tf` - Terraform infrastructure configuration
- `.gitignore` - Git ignore rules

## Notes

- The application runs on port 5000
- The Terraform configuration creates a VPC, public subnet, and ECR repository
- Remember to update the AWS region in `main.tf` if needed
- Make sure to configure AWS credentials before running Terraform commands
