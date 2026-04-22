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
├── setup/        # Scripts to create DynamoDB tables and S3 bucket
├── load/         # Scripts to load data into DynamoDB and S3
├── data/         # Source dataset (JSON file)
├── .gitignore
└── README.md
```

---

##  Prerequisites

Before running the scripts, ensure you have:

- Python 3.x installed
- An AWS account
- AWS CLI installed and configured

To configure AWS locally:

```bash
aws configure
```

---

## Dependencies

Install required Python packages:

```bash
pip install boto3 requests
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

Run the scripts in the `setup/` folder:

```bash
python setup/create_music_table.py
python setup/create_login_table.py
python setup/create_subscription_table.py
python setup/create_s3_bucket.py
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
