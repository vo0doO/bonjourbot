# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import json
from scrapy.exceptions import DropItem


class BonjourbotPipeline:
    def process_item(self, item, spider):
        return item


class DublicatesPipeLine:

    def __init__(self):
        self.hash_seen = set()

    def process_item(self, item, spider):
        if item['hash'] in self.hash_seen:
            raise DropItem(f"Обнаружен  дубликат ==> {item}")
        else:
            self.hash_seen.add(item["hash"])
            return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open(f"{spider.name}.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item, ensure_ascii=False,) + "\n"
        self.file.write(line)
        return item
