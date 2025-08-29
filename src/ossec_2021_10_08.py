import numpy as np
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')
from sys import getsizeof

from regular.decoder import get_decoder_dataframe
from regular.rules import get_rules_dataframe
from regular.rules_cn import RulesCN

 
class OSSEC():
    def __init__(self):

        self.dfIsDecoder = get_decoder_dataframe()

        self.dfIsRules = get_rules_dataframe()

        self.dic1 = {"hostname":[],"program_name":[],"full_event":[],"log":[]}
        
        self.hostname = ""
        self.program_name = ""
        self.full_event = ""
        self.msg = ""
        self.log = ""

    def newmsg(self,msg:str=""):
        """日志预处理
        full_event -> log
        日志头格式处理和抽取字段
        """
        msg = re.sub("\s+"," ",msg)
        self.full_event = msg
        msg = re.sub(r"^\[(Mond?a?y?|Tues?d?a?y?|Wedn?e?s?d?a?y?|Thur?s?d?a?y?|Frid?a?y?|Satu?r?d?a?y?|Sund?a?y?)\.? (Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}\d{1,2} {1,2}\d{1,2}:\d{1,2}:\d{1,2} \d{4}\] ?","",msg)
        msg = re.sub(r"^(Janu?a?r?y?|Febr?u?a?r?y?|Marc?h?|Apri?l?|May|June?|July?|Augu?s?t?|Sept?e?m?b?e?r?|Octo?b?e?r?|Nove?m?b?e?r?|Dece?m?b?e?r?)\.? {1,2}(\d{1,2}) {1,2}(\d{1,2}:\d{1,2}:\d{1,2}) ","",msg)
        msg = re.sub(r"^\d{4}-\d{1,2}-\d{1,2}(T| )(\d{1,2}:\d{1,2}:\d{2})(\S)+ ","",msg)

        for pp1 in [re.compile(r'^([^\f\n\r\t\v:]+ )?([^\f\n\r\t\v:]+\[\S+\]:? )',re.I),re.compile(r'^([^\f\n\r\t\v:]+ )?([^\[\]\f\n\r\t\v]+: )',re.I)]:
            searchObj = pp1.search(msg)
            if searchObj is not None:
                g = searchObj.group()
                g1 = searchObj.group(1)
                g2 = searchObj.group(2)
                self.hostname = g1
                program2 = re.sub(r"(\[\S+\])?:? ",": ",g2)
                msg = msg.replace(g,program2)
                program2s = re.search(r"^(\S+): ?",program2)
                if program2s is not None:
                    self.program_name = program2s.group(1)
                break
        msg = msg.replace("{",'"').replace("}",'"')
        self.log = msg
        
    def _program_name_pcre2(self,ss:pd.Series):
        '''第一步:decoder
        根据program_name_pcre2正则解析decoder
        '''
        if ss['parent'] == "":
            for i in ss['program_name_pcre2']:
                mobj = i.search(self.program_name)
                if mobj is None:
                    return False,""
                else:
                    return True,re.sub("^(\S+): ","",self.log)
            else:
                if ss['program_name'] == True:
                    return True,re.sub("^(\S+): ","",self.log)
                else:
                    return True,self.log
        else:
            return False,""
 
    def _prematch_pcre2(self,ss:pd.Series):
        '''第二步:prematch正则判定以及剔除对于字符
        根据prematch_pcre2规则,判断是否符合要求,如果符合则返回True且剔除对于的字符
        '''
        msg = ss['msg']
        span = (0,0)
        if "after_parent" in ss['offset_in_prematch_pcre2']:
            dff = self.dfIsParent.query("decoder_name == '{}'".format(ss['parent']))
            for index, value in dff["prematch_pcre2_span"].items():
                msg = msg[value[-1]:]
                # span = value
        for i in ss['prematch_pcre2']:
            mobj = i.search(msg)
            if mobj is not None:
                if mobj.group() == "":
                    pass
                else:
                    span = (0,span[1] + mobj.span()[1])
                    return True,span
            else:
                return False,(0, 0)
        return True,(None,None)

    def _pcre2(self,ss:pd.Series):
        '''第三步:pcre2正则获取对应的字段值
        完成或第一步且第二步之后.我们得到的log进行pcre2正则判定,并且可以抽取得到对应的order字段值
        '''
        msg = ss['msg']
        if "after_parent" in ss['offset_in_pcre2']:
            dff = self.dfIsParent.query("decoder_name == '{}'".format(ss['parent']))
            for index, value in dff["prematch_pcre2_span"].items():
                msg = msg[value[-1]:]
                                     
        if "after_prematch" in ss['offset_in_pcre2']:
            msg = msg[ss['prematch_pcre2_span'][-1]:]

        if "after_regex" in ss['offset_in_pcre2']:
            dff = self.dfIsChild.query("decoder_name == '{}'".format(ss['decoder_name']))
            dff = dff.explode('offset_in_pcre2')
            dff = dff[dff['offset_in_pcre2'].isna()]
            for index, pcre2 in dff["pcre2"].items():
                for i in pcre2:
                    msg = i.sub("",msg)      
       
        for i in ss['pcre2']:
            list1 = np.array(i.findall(msg)).flatten()
            list2 = np.delete(list1, np.where(list1==""))
            if list2.size > 0:
                self.dic1.update(dict(zip(ss['order'],list2)))
                return True
        else:
            return False

    
    def rules_pcre2(self,ss:pd.Series,parameter="$"):
        """rules.d判定
        判断是否符合正则,留下对应可以对应的规则列表.
        后续可以根据对应的df得到对应的rulesId,Level,description
        """
        pcre2_count = 0
        msg = ss['msg']


        if ss.get('decoded_as') is not None :
            pcre2_count += 1
            if ss['decoded_as'] not in self.dic1.get('decoder',[]):
                
                return False
        
        if ss.get('category') is not None:
            pcre2_count += 1
            if ss['category'] not in self.dic1.get('type',[]):
                return False
        

        if ss.get('if_group') is not None:
            pcre2_count += 1
            if ss['if_group'] not in self.dic1.get('group',[]):
                return False
        
        if ss.get('if_matched_sid') or ss.get('if_matched_group') or ss.get('frequency') or ss.get('timeframe'):
            pcre2_count += 1
            return False 
        
        if ss.get('maxsize') is not None:
            pcre2_count += 1
            if getsizeof(msg) < int(ss['maxsize']):
                return False 
        
        for p2 in ss['program_name_pcre2']:
            pcre2_count += 1
            mobj = p2.search(self.program_name)
            if mobj is None:
                return False

        if ss['pcre2'].size:
            for i in ss['pcre2']:
                pcre2_count += 1
                ps = i.search(msg)
                if ps is not None:
                    if ps.group() != "":
                        break
            else:
                return False
        
        if ss.get('status_pcre2') is not None:
            pcre2_count += 1
            p3 = re.compile(ss['status_pcre2'],flags=re.IGNORECASE)
            if p3.search(self.dic1.get("status","")) is None:
                return False
        

        if ss.get('user_pcre2') is not None:
            pcre2_count += 1
            for i in self.dic1.keys():
                if re.search('user',i):
                    if re.search(ss['user_pcre2'],self.dic1.get(i,""),flags=re.I) is not None:
                        
                        break
            else:
                return False
        
        if ss.get('id_pcre2') is not None:
            pcre2_count += 1
            if re.search(ss['id_pcre2'],self.dic1.get("id",""),flags=re.I) is None:
                return False
        
        if ss.get('extra_data_pcre2') is not None:
            pcre2_count += 1
            if re.search(ss['extra_data_pcre2'],self.dic1.get("extra_data",""),flags=re.I) is None:
                return False

        if '' not in ss.get('check_if_ignored'):
            pcre2_count += 1
            for i in ss.get('check_if_ignored'):
                if i in self.dic1.keys():
                    return False

        
        if ss.get('action') is not None:
            pcre2_count += 1
            if re.search(ss['action'],self.dic1.get("action",""),flags=re.I) is None:
                return False
        
        if ss.get('url_pcre2') is not None:
            pcre2_count += 1
            url_match = re.search(ss['url_pcre2'],self.dic1.get("url",""),flags=re.I)
            if url_match is None:
                return False
            elif url_match.group() == "":
                return False
        
        if ss.get('weekday') is not None:
            pcre2_count += 1
            if re.search(ss['weekday'],self.dic1.get("weekday",""),flags=re.I) is None:
                return False
        
        if ss.get('time') is not None:
            pcre2_count += 1
            if re.search(ss['time'],self.dic1.get("time",""),flags=re.I) is None:
                return False
        
        if '' in ss['if_sid']:
            return True
        
        if pcre2_count > 0:
            return True
        else:
            if ss.get('if_fts') is None:
                return False
            else:
                return True
        

    def if_sid(self,ss:pd.Series,start=0):
        
        if self.program_name != "":
            ss['msg'] = re.sub("^{}: ?".format(self.program_name),"",self.log)
        else:
            ss['msg'] = self.log
        # print("=====================",ss['msg'])
        # print("start=",start)
        # print("ID:",ss.get('id',np.nan))
        # print("if_sid:",ss['if_sid'])
        

        if self.rules_pcre2(ss) is False:
            # print("rules_pcre2否决",False,start) 
            return False,start
        else:
            
            df:pd.DataFrame = self.dfIsRules[self.dfIsRules['id'].isin(ss['if_sid'])]
            if df.empty:
                # print("if_sid穷尽",True,start)
                return True,start
            else:
                df[['OK','start']] = df.apply(lambda x:self.if_sid(x,start=start+1),axis=1,result_type="expand")
                # print(df[['OK','start']])
                return df['OK'].all(),df['start'].max()
                
            
        


    def get_ossec(self,msg:str):
        self.newmsg(msg)
        # 测试
        # print(self.dfIsDecoder[self.dfIsDecoder['decoder_name'].isin(['openbsd-httpd'])])
        # 父级decoder解析
        self.dfIsDecoder[['OK','msg']] = self.dfIsDecoder.apply(lambda x:self._program_name_pcre2(x), axis=1, result_type="expand")
        self.dfIsParent = self.dfIsDecoder[self.dfIsDecoder['OK']]

        if not self.dfIsParent.empty:

            self.dfIsParent[['OK','prematch_pcre2_span']] = self.dfIsParent.apply(lambda x:self._prematch_pcre2(x), axis=1, result_type="expand")
            self.dfIsParent = self.dfIsParent[self.dfIsParent['OK']]
            
            if not self.dfIsParent.empty:
                self.dic1['decoder'] = self.dfIsParent['decoder_name'].drop_duplicates().to_list()
                df_type = self.dfIsParent[self.dfIsParent['type'].apply(lambda x: x is not None)]
                if not df_type.empty:
                    self.dic1['type'] = df_type['type'].drop_duplicates().to_list()
                self.dfIsParent[self.dfIsParent.apply(lambda x:self._pcre2(x),axis=1)]
                # if not self.dfIsParent.empty:
                #     pass


        
        # 子级decoder解析
        self.dfIsChild = self.dfIsDecoder[self.dfIsDecoder['parent'].isin(self.dic1.get('decoder',[]))]
        if not self.dfIsChild.empty:
            df1 = self.dfIsParent[['decoder_name','msg']].set_index(["decoder_name"])
            self.dfIsChild.loc[:,'msg'] = self.dfIsChild['parent'].map(df1['msg'].to_dict())
            self.dfIsChild[['OK','prematch_pcre2_span']] = self.dfIsChild.apply(lambda x:self._prematch_pcre2(x), axis=1, result_type="expand")
            self.dfIsChild = self.dfIsChild[self.dfIsChild['OK']]
            if not self.dfIsChild.empty:
                self.dfIsChild = self.dfIsChild[self.dfIsChild.apply(lambda x:self._pcre2(x),axis=1)]
                self.dic1['child'] = self.dfIsChild['decoder_name'].drop_duplicates().to_list()
                df_own = self.dfIsChild[self.dfIsChild['use_own_name'].apply(lambda x: x is not None)]
                if not df_own.empty:
                    self.dic1['decoder'] = df_own['decoder_name'].drop_duplicates().to_list()
                df_type = self.dfIsChild[self.dfIsChild['type'].apply(lambda x: x is not None)]
                if not df_type.empty:
                    self.dic1['type'] = df_type['type'].drop_duplicates().to_list()

        
        
        # 以下开始Rules.d 解析
        # 定点测试==============================
        # self.dfIsRules = self.dfIsRules[self.dfIsRules['id'].isin(["31100","31108","31103"])]
        # print(self.dfIsRules[['id','pcre2','user_pcre2','id','category']])
        # 定点测试==============================
        self.dfIsRules[['OK','start']] = self.dfIsRules.apply(lambda x:self.if_sid(x), axis=1, result_type="expand")
        self.dfIsRules = self.dfIsRules[self.dfIsRules['OK']]

        
        if not self.dfIsRules.empty:
            self.dfIsRules[['start','level','id']] = self.dfIsRules[['start','level','id']].applymap(lambda x:int(x))
            df_start = self.dfIsRules.sort_values(by=['start','level'],ascending=[False,False]).groupby(['group_name']).head(1)
            # print(df_start)
 
            df_level = df_start[df_start['level'].rank(method='min',ascending=False) == 1.0]
            self.dic1['rule_id'] = df_level['id'].to_list()
            self.dic1['level'] = df_level['level'].to_list()
            self.dic1['description'] = df_level['description'].to_list()

        self.dic1.update({"hostname":self.hostname,"program_name":self.program_name,"full_event":self.full_event,"log":self.log})
        return self.dic1

    @classmethod
    def test(cls,msg):
        this = cls()
        js1 = this.get_ossec(msg)
        js1['rule_cn'] = RulesCN.get_cn(*js1.get('rule_id',[0]))
        return js1




if __name__ == "__main__":
    # ossec stable 版本查看：https://github.com/ossec/ossec-hids/tree/stable
    msg = """Jun 25 14:04:30 10.0.0.1 dropbear[30746]: Failed listening on '7001': Error listening: Address already in use""" 
    # # 正则参数问题，与下面的1002问题一样
    
    msg = """May  8 08:26:55 mail postfix/postscreen[22055]: NOQUEUE: reject: RCPT from [157.122.148.242]:47407: 550 5.7.1 Service unavailable; client [157.122.148.242] blocked using bl.spamcop.net; from=<kos@mafia.network>, to=<z13699753428@vip.163.com>, proto=ESMTP, helo=<XL-20160217QQJV>""" 
    # 按正则规则是正确的，可能与ossec规则有点不一样
    # 3302是正确的，因为id正则确实是符合的，而3306是不符的，ossec stable版本是符合正则的匹配的
    
    # msg = """2014-05-20T09:01:07.283219-04:00 arrakis unbound: [9405:0] notice: sendto failed: Can't assign requested address""" # 稳定版 rule_id=500100~ 不存在 1002结果也是不正确的，1002是普遍存在的
    
    # msg = """[Fri Dec 13 06:59:54 2013] [error] [client 12.34.65.78] PHP Notice:"""
    o = OSSEC()
    m=o.get_ossec(msg)
    print(m)

