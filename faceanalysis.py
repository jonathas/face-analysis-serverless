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


def create_list_detected_face_id(detected_faces):
    detected_face_id = []
    for images in range(len(detected_faces['FaceRecords'])):
        detected_face_id.append(detected_faces['FaceRecords'][images]['Face']['FaceId'])
    return detected_face_id


def compare_images(detected_face_ids):
    images_result = []
    for ids in detected_face_ids:
        images_result.append(
            client.search_faces(
                CollectionId='faces',
                FaceId=ids,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return images_result


def format_output(images_result):
    json_data = []
    for face_matches in images_result:
        if(len(face_matches.get('FaceMatches'))) >= 1:
            profile = dict(name=face_matches['FaceMatches'][0]['Face']['ExternalImageId'],
                           faceMatch=round(face_matches['FaceMatches'][0]['Similarity'], 2))
            json_data.append(profile)
    return json_data


detected = detect_faces()
face_id_list = create_list_detected_face_id(detected)
result = compare_images(face_id_list)
output = format_output(result)
print(json.dumps(output, indent=4))
