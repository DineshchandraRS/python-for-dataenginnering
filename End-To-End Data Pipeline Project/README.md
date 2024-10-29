# Spotify End-ToEnd Data Engineering project

### Introduction 
In this project, we will build an ETL [Extract ,Transform, Load] Pipeline using Spotify API on AWS. The Pipeline will retrive the data from the Spotify API, transform it to a desired format, and load it into an AWS data store.

### Architecture

### About Dataset/API
This API contains information aboy music artist, albums and songs - [Spotify API](https://developer.spotify.com/documentation/)

### Services Used
1. **S3(Simple Storage Service):** Amazon S3(Simple Storage Service) is a highly scalable object storage service that can store and retrieve any amount of data from anywhere on the web. It is commonly used to store and distribute large media files, data backups, and static website files.

2. **AWS Lambda:** AWS Lambda is as serverless computing service that lets you run your code without managing servers. You can use Lambda to run code and to get response to events like changes in S3, DynamoDB, or other AWS services.

3. **Cloud Watch:** Amazon Cloudwatch is a monitoring service for AWS resources and the applications you run on them. YOu can use CloudWatch Trigger to track metrics,  collect and monitor log files, and set alarms.

4. **Glue Crawler:** AWS Glue Crawler is a fully managed service that automatically  crawls your data sources, identifies data fromats and infer schemas to create an AWS Data Catalog

5. **Data Catalog:** AWS Glue Data catlog is fully managed metadata repository that makes it easy to discover and manage data in AWS, You can use the Glue Data Catalog with other AWS services, such as Athena

6. **Amazon Athena:** Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. You can use Athena to analyze data in your Glue Data Catlog or in other S3 buckets.
