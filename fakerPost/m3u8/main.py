# coding: utf-8
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from Extractor import *

if __name__ == '__main__':
    filePath = 'm3u8.txt'
    extractor = Extractor()
    links = extractor.extract(filePath)
    
    indexStart = 0
    # indexEnd = 1000
    links = links[indexStart:]
    completions = []
    with ThreadPoolExecutor(max_workers=16) as t:
        threads = []
        index = indexStart
        for link in links:
            name = 'ts/{}.ts'.format(index)
            thread = t.submit(extractor.download, link, name)
            threads.append(thread)
            index += 1

        for future in as_completed(threads):
            name = future.result()
            print(f"\n{name} completed.\n")
            completions.append(name)

    print(f'\nsize :{len(completions)} / {len(links)}\n')
    print(completions)
