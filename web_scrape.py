import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#Uses AI :(
def scrape_article(url: str) -> str:
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=chrome_options)
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

if __name__ == '__main__':
    article_text = scrape_article('https://news.qq.com/rain/a/20250416A052DT00')
    print(article_text)
