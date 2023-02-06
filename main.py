import argparse
from crawling import crawling_all


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', required=True, type=str, help="크롤링 키워드")
    parser.add_argument('--path', required=True, type=str, help="저장 디렉토리")

    config = parser.parse_args()
    return config


def main():
    config = argparser()
    crawling_all(config.keyword, config.path)


if __name__ == '__main__':
    main()
