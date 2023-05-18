from script.news import NewsScraper


def main():
    news = NewsScraper()
    news.connect_news()


if __name__ == '__main__':
    main()
