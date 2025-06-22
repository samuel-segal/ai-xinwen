import boto3

client = boto3.client(
    'dynamodb'
)


def get_student_words(user_id: str) -> str:
    student_info_request = client.get_item(
        TableName = 'student_info',
        Key = {
            'user_id': {
                'S': user_id
            }
        },
        ProjectionExpression = 'user_id, known_words'
    )

    student_info = student_info_request['Item']

    return student_info['known_words']['SS']

def initialize_student_words(user_id: str, resource_name: str) -> None:
    with open(resource_name, 'r', encoding='utf-8') as file:
        known_words = file.read().splitlines()
        update_student_words(user_id, known_words)

#Necessary for a clean reset, for larger it may be more efficient
#To simply add the values on
def update_student_words(user_id: str, known_words: list[str]) -> None:
    client.update_item(
        TableName = 'student_info',
        Key = {
            'user_id': {
                'S': user_id
            }
        },
        UpdateExpression = 'SET #KW = :w',
        ExpressionAttributeNames = {
            '#KW': 'known_words'
        },
        ExpressionAttributeValues = {
            ':w': {'SS': known_words}
        }
    )

def get_student_articles(user_id: str):
    student_info_request = client.get_item(
        TableName = 'student_info',
        Key = {
            'user_id': {
                'S': user_id
            }
        },
        ProjectionExpression = 'user_id, translated_articles'
    )

    student_info = student_info_request['Item']

    return list(map(
        lambda x: x['S'],
        student_info['translated_articles']['L']
    ))


if __name__ == '__main__':
    initialize_student_words('bgq9ar', 'sample_data/HSK_1.txt')
    words = get_student_words('bgq9ar')
    articles = get_student_articles('bgq9ar')

    print('Words',words)
    print('Articles',articles)