import asyncio
import aiohttp
import datetime
import requests
import json
import re
from urllib.parse import urljoin, urlparse
import time
import os
import random
from typing import List, Tuple, Dict, Set
import socket
import statistics

URL_FILE = "https://raw.githubusercontent.com/adminouyang/231006/refs/heads/main/py/Hotel/hotel_ip.txt"

CHANNEL_CATEGORIES = {
    "央视频道": [
        "CCTV1", "CCTV2", "CCTV3", "CCTV4", "CCTV4欧洲", "CCTV4美洲", "CCTV5", "CCTV5+", "CCTV6", "CCTV7",
        "CCTV8", "CCTV9", "CCTV10", "CCTV11", "CCTV12", "CCTV13", "CCTV14", "CCTV15", "CCTV16", "CCTV17",
        "兵器科技", "风云音乐", "风云足球", "风云剧场", "怀旧剧场", "第一剧场", "女性时尚", "世界地理", "央视台球", "高尔夫网球",
        "央视文化精品", "卫生健康", "电视指南", "老故事", "中学生", "发现之旅", "书法频道", "国学频道", "环球奇观"
    ],
    "卫视频道": [
        "湖南卫视", "浙江卫视", "江苏卫视", "东方卫视", "深圳卫视", "北京卫视", "广东卫视", "广西卫视", "东南卫视", "海南卫视",
        "河北卫视", "河南卫视", "湖北卫视", "江西卫视", "四川卫视", "重庆卫视", "贵州卫视", "云南卫视", "天津卫视", "安徽卫视",
        "山东卫视", "辽宁卫视", "黑龙江卫视", "吉林卫视", "内蒙古卫视", "宁夏卫视", "山西卫视", "陕西卫视", "甘肃卫视", "青海卫视",
        "新疆卫视", "西藏卫视", "三沙卫视", "兵团卫视", "延边卫视", "安多卫视", "康巴卫视", "农林卫视", "山东教育卫视",
        "中国教育1台", "中国教育2台", "中国教育3台", "中国教育4台", "早期教育"
    ],
    "数字频道": [
        "CHC动作电影", "CHC家庭影院", "CHC影迷电影", "淘电影", "淘精彩", "淘剧场", "淘4K", "淘娱乐", "淘BABY", "淘萌宠", "重温经典",
        "星空卫视", "CHANNEL[V]", "凤凰卫视中文台", "凤凰卫视资讯台", "凤凰卫视香港台", "凤凰卫视电影台", "求索纪录", "求索科学",
        "求索生活", "求索动物", "纪实人文", "金鹰纪实", "纪实科教", "睛彩青少", "睛彩竞技", "睛彩篮球", "睛彩广场舞", "魅力足球", "五星体育",
        "劲爆体育", "快乐垂钓", "茶频道", "先锋乒羽", "天元围棋", "汽摩", "梨园频道", "文物宝库", "武术世界",
        "乐游", "生活时尚", "都市剧场", "欢笑剧场", "游戏风云", "金色学堂", "动漫秀场", "新动漫", "卡酷少儿", "金鹰卡通", "优漫卡通", "哈哈炫动", "嘉佳卡通", 
        "中国交通", "中国天气", "海看大片", "经典电影", "精彩影视", "喜剧影院", "动作影院", "都市剧场", "精品剧场"
    ],
    "北京": [
    "北京卫视", "BRTV文艺", "BRTV纪实科教", "BRTV影视", "BRTV财经", "BRTV体育休闲", "BRTV生活", "BRTV新闻"
    ],
   "辽宁": [
        "辽宁卫视", "辽宁都市", "辽宁影视剧", "辽宁体育", "辽宁生活", "辽宁教育青少", "辽宁北方", "辽宁宜佳购物", "辽宁公共", "辽宁经济",
    ],
    "上海": [
    "上海新闻综合","BesTV", "BesTV4K纪录", "BesTV4K动画", "BesTV4K电影","BesTV体育", "BesTV直播1", "BesTV直播2", "BesTV直播3", "BesTV直播4", "BesTV直播5", "BesTV直播8", "BesTV直播9", "BesTV直播10","BesTV百视通"
    ],
    "山东": [
        "山东购物", "山东教育", "山东农科", "山东齐鲁", "山东少儿", "山东生活", "山东体育", "山东文旅", "山东新闻", "山东综艺",
    ],
    "山西": [
    "山西黄河", "山西经济与科技", "山西影视", "山西社会与法治", "山西文体生活", "山西卫视",
    "朔州-1", "朔州-2", "孝义电视台", "清徐", "古交电视台", "阳曲", "九屏测试",
    "太原1", "太原2", "太原3", "太原4", "太原5", "太原教育"
    ],
    "河北": [
    "河北卫视", "河北经济生活", "河北都市", "河北影视剧", "河北少儿科教", "河北公共", "河北农民",
    "CGTN国际", "睛彩河北", "石家庄新闻综合", "石家庄娱乐", "石家庄生活", "石家庄都市"
    ],
    "河南": [
    "河南卫视", "河南都市频道", "河南民生频道", "河南法治频道", "河南电视剧频道", "河南新闻频道", "河南欢腾购物", "河南公共频道", "河南乡村频道", "河南国际频道", "睛彩中原", "移动戏曲", "河南文物宝库", "河南梨园频道", "河南武术世界"
    ],
    "天津": [
    "天津卫视", "天津新闻", "天津文艺", "天津影视", "天津都市", "天津体育", "天津科教", "天津少儿", "天津购物", "天津IPTV", "天津购物自营",
    "天津文艺广播", "天津经济广播", "天津新闻广播", "天津生活广播", "天津交通广播", "天津相声广播", "天津小说广播", "天津滨海广播", "天津音乐广播", "天津农村广播"
    ],
    "安徽": [
    "安徽经济生活", "安徽影视频道", "安徽农业科教", "安徽国际频道", "安徽公共频道", "安徽综艺体育",
    "合肥新闻频道", "肥西新闻综合", "黄山新闻综合", "黄山文旅频道", "旌德新闻综合", "霍邱新闻综合",
    "六安综合频道", "六安社会生活", "淮北新闻综合", "淮北经济生活", "淮南新闻综合", "淮南民生频道",
    "滁州新闻综合", "滁州科教频道", "滁州公共频道", "蒙城新闻频道", "南陵新闻综合", "祁门综合频道",
    "湾沚综合频道", "繁昌新闻综合", "桐城综合频道", "太湖新闻综合", "池州新闻综合", "池州文教生活",
    "义安新闻综合", "阜阳新闻综合", "阜阳生活频道", "阜阳教育频道", "阜阳都市文艺", "泗县新闻频道",
    "临泉新闻频道", "阜南新闻综合", "亳州综合频道", "亳州农村频道", "徽州新闻频道", "蚌埠新闻综合",
    "蚌埠生活频道", "寿县新闻综合", "屯溪融媒频道", "芜湖新闻综合", "芜湖生活频道", "无为新闻频道",
    "马鞍山新闻综合", "马鞍山科教生活", "安庆新闻综合", "安庆经济生活", "潜山综合频道", "黄山区融媒",
    "歙县综合频道", "休宁新闻综合", "黟县新闻综合", "宣城综合频道", "宣城文旅生活", "广德新闻综合",
    "广德生活频道", "郎溪新闻频道", "宁国新闻综合", "铜陵新闻综合", "铜陵教育科技", "枞阳电视台",
    "霍山综合频道", "金寨综合频道", "濉溪新闻频道", "宿州新闻综合", "宿州公共频道", "宿州科教频道",
    "萧县新闻综合", "五河新闻综合", "固镇新闻综合", "界首综合频道", "利辛新闻综合", "涡阳新闻综合"
    ],
    "内蒙古": [
    "内蒙古卫视", "内蒙经济", "内蒙新闻", "内蒙文体娱乐", "内蒙农牧", "内蒙少儿", "内蒙蒙语","XHTV", "ELTV",
    "呼市都市", "呼市新闻", "呼市影视","包头经济", "包头生活", "包头新闻","乌海新闻", "乌海都市","乌盟经济", "乌盟新闻", "乌盟生活",
    "赤峰新闻", "赤峰经济", "赤峰影视","兴安新闻", "兴安文化", "兴安影视","通辽城市", "通辽新闻", "通辽蒙语","阿拉善新闻", "阿拉善经济",
    "呼伦贝尔新闻", "呼伦贝尔文游", "呼伦贝尔资讯","巴彦淖尔新闻", "巴彦淖尔经济", "巴彦淖尔影视","鄂尔多斯新闻", "鄂尔多斯生活", "鄂尔多斯经济", "鄂尔多斯蒙语","锡林郭勒1", "锡林郭勒2",
    "苏尼特左旗", "苏尼特右旗","乌拉特前旗", "乌拉特中旗", "乌拉特后旗","突泉", "磴口", "多伦", "杭后", "达茂", "库伦", "丰镇",
    "五原", "武川", "扎兰屯", "阿尔山", "阿巴嘎", "翁牛特","托克托", "满洲里", "额济纳", "西乌旗", "阿右旗", "正蓝旗",
    "东乌旗", "土左旗", "太仆寺旗", "准格尔旗", "科右中旗","正镶白旗", "扎赉特旗", "察右中旗", "喀喇沁县", "额尔古纳","和林格尔", "伊金霍洛旗", "克什克腾旗","4K", "内蒙古购物"
    ],
    "新疆": [
    "包头TV1", "包头TV2", "包头TV3","乌鲁木齐1","阿克苏1", "阿克苏2","阿拉尔","阿勒泰1","克孜勒苏柯尔克孜1", "克孜勒苏柯尔克孜2", "克孜勒苏柯尔克孜3",
    "伊犁哈萨克1", "伊犁哈萨克2", "伊犁哈萨克3", "伊犁哈萨克4","喀什1", "喀什2", "喀什3","巴音郭楞1", "巴音郭楞2", "巴音郭楞3", "巴音郭楞4",
    "昌吉市电视台","霍城1","呼图壁1","玛纳斯1","竹山1", "竹山2","奎屯1", "奎屯3","综合","哈密TV1", "哈密TV3","人物频道","精彩影视","党员远程教育","SSTV2"
  ],
    "宁夏": [
    "宁夏公共", "宁夏教育", "宁夏经济", "宁夏少儿", "宁夏卫视", "宁夏文旅"
    ],
    "甘肃": [
    "甘肃文化影视", "甘肃公共", "甘肃都市", "甘肃经济", "甘肃少儿"
    ],
    "云南": [
    "云南4K", "云南康旅", "云南少儿", "云南卫视", "云南影视", "云南娱乐"
    ],
    "浙江": [
    "浙江新闻", "浙江民生", "浙江科教影视", "浙江经济生活", "浙江钱江", "浙江少儿", "之江纪录", "浙江好易购",
    "杭州综合", "杭州明珠", "杭州生活", "杭州影视", "杭州青少体育", "杭州导视",
    "宁波1", "宁波2", "宁波3", "宁波4",
    "温州新闻", "衢州综合", "衢州公共", "绍兴新闻", "湖州新闻", "桐乡新闻", "嘉兴新闻", "YMG新闻频道", "临平新闻", "丽水新闻", "金华新闻", "经济生活"
    ],

    "陕西": [
    "安康综合", "白水", "宝鸡", "宝鸡1", "宝鸡2", "凤翔", "扶风", "佛坪", "富平", "韩城综合", "华阴", "华州综合", 
    "岚皋", "麟游", "留坝", "陇县", "略阳", "眉县新闻", "勉县综合", "南郑", "宁强", "蒲城综合", "千阳", "太白", "商洛", "潼关综合", 
    "渭南新闻", "铜川", "西安1", "西安2", "西安3", "西安4", "西安都市", "西安教育", "西安乐购", "西安商务", "西安丝路", "西安新闻", "西安影视", 
    "西部电影", "西乡融媒", "咸阳综合", "兴平融媒", "延安1", "杨凌", "洋县电视台", "榆林1", "榆林2", "圆点生活", "圆点影视", "悦美生活", 
    "陕西1套", "陕西2套", "陕西3套", "陕西4套", "陕西5套", "陕西6套", "陕西7套", "陕西8套", "陕西都市", "陕西公共", "陕西乐家购物", "陕西生活", "陕西新闻", "陕西体育", "陕西影视", 
    "农林卫视", "陕视融媒", "陕视直播", "生态环境", "丝路", "台球"
  ],
    "青海": [
    "青海卫视", "青海经视", "青海都市", "九画面", "海北", "果洛", "黄南", "青海油田", "矿区生活", "西宁生活服务", "西宁新闻综合"
    ],  
    "福建": [
    "东南卫视", "福建综合频道", "福建公共频道", "福建新闻频道", "福建电视剧频道", "福建经济频道", "福建文体频道", "福建少儿频道", "福建教育频道", "福建旅游频道", "海峡卫视", "三沙卫视", "厦门卫视"
    ],
    "江苏": [
    "江苏新闻", "江苏城市", "江苏综艺", "江苏体育休闲", "江苏影视", "江苏教育", "江苏国际",
    "江苏南京生活", "江苏南京教科", "江苏南京十八", "江苏南京新闻", "江苏南京影视", "江苏南京娱乐", "江苏南京信息", "江苏南京少儿","武术世界"
    ],
    "重庆": [
    "重庆社会与法", "重庆红岩文化", "重庆新农村", "重庆红叶", "重庆移动", "重庆新闻", "重庆影视剧", "重庆文体娱乐", "重庆少儿", "重庆汽摩"
    ],
    "湖南": [
    "都市剧场", "湖南都市", "湖南经视", "湖南爱晚", "湖南电影", "湖南电视剧", "湖南娱乐", "湖南教育", "湖南国际","长沙综合", "长沙政法", "长沙嘉丽购",
    "湘西文化旅游", "湘西综合","张家界综合", "张家界公共","衡阳综合", "衡阳文旅法治","郴州综合","芷江电视台","永州新闻综合","常德综合",
    "临武综合","桂东融媒","湖南九画面",

    ],
    "湖北": [
        "湖北公共新闻", "湖北经视频道", "湖北综合频道", "湖北垄上频道", "湖北影视频道", "湖北生活频道", "湖北教育频道", "武汉新闻综合", "武汉电视剧", "武汉科技生活",
        "武汉文体频道", "武汉教育频道", "阳新综合", "房县综合", "蔡甸综合","湖北卫视", "湖北经视", "湖北综合", "湖北垄上", "湖北公共", "湖北影视", "湖北教育", "湖北生活",
        "武汉新闻", "武汉电视剧", "武汉生活", "武汉经济", "武汉文体", "武汉外语", "武汉少儿"
    ],
    "贵州": [
    "贵阳-1", "贵阳-2", "贵阳-3","贵州-4", "贵州-5", "贵州-6", "贵州-7","六盘水-1", "六盘水-2","黔南-1", "黔南-2","黔西南综合频道", "黔西南公共频道",
    "黔西-1","黔东南综合频道","遵义综合频道", "遵义公共频道", "遵义都市频道","铜仁-1", "铜仁-2","毕节-1", "毕节-2","安顺新闻综合", "安顺公共频道",
    "瓮安电视台","思南综合频道","凯里TV","雷山综合频道","安多卫视"
    ],
    "广东": [
    "广东综艺", "广东珠江", "广东珠江超清", "广东影视4K"
    ],
    "广西": [
    "广西影视", "广西新闻", "广西移动", "广西综艺旅游", "广西都市", "广西视听","南宁影视娱乐", "南宁文旅生活", "南宁新闻综合", "南宁公共",
    "北海综合", "防城港综合", "桂林综合", "桂林公共", "桂林科教", "崇左综合","来宾综合", "柳州综合", "梧州综合", "河池综合", "玉林综合", "百色综合","钦州综合", "贵港综合", "贺州综合"
    ],
    "海南": [
    "海南公共频道", "海南少儿频道", "海南文旅频道", "海南新闻频道", "海南自贸频道", "海口1台", "海口2台", "海口3台"
    ],
    "广东频道": [
        "广东影视","广东珠江", "广东体育", "广东新闻", "广东公共", "梅州-1", "梅州-2", "惠州公共", "经济科教", "广东少儿", "岭南戏曲"
    ],
    "吉林频道": [
        "吉林生活","长影频道", "吉林都市", "吉林乡村", "吉林市公共", "吉林影视", "吉林新闻", "吉林舒兰综合频道"
    ],
    "山东频道": [
        "山东齐鲁", "山东影视", "山东公共", "山东体育", "山东综艺", "山东少儿", "济宁综合", "济宁公共", "梁山综合", "梁山影视"
    ],
    "新疆频道": [
        "新疆卫视-3","新疆卫视-5"
    ],
    "其它频道": [
    ],
}

CHANNEL_MAPPING = {
    "CCTV1": ["CCTV-1", "CCTV1-综合", "CCTV-1 综合", "CCTV-1综合", "CCTV1HD", "CCTV-1高清", "CCTV-1HD", "cctv-1HD", "CCTV1综合高清", "cctv1"],
    "CCTV2": ["CCTV-2", "CCTV2-财经", "CCTV-2 财经", "CCTV-2财经", "CCTV2HD", "CCTV-2高清", "CCTV-2HD", "cctv-2HD", "CCTV2财经高清", "cctv2"],
    "CCTV3": ["CCTV-3", "CCTV3-综艺", "CCTV-3 综艺", "CCTV-3综艺", "CCTV3HD", "CCTV-3高清", "CCTV-3HD", "cctv-3HD", "CCTV3综艺高清", "cctv3"],
    "CCTV4": ["CCTV-4", "CCTV4-国际", "CCTV-4 中文国际", "CCTV-4中文国际", "CCTV4HD", "cctv4HD", "CCTV-4HD", "CCTV4-中文国际", "CCTV4国际高清", "cctv4"],
    "CCTV4欧洲": ["CCTV-4欧洲", "CCTV-4欧洲", "CCTV4欧洲 HD", "CCTV-4 欧洲", "CCTV-4中文国际欧洲", "CCTV4中文欧洲", "CCTV4欧洲HD", "cctv4欧洲HD", "CCTV-4欧洲HD", "cctv-4欧洲HD"],
    "CCTV4美洲": ["CCTV-4美洲", "CCTV-4北美", "CCTV4美洲 HD", "CCTV-4 美洲", "CCTV-4中文国际美洲", "CCTV4中文美洲", "CCTV4美洲HD", "cctv4美洲HD", "CCTV-4美洲HD", "cctv-4美洲HD"],
    "CCTV5": ["CCTV-5", "CCTV5-体育", "CCTV-5 体育", "CCTV-5体育", "CCTV5HD", "CCTV-5高清", "CCTV-5HD", "CCTV5体育", "CCTV5体育高清", "cctv5"],
    "CCTV5+": ["CCTV-5+", "CCTV5+体育赛事", "CCTV-5+ 体育赛事", "CCTV5+体育赛事", "CCTV5+HD", "CCTV-5+高清", "CCTV-5+HD", "cctv-5+HD", "CCTV5plas", "CCTV5+体育赛视高清", "cctv5+"],
    "CCTV6": ["CCTV-6", "CCTV6-电影", "CCTV-6 电影", "CCTV-6电影", "CCTV6HD", "CCTV-6高清", "CCTV-6HD", "cctv-6HD", "CCTV6电影高清", "cctv6"],
    "CCTV7": ["CCTV-7", "CCTV7-军农", "CCTV-7 国防军事", "CCTV-7国防军事", "CCTV7HD", "CCTV-7高清", "CCTV-7HD", "CCTV7-国防军事", "CCTV7军事高清", "cctv7"],
    "CCTV8": ["CCTV-8", "CCTV8-电视剧", "CCTV-8 电视剧", "CCTV-8电视剧", "CCTV8HD", "CCTV-8高清", "CCTV-8HD", "cctv-8HD", "CCTV8电视剧高清", "cctv8"],
    "CCTV9": ["CCTV-9", "CCTV9-纪录", "CCTV-9 纪录", "CCTV-9纪录", "CCTV9HD", "cctv9HD", "CCTV-9高清", "cctv-9HD", "CCTV9记录高清", "cctv9"],
    "CCTV10": ["CCTV-10", "CCTV10-科教", "CCTV-10 科教", "CCTV-10科教", "CCTV10HD", "CCTV-10高清", "CCTV-10HD", "CCTV-10高清", "CCTV10科教高清", "cctv10"],
    "CCTV11": ["CCTV-11", "CCTV11-戏曲", "CCTV-11 戏曲", "CCTV-11戏曲", "CCTV11HD", "cctv11HD", "CCTV-11HD", "cctv-11HD", "CCTV11戏曲高清", "cctv11"],
    "CCTV12": ["CCTV-12", "CCTV12-社会与法", "CCTV-12 社会与法", "CCTV-12社会与法", "CCTV12HD", "CCTV-12高清", "CCTV-12HD", "cctv-12HD", "CCTV12社会与法高清", "cctv12"],
    "CCTV13": ["CCTV-13", "CCTV13-新闻", "CCTV-13 新闻", "CCTV-13新闻", "CCTV13HD", "cctv13HD", "CCTV-13HD", "cctv-13HD", "CCTV13新闻高清", "cctv13"],
    "CCTV14": ["CCTV-14", "CCTV14-少儿", "CCTV-14 少儿", "CCTV-14少儿", "CCTV14HD", "CCTV-14高清", "CCTV-14HD", "CCTV少儿", "CCTV14少儿高清", "cctv14"],
    "CCTV15": ["CCTV-15", "CCTV15-音乐", "CCTV-15 音乐", "CCTV-15音乐", "CCTV15HD", "cctv15HD", "CCTV-15HD", "cctv-15HD", "CCTV15音乐高清", "cctv15"],
    "CCTV16": ["CCTV-16", "CCTV-16 HD", "CCTV-16 4K", "CCTV-16奥林匹克", "CCTV16HD", "cctv16HD", "CCTV-16HD", "cctv-16HD", "CCTV16奥林匹克高清", "cctv16"],
    "CCTV17": ["CCTV-17", "CCTV17高清", "CCTV17 HD", "CCTV-17农业农村", "CCTV17HD", "cctv17HD", "CCTV-17HD", "cctv-17HD", "CCTV17农业农村高清", "cctv17"],
    "兵器科技": ["CCTV-兵器科技", "CCTV兵器科技", "CCTV兵器高清"],
    "风云音乐": ["CCTV-风云音乐", "CCTV风云音乐"],
    "第一剧场": ["CCTV-第一剧场", "CCTV第一剧场"],
    "风云足球": ["CCTV-风云足球", "CCTV风云足球"],
    "风云剧场": ["CCTV-风云剧场", "CCTV风云剧场"],
    "怀旧剧场": ["CCTV-怀旧剧场", "CCTV怀旧剧场"],
    "女性时尚": ["CCTV-女性时尚", "CCTV女性时尚"],
    "世界地理": ["CCTV-世界地理", "CCTV世界地理"],
    "央视台球": ["CCTV-央视台球", "CCTV央视台球"],
    "高尔夫网球": ["CCTV-高尔夫网球", "CCTV高尔夫网球", "CCTV央视高网", "CCTV-高尔夫·网球", "央视高网"],
    "央视文化精品": ["CCTV-央视文化精品", "CCTV央视文化精品", "CCTV文化精品", "CCTV-文化精品", "文化精品", "央视文化"],
    "卫生健康": ["CCTV-卫生健康", "CCTV卫生健康"],
    "电视指南": ["CCTV-电视指南", "CCTV电视指南"],
    "东南卫视": ["福建东南"],
    "东方卫视": ["上海卫视"],
    "农林卫视": ["陕西农林卫视"],
    "内蒙古卫视": ["内蒙古", "内蒙卫视"],
    "康巴卫视": ["四川康巴卫视"],
    "山东教育卫视": ["山东教育"],
    "CETV1": ["中国教育1台", "中国教育一台", "中国教育1", "CETV", "CETV-1", "中国教育", "中国教育高清"],
    "CETV2": ["中国教育2台", "中国教育二台", "中国教育2", "CETV-2 空中课堂", "CETV-2"],
    "CETV3": ["中国教育3台", "中国教育三台", "中国教育3", "CETV-3 教育服务", "CETV-3", "早期教育"],
    "CETV4": ["中国教育4台", "中国教育四台", "中国教育4", "中国教育电视台第四频道", "CETV-4"],
    "CHC动作电影": ["CHC动作电影高清", "动作电影"],
    "CHC家庭影院": ["CHC家庭电影高清", "家庭影院"],
    "CHC影迷电影": ["CHC高清电影", "高清电影", "影迷电影", "chc高清电影"],
    "淘电影": ["IPTV淘电影", "北京IPTV淘电影", "北京淘电影"],
    "淘精彩": ["IPTV淘精彩", "北京IPTV淘精彩", "北京淘精彩"],
    "淘剧场": ["IPTV淘剧场", "北京IPTV淘剧场", "北京淘剧场"],
    "淘4K": ["IPTV淘4K", "北京IPTV4K超清", "北京淘4K", "淘4K", "淘 4K"],
    "淘娱乐": ["IPTV淘娱乐", "北京IPTV淘娱乐", "北京淘娱乐"],
    "淘BABY": ["IPTV淘BABY", "北京IPTV淘BABY", "北京淘BABY", "IPTV淘baby", "北京IPTV淘baby", "北京淘baby"],
    "淘萌宠": ["IPTV淘萌宠", "北京IPTV萌宠TV", "北京淘萌宠"],
    "吉林都市": ["吉视都市"],
    "吉林乡村": ["吉视乡村"],
    "吉林公共": ["吉林市公共"],
    "吉林影视": ["吉视影视"],
    "吉林生活": ["吉视生活"],
    "吉林舒兰综合频道": ["舒兰"],
    "魅力足球": ["上海魅力足球"],
    "睛彩青少": ["睛彩羽毛球"],
    "求索纪录": ["求索记录", "求索纪录4K", "求索记录4K", "求索纪录 4K", "求索记录 4K"],
    "金鹰纪实": ["湖南金鹰纪实", "金鹰记实"],
    "纪实科教": ["北京纪实科教", "BRTV纪实科教", "北京纪实卫视高清"],
    "星空卫视": ["星空衛視", "星空卫視"],
    "CHANNEL[V]": ["Channel [V]", "Channel[V]"],
    "凤凰卫视中文台": ["凤凰中文", "凤凰中文台", "凤凰卫视中文", "凤凰卫视"],
    "凤凰卫视香港台": ["凤凰香港台", "凤凰卫视香港", "凤凰香港"],
    "凤凰卫视资讯台": ["凤凰资讯", "凤凰资讯台", "凤凰咨询", "凤凰咨询台", "凤凰卫视咨询台", "凤凰卫视资讯", "凤凰卫视咨询"],
    "凤凰卫视电影台": ["凤凰电影", "凤凰电影台", "凤凰卫视电影", "鳳凰衛視電影台", " 凤凰电影"],
    "茶频道": ["湖南茶频道"],
    "快乐垂钓": ["湖南快乐垂钓"],
    "先锋乒羽": ["湖南先锋乒羽"],
    "天元围棋": ["天元围棋频道"],
    "汽摩": ["重庆汽摩", "汽摩频道", "重庆汽摩频道"],
    "梨园频道": ["河南梨园频道", "梨园", "河南梨园"],
    "文物宝库": ["河南文物宝库"],
    "武术世界": ["河南武术世界"],
    "乐游": ["乐游频道", "上海乐游频道", "乐游纪实", "SiTV乐游频道", "SiTV 乐游频道"],
    "欢笑剧场": ["上海欢笑剧场4K", "欢笑剧场 4K", "欢笑剧场4K", "上海欢笑剧场"],
    "生活时尚": ["生活时尚4K", "SiTV生活时尚", "上海生活时尚"],
    "都市剧场": ["都市剧场4K", "SiTV都市剧场", "上海都市剧场"],
    "游戏风云": ["游戏风云4K", "SiTV游戏风云", "上海游戏风云"],
    "金色学堂": ["金色学堂4K", "SiTV金色学堂", "上海金色学堂"],
    "动漫秀场": ["动漫秀场4K", "SiTV动漫秀场", "上海动漫秀场"],
    "卡酷少儿": ["北京KAKU少儿", "BRTV卡酷少儿", "北京卡酷少儿", "卡酷动画", "北京卡通", "北京少儿"],
    "哈哈炫动": ["炫动卡通", "上海哈哈炫动"],
    "优漫卡通": ["江苏优漫卡通", "优漫漫画"],
    "金鹰卡通": ["湖南金鹰卡通"],
    "嘉佳卡通": ["佳佳卡通"],
    "中国交通": ["中国交通频道"],
    "中国天气": ["中国天气频道"],
    "经典电影": ["IPTV经典电影"],
}

RESULTS_PER_CHANNEL = 20
SPEED_THRESHOLD = 200  # KB/s
TEST_DOWNLOAD_SIZE = 51200  # 50KB for speed test
TEST_TIMEOUT = 8  # 单个测速任务超时时间
SPEED_TEST_CONCURRENCY = 8  # 测速并发数

def load_urls():
    """从 GitHub 下载 IPTV IP 段列表"""
    try:
        resp = requests.get(URL_FILE, timeout=5)
        resp.raise_for_status()
        urls = [line.strip() for line in resp.text.splitlines() if line.strip()]
        print(f"📡 已加载 {len(urls)} 个基础 URL")
        return urls
    except Exception as e:
        print(f"❌ 下载 {URL_FILE} 失败: {e}")
        exit()

async def generate_urls(url):
    """生成待扫描的URL列表"""
    modified_urls = []

    ip_start = url.find("//") + 2
    ip_end = url.find(":", ip_start)

    base = url[:ip_start]
    ip_prefix = url[ip_start:ip_end].rsplit('.', 1)[0]
    port = url[ip_end:]

    json_paths = [
        "/iptv/live/1000.json?key=txiptv",
        "/iptv/live/1001.json?key=txiptv",
        "/iptv/live/2000.json?key=txiptv",
        "/iptv/live/2001.json?key=txiptv"
    ]

    for i in range(1, 256):
        ip = f"{base}{ip_prefix}.{i}{port}"
        for path in json_paths:
            modified_urls.append(f"{ip}{path}")

    return modified_urls

async def fetch_json(session, url, semaphore):
    """获取JSON数据并解析频道信息"""
    async with semaphore:
        try:
            async with session.get(url, timeout=3) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                results = []
                for item in data.get('data', []):
                    name = item.get('name')
                    urlx = item.get('url')
                    if not name or not urlx or ',' in urlx:
                        continue

                    if not urlx.startswith("http"):
                        urlx = urljoin(url, urlx)

                    for std_name, aliases in CHANNEL_MAPPING.items():
                        if name in aliases:
                            name = std_name
                            break

                    results.append((name, urlx))
                return results
        except Exception as e:
            return []

async def check_url(session, url, semaphore):
    """检查URL是否可用"""
    async with semaphore:
        try:
            async with session.get(url, timeout=3) as resp:
                if resp.status == 200:
                    return url
        except:
            return None

async def test_stream_speed_accurate(session, url, semaphore, test_id=0):
    """准确的速度测试函数，使用分段下载计算平均速度"""
    async with semaphore:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Range': f'bytes=0-{TEST_DOWNLOAD_SIZE-1}'
            }
            
            start_time = time.time()
            total_downloaded = 0
            
            try:
                async with session.get(url, headers=headers, timeout=TEST_TIMEOUT) as resp:
                    if resp.status not in (200, 206):
                        print(f"  ❌ 测速{test_id}: 状态码 {resp.status}")
                        return 0
                    
                    # 分段下载，每段记录时间
                    chunk_size = 8192
                    download_times = []
                    chunk_start = time.time()
                    
                    while total_downloaded < TEST_DOWNLOAD_SIZE:
                        try:
                            # 设置读取超时
                            chunk = await asyncio.wait_for(
                                resp.content.read(chunk_size),
                                timeout=2.0
                            )
                            if not chunk:
                                break
                            
                            chunk_size_actual = len(chunk)
                            total_downloaded += chunk_size_actual
                            
                            chunk_end = time.time()
                            chunk_time = chunk_end - chunk_start
                            download_times.append((chunk_size_actual, chunk_time))
                            chunk_start = chunk_end
                            
                        except asyncio.TimeoutError:
                            break
                        except Exception as e:
                            break
                    
                    end_time = time.time()
                    total_time = end_time - start_time
                    
                    if total_time <= 0 or total_downloaded == 0:
                        print(f"  ⚠️ 测速{test_id}: 下载失败或时间为0")
                        return 0
                    
                    # 计算平均速度 (KB/s)
                    speed_kbs = (total_downloaded / 1024) / total_time
                    
                    # 计算最后一段的速度（更准确）
                    if len(download_times) >= 2:
                        # 取最后3个块的平均速度
                        last_chunks = download_times[-3:] if len(download_times) >= 3 else download_times
                        last_speeds = []
                        for size, t in last_chunks:
                            if t > 0:
                                last_speeds.append((size / 1024) / t)
                        if last_speeds:
                            # 使用最后几段的平均速度，更稳定
                            speed_kbs = sum(last_speeds) / len(last_speeds)
                    
                    # 打印详细的测速结果
                    speed_status = "✅" if speed_kbs >= SPEED_THRESHOLD else "❌"
                    ip_port = extract_ip_port(url) or "Unknown"
                    print(f"  {speed_status} 测速{test_id}: {speed_kbs:7.2f} KB/s | 大小: {total_downloaded/1024:.1f}KB | 时间: {total_time:.2f}s | {ip_port}")
                    
                    return speed_kbs
                    
            except asyncio.TimeoutError:
                print(f"  ⏱️ 测速{test_id}: 超时")
                return 0
            except Exception as e:
                print(f"  ❌ 测速{test_id}: 错误 {str(e)[:30]}")
                return 0
                
        except Exception as e:
            print(f"  ❌ 测速{test_id}: 异常 {str(e)[:30]}")
            return 0

def extract_ip_port(url):
    """从URL中提取IP和端口"""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        
        if not hostname:
            return None
            
        # 解析端口
        if parsed.port:
            port = parsed.port
        elif parsed.scheme == 'https':
            port = 443
        else:
            port = 80
            
        return f"{hostname}:{port}"
    except:
        return None

def is_valid_stream(url):
    """检查是否为有效流"""
    if url.startswith("rtp://") or url.startswith("udp://") or url.startswith("rtsp://"):
        return False
    if "239." in url:
        return False
    if url.startswith("http://16.") or url.startswith("http://10.") or url.startswith("http://192.168."):
        return False
    
    # 检查是否包含流媒体扩展名
    valid_ext = (".m3u8", ".ts", ".flv", ".mp4", ".mkv")
    if any(ext in url.lower() for ext in valid_ext):
        return True
        
    # 或者检查是否包含流媒体路径关键字
    stream_keywords = ("/live/", "/stream/", "/hls/", "/live-stream/", "m3u8", "ts")
    if any(keyword in url.lower() for keyword in stream_keywords):
        return True
        
    return False

async def main():
    print("🚀 开始运行 hotel 脚本 - 优化测速版")
    
    # 加载基础URL
    urls = load_urls()
    
    # 创建会话
    async with aiohttp.ClientSession() as session:
        # 设置信号量控制并发
        scan_semaphore = asyncio.Semaphore(150)
        speed_semaphore = asyncio.Semaphore(SPEED_TEST_CONCURRENCY)
        
        # 生成所有待扫描URL
        all_urls = []
        for url in urls:
            modified_urls = await generate_urls(url)
            all_urls.extend(modified_urls)
        
        print(f"🔍 生成待扫描 URL 共: {len(all_urls)} 个")
        
        # 检测可用JSON API
        print("⏳ 开始检测可用 JSON API...")
        tasks = [check_url(session, u, scan_semaphore) for u in all_urls]
        valid_urls = [r for r in await asyncio.gather(*tasks) if r]
        
        print(f"✅ 可用 JSON 地址: {len(valid_urls)} 个")
        
        # 抓取节目单JSON
        print("📥 开始抓取节目单 JSON...")
        tasks = [fetch_json(session, u, scan_semaphore) for u in valid_urls]
        fetched = await asyncio.gather(*tasks)
        
        # 合并结果
        all_results = []
        for sublist in fetched:
            all_results.extend(sublist)
        
        print(f"📺 抓到原始频道总数: {len(all_results)} 条")
        
        # 去重
        unique_results = []
        seen_channels_urls = set()
        for name, url in all_results:
            key = f"{name}::{url}"
            if key not in seen_channels_urls:
                seen_channels_urls.add(key)
                unique_results.append((name, url))
        
        print(f"🔍 去重后频道总数: {len(unique_results)} 条")
        
        # 过滤无效流
        valid_results = []
        for name, url in unique_results:
            if is_valid_stream(url):
                valid_results.append((name, url))
        
        print(f"✅ 有效流总数: {len(valid_results)} 条")
        
        # 按频道分组
        channel_groups = {}
        for name, url in valid_results:
            if name not in channel_groups:
                channel_groups[name] = []
            channel_groups[name].append(url)
        
        print(f"📊 频道分组数: {len(channel_groups)} 个")
        
        # 特别处理CCTV1 - 测速
        cctv1_urls = channel_groups.get("CCTV1", [])
        cctv1_with_speed = []
        qualified_ips = set()
        
        if cctv1_urls:
            print(f"\n🚀 开始对 CCTV1 进行测速，共 {len(cctv1_urls)} 个源")
            print("=" * 80)
            print("测速结果 (≥200KB/s为合格):")
            print("-" * 80)
            
            # 对CCTV1的所有源进行测速
            speed_tasks = []
            for i, url in enumerate(cctv1_urls[:100]):  # 限制最多测速100个，避免太多
                task = test_stream_speed_accurate(session, url, speed_semaphore, i+1)
                speed_tasks.append(task)
            
            speeds = await asyncio.gather(*speed_tasks)
            
            # 组合URL和速度
            for i, (url, speed) in enumerate(zip(cctv1_urls[:100], speeds)):
                if speed > 0:  # 只保留测速成功的
                    cctv1_with_speed.append((url, speed))
                    
                    # 检查是否合格
                    if speed >= SPEED_THRESHOLD:
                        ip_port = extract_ip_port(url)
                        if ip_port:
                            qualified_ips.add(ip_port)
            
            # 按速度降序排序
            cctv1_with_speed.sort(key=lambda x: x[1], reverse=True)
            
            print("-" * 80)
            print(f"📈 CCTV1 测速完成统计:")
            print(f"   总测试数: {len(cctv1_urls[:100])}")
            print(f"   有效源数: {len(cctv1_with_speed)}")
            print(f"   合格源数(≥{SPEED_THRESHOLD}KB/s): {len(qualified_ips)}")
            
            if cctv1_with_speed:
                print(f"\n🏆 速度排名前10:")
                for i, (url, speed) in enumerate(cctv1_with_speed[:10], 1):
                    ip_port = extract_ip_port(url) or "N/A"
                    print(f"  {i:2}. {speed:7.2f} KB/s - {ip_port}")
        
        # 将合格的IP保存到文件
        if qualified_ips:
            with open("py/Hotel/已检测ip.txt", 'w', encoding='utf-8') as f:
                f.write(f"# CCTV1 测速合格IP列表 (≥{SPEED_THRESHOLD}KB/s)\n")
                f.write(f"# 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 合格IP数量: {len(qualified_ips)}\n")
                f.write("#" * 50 + "\n")
                for ip_port in sorted(qualified_ips):
                    f.write(f"{ip_port}\n")
            print(f"\n💾 已保存 {len(qualified_ips)} 个测速合格的IP到 py/Hotel/已检测ip.txt")
        else:
            print(f"\n⚠️ 没有找到速度大于{SPEED_THRESHOLD}KB/s的CCTV1源")
            # 创建空文件
            with open("py/Hotel/已检测ip.txt", 'w', encoding='utf-8') as f:
                f.write(f"# 没有找到速度大于{SPEED_THRESHOLD}KB/s的CCTV1源\n")
                f.write(f"# 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 构建最终结果
        final_results = []
        
        # 添加CCTV1（使用测速结果，最多取RESULTS_PER_CHANNEL个）
        for url, speed in cctv1_with_speed[:RESULTS_PER_CHANNEL]:
            final_results.append(("CCTV1", url, speed))
        
        # 添加其他频道（每个频道取前3个URL，速度标记为0）
        for name, urls in channel_groups.items():
            if name == "CCTV1":
                continue  # CCTV1已处理
            
            # 每个非CCTV1频道最多取3个URL
            for url in urls[:3]:
                final_results.append((name, url, 0))
        
        print(f"\n🎯 最终频道列表: {len(final_results)} 条")
        
        # 分类整理
        itv_dict = {cat: [] for cat in CHANNEL_CATEGORIES}
        categorized_channels = set()
        
        # 首先处理已定义的频道
        for name, url, speed in final_results:
            categorized = False
            for cat, channels in CHANNEL_CATEGORIES.items():
                if name in channels:
                    itv_dict[cat].append((name, url, speed))
                    categorized_channels.add(name)
                    categorized = True
                    break
        
        # 然后将未分类的频道放入"其它频道"
        for name, url, speed in final_results:
            if name not in categorized_channels:
                itv_dict["其它频道"].append((name, url, speed))
        
        # 打印分类统计
        print("\n📦 分类统计:")
        for cat in CHANNEL_CATEGORIES:
            print(f"  {cat}: {len(itv_dict[cat])} 条")
        
        # 生成最终文件
        beijing_now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8))
        ).strftime("%Y-%m-%d %H:%M:%S")
        
        with open("py/Hotel/hotel.txt", 'w', encoding='utf-8') as f:
            f.write("更新时间,#genre#\n")
            f.write(f"{beijing_now},#\n\n")
            
            for cat in CHANNEL_CATEGORIES:
                f.write(f"{cat},#genre#\n")
                
                if cat == "其它频道":
                    # 对"其它频道"按照频道名称排序
                    channels_in_category = {}
                    for name, url, speed in itv_dict[cat]:
                        if name not in channels_in_category:
                            channels_in_category[name] = []
                        channels_in_category[name].append((name, url, speed))
                    
                    # 对频道名称排序
                    sorted_channel_names = sorted(channels_in_category.keys())
                    
                    for channel_name in sorted_channel_names:
                        ch_items = channels_in_category[channel_name]
                        ch_items = ch_items[:RESULTS_PER_CHANNEL]
                        
                        for item in ch_items:
                            f.write(f"{item[0]},{item[1]}\n")
                else:
                    # 原逻辑：只写入在CHANNEL_CATEGORIES[cat]中定义的频道
                    for ch in CHANNEL_CATEGORIES[cat]:
                        ch_items = [x for x in itv_dict[cat] if x[0] == ch]
                        ch_items = ch_items[:RESULTS_PER_CHANNEL]
                        
                        for item in ch_items:
                            f.write(f"{item[0]},{item[1]}\n")
        
        print("\n🎉 hotel.txt 已生成完成！")
        
        # 打印未分类的频道信息
        other_channels = sorted(set([name for name, _, _ in itv_dict["其它频道"]]))
        if other_channels:
            print(f"\n📊 未分类频道 ({len(other_channels)} 个):")
            for i, channel in enumerate(other_channels[:20], 1):
                print(f"  {i:3}. {channel}")
            if len(other_channels) > 20:
                print(f"  ... 还有 {len(other_channels) - 20} 个未显示")

if __name__ == "__main__":
    asyncio.run(main())
