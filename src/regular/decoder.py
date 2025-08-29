import os
import pandas as pd
from xml.etree.ElementTree import parse
import numpy as np
import re
import config



def get_decoder_dataframe():
    try:
        data_list = []
        for file_name in os.listdir(config.decoders_path):
            file_path = os.path.join(config.decoders_path, file_name)
            for item in parse(file_path).iterfind('decoder'):
                dc1 =  {}
                dc1['decoder_name'] = item.attrib.get("name")
                dc1['parent'] = item.findtext('parent',default="")
                dc1['type'] = item.findtext('type')
                dc1['order'] = re.sub("\s+","",item.findtext('order',default="")).split(",")
                dc1['fts'] = item.findtext('fts')
                dc1['use_own_name'] = item.findtext('use_own_name')
                # dc1['program_name_pcre2'] = [re.compile(i.text,flags=re.IGNORECASE) for i in item.findall('program_name_pcre2')]
                dc1['program_name_pcre2'] = [i.text for i in item.findall('program_name_pcre2')]
                dc1['program_name_flag'] = True if item.findtext('program_name') is not None else False
                dc1['prematch_pcre2'] = [i.text for i in item.findall('prematch_pcre2')]
                dc1['pcre2'] = [i.text for i in item.findall('pcre2')]
                offset1 = np.array([i.attrib.get("offset") for i in item.iter("pcre2")])
                dc1['offset_in_pcre2'] = np.delete(offset1, np.where(offset1 == None)).tolist()
                offset2 = np.array([i.attrib.get("offset") for i in item.iter("prematch_pcre2")])
                dc1['offset_in_prematch_pcre2'] = np.delete(offset2, np.where(offset2 == None)).tolist()
                data_list.append(dc1)
           
        else:
            return pd.DataFrame(data_list)
  

    except Exception as e:
        print('decoder.d 规则验证不通过！')
        print(str(e))

    else:
        print('decoder.d规则更新成功.')


    
