# if __name__ == "__main__":
#     print("여기는 진짜 실행되면 안됨")
# 내가 직접 실행하면 main으로 바뀐다. 
# test에서 실행하면 name이 test가 되고 main은 aws가 되어서 
# 둘이 같지 않아서 실행안됨
# 크리티컬한 부분은 여기 쓰면됨.

import boto3 

def detect_labels_local_file(photo):


    client=boto3.client('rekognition')
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()}) 
    
    result = []

    for label in response["Labels"]:
        name = label["Name"]
        confidence = label["Confidence"]

        result.append(f"{name} : {confidence:.2f}%")
    
    r = "<br/>".join(map(str,result))
    # ["Dog : 22.23%", "Cat : 40.64%"]
    return r


def compare_faces(sourceFile, targetFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=0,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        similarity = faceMatch['Similarity']

    imageSource.close()
    imageTarget.close()
    return f"동일 인물인 확률은 {similarity:.2f}%입니다"
        

