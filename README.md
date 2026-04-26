# A2 – Data Layer Setup (DynamoDB & S3)

This repository contains the **data layer implementation** for Assignment 2.

The goal of this part is to design and initialise the backend storage required for the web application using **AWS DynamoDB and S3**.

---

## Scope of This Part

This implementation includes:

- Creating DynamoDB tables
- Designing key schemas based on dataset analysis
- Loading song data into DynamoDB
- Creating an S3 bucket
- Downloading and uploading artist images to S3

---

## Project Structure

```
A2/
├── create/             # Scripts to create DynamoDB tables and S3 bucket
├── load/               # Scripts to load data into DynamoDB and S3
├── delete/             # Scripts to delete DynamoDB tables
├── data/               # Source dataset (JSON file)
├── test/               # Simple test script for local verification of data loading and query behaviour
├── requirements.txt 
├── .gitignore
├── 2026a2_songs.json   # Songs dataset
├── eda.ipynb           # Notebook file for exploratory anaylisis of the raw songs dataset
└── README.md
```

---

## Prerequisites

Before running the scripts, ensure you have:

- Python 3.x installed
- Access to AWS Learner Lab
- AWS CLI installed locally

---

## AWS Configuration (Learner Lab)

This project uses **AWS Learner Lab temporary credentials**.

1. Log in to AWS Learner Lab and start the lab session

2. Locate your temporary AWS credentials (Access Key, Secret Key, Session Token)

3. Open your credentials file locally (e.g., using the following command):
```bash
nano ~/.aws/credentials 
```
4. Update it with your Learner Lab credentials:
[default]
aws_access_key_id=YOUR_ACCESS_KEY
aws_secret_access_key=YOUR_SECRET_KEY
aws_session_token=YOUR_SESSION_TOKEN
5. Save and exit

---

## Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

## DynamoDB Tables

### 1. Login Table

- **Partition Key:** `email`
- Stores:
  - `email`
  - `user_name`
  - `password`

---

### 2. Music Table

- **Partition Key:** `artist`
- **Sort Key:** `title_album` (composite: `title#album`)

This design ensures:
- No data loss from duplicate song titles
- Efficient grouping by artist

Additional attributes:
- `title`
- `album`
- `year`
- `image_url`

Indexes :
- GSI/LSI to support different query patterns (e.g., by title, album, year)


---

## S3 Bucket

- Stores artist images
- Images are downloaded from the dataset (`img_url`)
- Uploaded to S3 for later use in the web application

---

## How to Run

### Step 1: Create Tables and Bucket

Run the scripts in the `create/` folder:

```bash
python create/create_music_table.py
python create/create_login_table.py
python create/create_subscription_table.py
python create/create_s3_bucket.py
```

---

### Step 2: Load Data

Run the scripts in the `load/` folder:

```bash
python load/load_music_data.py
python load/fillin_login_table.py
python load/upload_images_to_s3.py
```

This will:

- Insert song data into DynamoDB
- Insert login records
- Upload images to S3


### Cleanup Scripts

The `delete/` folder contains utility scripts to remove existing DynamoDB tables.

These scripts are useful when:
- resetting the environment
- updating schema design
- reloading data without conflicts

Example usage:

```bash
python delete/delete_login_table.py
python delete/delete_music_table.py
```

### Optional: Run Tests (Local Verification)

The `tests/` folder contains simple scripts for local verification of the datasets.

These can be used to:
- check that datasets load correctly  
- validate basic query behaviour  
- ensure schema consistency  

Example usage:

```bash
python tests/test_query.py
```

---
## Design Considerations

### Schema Design

The DynamoDB schema was carefully designed based on dataset analysis:

- Duplicate `(artist, title)` combinations exist
- A composite sort key (`title_album`) is used to prevent overwriting

---

### Query Support

The schema supports:

- Searching songs by artist
- Filtering by multiple attributes (title, year, album)
- Supporting AND-based query logic in the application layer

---

## Next Step

This data layer will be used in the next stage to build the **Flask web application**, including:

- Login and registration
- Query functionality
- Subscription management
- Displaying images from S3
