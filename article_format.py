import re
import boto3

def reformat_article(article_text: str, valid_words: list[str]) -> str:

    client = boto3.client('bedrock-runtime')
    model_id = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

    response = client.converse(
        modelId = model_id,
        messages = [
            {
                'role': 'user',
                'content': [
                    {
                        
                        'document': {
                            'name': 'word_list',
                            'format': 'txt',
                            'source':{
                                'bytes': '\n'.join(valid_words)
                            }
                        }
                    },
                    {'text': 'Using only words in "word_list.txt", please summarize the given article. Do not use words outside of the list.\n'+article_text}
                ]
            }
        ],
        inferenceConfig  = {'maxTokens': 4096, 'temperature': 0.3, 'topP': 0.9},
        system=[
            {
                'text': """Aim for a response of around 10 sentences.
    Do not include text outside of the written summary.
    Put spaces in between each Chinese word."""
            }
        ],

    )

    response_text = response['output']['message']['content'][0]['text']

    line_split = response_text.splitlines()
    if line_split[0].startswith('以下是'):
        return '\n'.join(line_split[1:])

    return response_text


def get_unknown_words(formatted_article_text: str, valid_words: list[str]) -> list[str]:
    article_words = re.split(r"[\s,.，、。\"'“”‘’]", formatted_article_text)
    return list(set(filter(
        lambda word: len(word) != 0 and not re.search(r'\d', word) and word not in valid_words,
        map(str.strip, article_words)
    )))

if __name__ == '__main__':
    with open('sample_data/HSK_1.txt', encoding='utf-8') as file:
        known_words = file.read().splitlines()
    with open('sample_data/sample_article.txt', encoding='utf-8') as file:
        article_text = file.read()
    
    reformatted_article = reformat_article(article_text, known_words)
    print(reformatted_article)
    new_words = get_unknown_words(reformatted_article, known_words)
    print(new_words)