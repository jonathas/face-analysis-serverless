import boto3
import json

client = boto3.client('rekognition')
s3 = boto3.resource('s3')
bucketName = 'jon-images-test'


def detect_faces():
    detected_faces = client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPORARY',
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': '_analysis.png',
            },
        },
    )
    return detected_faces


def create_list_detected_faceId(detected_faces):
    detected_faceId = []
    for images in range(len(detected_faces['FaceRecords'])):
        detected_faceId.append(detected_faces['FaceRecords'][images]['Face']['FaceId'])
    return detected_faceId


detected_faces = detect_faces()
detected_faceId = create_list_detected_faceId(detected_faces)
print(detected_faceId)
