import os
import pandas as pd
from xml.etree.ElementTree import parse
import numpy as np
import re
import config


def get_rules_dataframe():
    try:
        data_list = []
        df = pd.DataFrame()
        # ss = pd.Series()
        for file_name in os.listdir(config.rules_path):
            file_path = os.path.join(config.rules_path, file_name)
            for i in parse(file_path).getroot():
                if i.tag == 'var':
                    # ss=ss.append(pd.Series({dc1['group_name']:i.text}))
                    pass
                for j in i:
                    dc1 =  {}
                    dc1['group_name'] = i.attrib.get("name")
                    dc1["id"] = j.attrib.get("id")
                    dc1["level"] = j.attrib.get("level")
                    dc1["maxsize"] = j.attrib.get("maxsize")
                    dc1["frequency"] = j.attrib.get("frequency")
                    dc1["timeframe"] = j.attrib.get("timeframe")
                    dc1["program_name_pcre2"] = np.array([re.compile(p3.text,re.I) for p3 in j.iterfind("program_name_pcre2")])
                    dc1["if_sid"] = np.array(re.sub("\s+","",j.findtext('if_sid',default="")).split(","))
                    dc1["pcre2"] = np.array([re.compile(p2.text,re.I) for p2 in j.iterfind("pcre2")])
                    dc1["id_pcre2"] = j.findtext('id_pcre2')
                    dc1["status_pcre2"] = j.findtext('status_pcre2')
                    dc1["extra_data_pcre2"] = j.findtext('extra_data_pcre2')
                    dc1["action"] = j.findtext('action')
                    dc1["url_pcre2"] = j.findtext('url_pcre2')
                    dc1["user_pcre2"] = j.findtext('user_pcre2')
                    dc1["group"] = j.findtext('group')
                    dc1["description"] = j.findtext('description')
                    dc1["if_fts"] = j.findtext('if_fts')
                    dc1["if_group"] = j.findtext('if_group')
                    dc1["decoded_as"] = j.findtext("decoded_as")
                    dc1["category"] = j.findtext("category")
                    dc1["if_matched_sid"] = j.findtext("if_matched_sid")
                    dc1["if_matched_group"] = j.findtext("if_matched_group")
                    dc1["check_if_ignored"] = np.array(re.sub("\s+","",j.findtext('check_if_ignored',default="")).split(","))    
                    data_list.append(dc1)
        else:
            df = pd.DataFrame(data_list) 
            # print(df)
            return df
    
    except Exception as e:
        print('rules.d 规则验证不通过！')
        print(str(e))

    else:

        print('rules.d初始化成功.')




