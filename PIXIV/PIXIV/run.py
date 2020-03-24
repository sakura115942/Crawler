from scrapy.cmdline import execute


if __name__ == '__main__':
    user_id = '216403'
    command = f'scrapy crawl author -a user_id={user_id} -o pixiv.csv'
    execute(command.split(' '))
