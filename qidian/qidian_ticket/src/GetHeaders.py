import yaml

class GetHeaders:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/mobile QDReaderAndroid',
            'Host': 'druidv6.if.qidian.com'
        }

    def load(self, type):
        with open(f'log/email{type}.yml', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = lines[1:]

        with open(f'log/headers{type}.yml', 'w', encoding='utf-8') as f:
            f.writelines(lines)

        with open(f'log/headers{type}.yml') as f:
            self.origin_data = yaml.safe_load(f)
            self.origin_data['borgus'] = str(self.origin_data['borgus'])
            self.origin_data['tstamp'] = str(self.origin_data['tstamp'])

        self.headers['borgus'] = self.origin_data['borgus']
        self.headers['tstamp'] = self.origin_data['tstamp']
        self.headers['Cookie'] = self.origin_data['Cookie']

        return self.origin_data