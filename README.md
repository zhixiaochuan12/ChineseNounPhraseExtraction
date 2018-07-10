# Chinese noun phrase extraction

**code** modified from [phrasemachine project](https://github.com/slanglab/phrasemachine/blob/master/py/phrasemachine/phrasemachine.py)

**method** referred from [Justeston and Katz (1995)](https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q=Justeston+and+Katz+%281995%29&btnG=)

**key idea**: extract noun phrases by pattern *((A|N)+|(A|N)\*(NP)?(A|N)\*)N*

phrasemachine only supports English, this project can extract noun phrases by jieba.

## Example

**Input**(Chinese string)

>"中华人民共和国位于亚洲东部，太平洋西岸，是工人阶级领导的、以工农联盟为基础的人民民主专政的社会主义国家。"

**Output**(index of extracted noun phrases)

>[(0, 1),
 (2, 3),
 (5, 6),
 (9, 10),
 (9, 11),
 (10, 11),
 (16, 17),
 (18, 19),
 (18, 20),
 (19, 20),
 (21, 22),
 (21, 23),
 (22, 23)]
 
 ## TODO
 
 1. coarsemap completion
