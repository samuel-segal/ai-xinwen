from random import randbytes
import re
from urllib.request import urlopen
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



#TODO Specific to QQ
def get_frontpage_articles() -> list[str]:
    url = 'https://www.qq.com/'
    with urlopen(url) as res:
        data = res.read().decode('utf-8')
        reg_find = re.findall(r'https://news.qq.com/rain/a/\w+', data)
        return list(
            set(reg_find)
        )

#Uses AI :(
def scrape_article(url: str) -> str:
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get(url)
    body = driver.find_element(By.XPATH, '/html/body')
    html_text = body.text

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
                            'name': 'article',
                            'format': 'txt',
                            'source':{
                                'bytes': html_text
                            }
                        }
                    },
                    {'text': 'The attached file contains HTML of a news article. Please parse out the news article. Only output the news article. Output the article completely in text. Output the article in its entirety.'}
                ]
            }
        ],
        inferenceConfig  = {'maxTokens': 2000, 'temperature': 0.1, 'topP': 0.9},
        system=[
            {
                'text': """Do not modify the original Chinese of the news article.
Only output the original Chinese of the article.
Output the entire article."""
            }
        ],
    )

    response_text = response['output']['message']['content'][0]['text']


    return response_text

def add_frontpage_to_existing():
    front_page_articles = get_frontpage_articles()
    client = boto3.client('dynamodb')
    for article_url in front_page_articles:
        print()
        print(article_url)
        article_id = str(randbytes(20).hex())
        article_text = scrape_article(article_url)
        print(article_text)
    
        client.put_item(
            TableName = 'untranslated_articles',
            Item = {
                'article_id': {'S': article_id},
                'chinese_text': {'S': article_text},
                'english_text': {'S': 'Translation unavailable'}, #TODO
                'topic': {'S': 'general'}, #TODO
                'url': {'S': article_url}
            }
        )


if __name__ == '__main__':
    add_frontpage_to_existing()