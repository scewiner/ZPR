import argparse
from typing import List,AnyStr,Tuple
import re

def read_data(filename:AnyStr)->List:
    data = []
    with open(filename,'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def make_subset(src:List,tgt:List,tag:AnyStr)->Tuple:
    sub_src = []
    sub_tgt = []
    for s,t in zip(src,tgt):
        if '>' in t:
            sub_src.append(s)
            sub_tgt.append(t)
    return sub_src,sub_tgt


# def scoring_tag_F1(src:List,tgt:List,tag:AnyStr):
#     pattern = '<(.*?)>'+tag
#     pattern_tgt = '<(.*?)>'
#     TP = 0
#     FP = 0
#     TN = 0
#     FN = 0
#     Totals = 0
#     for s,t in zip(src,tgt):
#         s = s.split()
#         s = [x for x in s if tag in x]
#         Totals +=len(s)
#         s = ' '.join(s)
#         s_g = re.findall(pattern,s)
#         t_g = re.findall(pattern_tgt,t)
#
#         if len(t_g)==0:
#             FN+=len(s_g)
#             continue
#         if len(s_g)>len(t_g):
#             FN += len(s_g)-len(t_g)
#         is_tp = []
#         for tp in t_g:
#             if tp in s_g:
#                 is_tp.append(tp)
#         if len(t_g)>len(s_g):
#             FP += len(t_g)-len(s_g)
#             TP+=len(is_tp) if len(is_tp)<=len(s_g) else len(s_g)
#             FN+=max((len(s_g)-len(is_tp)),0)
#             continue
#         TP += len(is_tp)
#         FN += (len(t_g)-len(is_tp))
#
#     print(Totals)
#     P = TP/(TP+FP)
#     R = TP/(TP+FN)
#     F1 = 2*(P*R)/(P+R)
#     print('P: {} R:{} F1:{} Total:{}'.format(P,R,F1,Totals))



def scoring_acc(src:List,tgt:List,tag:AnyStr):
    # pattern = '<(.*?)>'+tag
    pattern_tgt = '<(.*?)>'
    Totals = 0
    TP = 0
    for s,t in zip(src,tgt):
        s = s.split()+['final']
        t_ = re.findall(pattern_tgt,t)
        # if len(t_)==0:
        #     continue
        t = t.split()+['final']
        s_w = []
        s_p = []
        for p,w in enumerate(s):
            if '<' in w:
                s_w.append(w)
                p-=len(s_p)
                s_p.append(p)
        t_w = []
        t_p = []
        for p,w in enumerate(t):
            if '<' in w:
                t_w.append(w)
                p-=len(t_p)
                t_p.append(p)
        assert len(t)-len(t_w) ==len(s)-len(s_w), '{} vs {}'.format(len(t)-len(t_w),len(s)-len(s_w))
        new_s = [0]*(len(t)-len(t_w))
        new_t = [0]*len(new_s)
        for n,(p,w) in enumerate(zip(s_p,s_w)):
            p = int(p)-n
            new_s[p]=w
        for n,(p,w) in enumerate(zip(t_p,t_w)):
            p = int(p) -n
            new_t[p] = w

        new = [(x,y) for x,y in zip(new_s,new_t) if tag in str(x) and y!=0]
        Totals += len(new)

        for (x,y) in new:
            x = re.findall(pattern_tgt,x)
            y = re.findall(pattern_tgt, str(y))
            if str(x) == str(y):
                TP += 1

    acc = TP / Totals
    print('T : {} Total : {} Acc: {}'.format(TP,Totals,acc))






def main(args):
    sources = read_data(args.input)
    target = read_data(args.hpy)
    assert len(sources) == len(target)
    sub_src,sub_tgt = make_subset(sources,target,args.tag)
    # scoring_tag_F1(sub_src,sub_tgt,args.tag)
    scoring_acc(sub_src,sub_tgt,args.tag)

if __name__ == '__main__':
    params = argparse.ArgumentParser()
    params.add_argument('-i','--input')
    params.add_argument('-t','--tag')
    params.add_argument('-p','--hpy')
    args = params.parse_args()
    main(args)
