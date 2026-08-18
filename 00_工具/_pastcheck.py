import io, json, re
for L in (14,15):
    j = json.load(io.open(r"D:\英语教学\00_工具\practice_content_DXH_L%d.json" % L, encoding="utf-8"))
    def walk(o):
        if isinstance(o,str): yield o
        elif isinstance(o,dict):
            for v in o.values():
                if isinstance(v,str): yield v
                elif isinstance(v,list): 
                    for i in v: yield from walk(i)
        elif isinstance(o,list):
            for i in o: yield from walk(i)
    text = " ".join(walk(j))
    # common past markers
    past_words = [" was "," were "," went "," came "," had "," did "," didn"," said "," told "," saw "," got "," made "," took "," gave "," bought "," paid "," spent "," ate "," drank "," walked "," visited "," stayed "," arrived "," asked "," wanted "," started "," finished "," played "," watched "," studied "," lived "," learned "," learnt "," thanked "," smiled ","help","  yesterday","last week","last weekend","last month","last night"," ago "]
    finds = {}
    for w in past_words:
        c = text.count(w)
        if c: finds[w.strip()] = c
    print("L%d 过去时疑似词:" % L, finds if finds else "NONE")
    # provenance ids
    ids = sorted(set(re.findall(r"DXH\d+_L\d+_\w+", text)))
    print("L%d 溯源ID:" % L, ids)
