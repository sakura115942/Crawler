from scrapy.cmdline import execute


if __name__ == '__main__':
    command = 'scrapy crawl Top250 -o top250.csv'
    execute(command.split(' '))
