# -*- coding: utf-8 -*-


"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help    显示帮助菜单
    -g           高铁
    -d           动车
    -t           特快
    -k           快速
    -z           直达

Example:
    tickets 北京 上海 2017-10-22
    tickets -dg 成都 南京 2017-10-22
"""

from docopt import docopt
from stations import stations
from prettytable import PrettyTable
import requests, colorama

colorama.init()

def cli():
    """ command-line interface"""
    arguments = docopt(__doc__)
    # print(arguments)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    options = ''.join([k for k, v in arguments.items() if
                       v is True])
    # print(from_station, to_station, date)
    # 构建URL
    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(
            date, from_station, to_station)
    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    r_json = r.json()['data']
    TrainCollection(r_json, options).pretty_print()

class TrainCollection:
    header = '车次 起始站 终点站 出发时间 到达时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split()
    
    def __init__(self, available_trains, options):
        """查询到的火车班次集合
        
        :param available_trains:一个列表，包含可获得的火车班次，每个火车班次是一个字典
        :param options:查询的选项，如高铁，动车，etc...
        """
        self.available_trains = available_trains
        self.options = options
    
    def _color_print(self, item, color):
        return color + item + colorama.Fore.RESET
    
    @property
    def train(self):
        for item in self.available_trains['result']:
            item = item.split('|')
            train_no = item[3]
            # 过滤为空或者是在过滤选项中
            if not self.options or train_no[0] in self.options:
                start_station = self.available_trains['map'].get(item[6])
                end_station = self.available_trains['map'].get(item[7])
                departure = item[8]
                arrival = item[9]
                duration = item[10]
                yd = item[-4]
                ed = item[-3]
                rw = item[23]
                yw = item[-7]
                yz = item[-6]
                wz = item[26]
                row = [train_no,
                       self._color_print(start_station, colorama.Fore.MAGENTA),
                       self._color_print(end_station, colorama.Fore.GREEN),
                       self._color_print(departure, colorama.Fore.MAGENTA),
                       self._color_print(arrival, colorama.Fore.GREEN),
                       duration, yd, ed, rw, yw, yz, wz]
                yield row
    
    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.train:
            pt.add_row(train)
        print(pt)
                
        
    
if __name__ == '__main__':
    cli()
    