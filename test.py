from article_format import get_unknown_words, reformat_article
from student_word_db import get_student_words, update_student_words
from web_scrape import get_frontpage_articles, scrape_article


get_frontpage_articles()

student_id = 'bgq9ar'
news_article = 'https://news.qq.com/rain/a/20250416A08VD800'

known_words = get_student_words(student_id)
article = scrape_article(news_article)
reformatted_article = reformat_article(article, known_words)

new_words = get_unknown_words(reformatted_article, known_words)
all_words = known_words + new_words

with open('output.txt', 'w') as file:
    print(reformatted_article, file = file)
    print(new_words, file = file)

update_student_words(student_id, all_words)