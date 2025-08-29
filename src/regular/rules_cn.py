import pandas as pd
import numpy as np
import config


class RulesCN():
    '''Rules规则中文'''

    def __init__(self):
        self.df = pd.read_csv(config.ossec_rules_cn_path)
    
    def get_cn(self,*rule_id):
        df = self.df[self.df['rule_id'].isin(rule_id)]
        return df['zh_cn'].replace({np.NaN:None}).to_list()