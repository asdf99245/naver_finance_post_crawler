import argparse
from crawling import crawling_all
import schedule
import time


def sample(a, b):
    print(a + b)


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', required=True, type=str, help="크롤링 키워드")
    parser.add_argument('--path', required=True, type=str, help="저장 디렉토리")
    parser.add_argument('--schedule', required=False, type=str, help="프로그램을 자동 실행할 스케줄링 시간")

    config = parser.parse_args()
    return config


def main():
    config = argparser()

    if config.schedule is None:
        crawling_all(config.keyword, config.path)
    else:
        schedule.every().day.at(config.schedule).do(crawling_all, config.keyword, config.path)
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    main()
