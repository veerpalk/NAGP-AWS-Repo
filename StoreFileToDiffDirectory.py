import json
import boto3

s3 = boto3.client('s3')

def uploadFileToNewBucket(letters, spaces, words):
	bucket ='distination-bucket-name'
	fileSummaryToUpload = {}
	fileSummaryToUpload['LETTERS'] = letters
	fileSummaryToUpload['WORDS'] = words
	fileSummaryToUpload['SPACES'] = spaces

	fileName = 'fileSummaryOutput' + '.txt'

	uploadByteStream = bytes(json.dumps(fileSummaryToUpload).encode('UTF-8'))

	s3.put_object(Bucket=bucket, Key=fileName, Body=uploadByteStream)

	print('Put Complete')
