from tomlkit import parse, dumps
from toml import loads

def tom_parse(in_str):
    return loads(in_str)

def tom_dump(in_dic):
    return dumps(in_dic)
