import json
import boto3
import urllib.parse
from fileCounter import counter
from uploadFileInNewBucket import uploadFileToNewBucket

# boto3 S3 initialization
s3_client = boto3.client("s3")


def lambda_handler(event, context):
   destination_bucket_name = 'source-bucket-name'

   # event contains all information about uploaded object
   print("Event :", event)

   # Bucket Name where file was uploaded
   source_bucket_name = event['Records'][0]['s3']['bucket']['name']
   print("Source: ", source_bucket_name)
  
   # Filename of object (with path)
   file_key_name = event['Records'][0]['s3']['object']['key']
   print("File Key nm:", file_key_name)
   
   
   fileObj = s3_client.get_object(Bucket=source_bucket_name, Key=file_key_name)
   print("FileObject", fileObj)
   file_content = fileObj["Body"].read().decode('utf-8')
   print("FILE:.", file_content)
   
   number_of_spaces = file_content.count(" ")
   
   number_of_letters = len(file_content) - number_of_spaces
   
   # to count words in string 
   number_of_words = len(file_content.split()) 
   

   print("No of letters: ", number_of_letters)
   print("No of spaces: ", number_of_spaces)
   print("No of words: ", str(number_of_words))
   
   
   uploadFileToNewBucket(number_of_letters, number_of_spaces, str(number_of_words))
   
   # Copy Source Object
   copy_source_object = {'Bucket': source_bucket_name, 'Key': file_key_name}
   print("copy_source_object: ", copy_source_object)

   # S3 copy object operation
   s3_client.copy_object(CopySource=copy_source_object, Bucket=destination_bucket_name, Key=file_key_name)

   return {
       'statusCode': 200,
       'body': json.dumps('Hello from S3 events Lambda!')
   }
   