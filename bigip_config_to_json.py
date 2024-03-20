
from re import search;
import os;

def bigip_config_to_json(xlist=list(), flag=False):
    if os.path.isfile("bigip.conf"):
        with open("bigip.conf", "r") as file:
            bigip_config = file.read().split("\n");
        
    for line in bigip_config:
        if search("^ltm\svirtual\s(.*)\s{$", line):
            virtual_server = search("^ltm\svirtual\s(.*)\s{$", line).group(1);
            xdict = {"virtual_server": virtual_server, "pool": str(), "nodes": list()};
            flag = True;

        if flag:
            if search("^\s+pool\s(.*)$", line):
                xdict["pool"] = search("^\s+pool\s(.*)$", line).group(1);
                
            if search("^}$", line):
                xlist.append(xdict);
                flag = False;

    for i, xdict in enumerate(xlist):
        for line in bigip_config:
            if search("^ltm\spool\s(.*)\s{$", line):
                if xdict.get("pool") == search("^ltm\spool\s(.*)\s{$", line).group(1):
                    flag = True;

            if flag:
                if search("^\s+address\s(.*)$", line):
                    xlist[i].get("nodes").append(search("^\s+address\s(.*)$", line).group(1));
                    
                if search("^}$", line):
                    flag = False;

    return xlist;
