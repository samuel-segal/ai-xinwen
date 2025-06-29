import random
import time
import boto3
from boto3.dynamodb.conditions import Attr

from article_format import reformat_article
from student_word_db import get_student_words


def get_user_articles(user_id, limit=-1):
    dynamodb = boto3.resource('dynamodb')
    article_table = dynamodb.Table('translated_articles')

    #TODO This process is horrifically inefficient
    results = article_table.scan()
    items = results['Items']
    filtered_items = list(filter(
        lambda obj: obj['user_id'] == user_id,
        items
    ))
    filtered_items.sort(
        key = lambda obj: obj['translate_datetime']
    )
    if limit > 0:
        return filtered_items[-limit:]
    return filtered_items

def format_random_article(user_id):
    #Gets list of recent articles
    dynamodb = boto3.resource('dynamodb')
    article_table = dynamodb.Table('untranslated_articles')
    results = article_table.scan(Limit = 10)
    
    selected_article = random.choice(results['Items'])
    old_article_id = selected_article['article_id']
    chinese_text = selected_article['chinese_text']

    known_words = get_student_words(user_id)
    new_article_id = str(random.randbytes(20).hex())
    new_article = reformat_article(chinese_text, known_words)
    epoch_time = int(time.time())

    client = boto3.client('dynamodb')
    client.put_item(
        TableName = 'translated_articles',
        Item = {
            'article_id': {
                'S': new_article_id#Randomly generated
            },
            'text_chinese': {
                'S': new_article
            },
            'text_english': {
                'S': 'This is an article.'
            },
            'translate_datetime': {
                'N': str(epoch_time)
            },
            'old_article_id': {
                'S': old_article_id
            },
            'user_id': {
                'S': user_id
            }

        }
    )

#Returns list of ids
# def get_formatted_articles(user_id: str):
    # results = client.query(
    #     TableName='untranslated_articles',
    #     KeyConditionExpression='artist = :artist',
    #     ExpressionAttributeValues={
    #         ':artist': {'S': 'Arturus Ardvarkian'}
    #     }
    # )

if __name__ == '__main__':
    format_random_article('8428d428-b011-7068-d08a-5f614a3586c2')
    get_user_articles('8428d428-b011-7068-d08a-5f614a3586c2', 10)