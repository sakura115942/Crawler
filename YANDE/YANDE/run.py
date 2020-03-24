from scrapy.cmdline import execute


if __name__ == '__main__':
    tags = 'takeuchi_takashi'
    command = f'scrapy crawl yande -a tags={tags}'
    execute(command.split(' '))
