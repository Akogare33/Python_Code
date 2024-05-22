import os

log_dir = "C:\\Users\\v_yljeyang\\Documents\\WeChat Files\\wxid_bptjh1stivih12\\FileStorage\\File\\2024-03\\蛊真人.txt"

# with open(log_dir,encoding='utf-8') as file:
with open(log_dir,encoding='utf-8', mode='r') as infile, open('output.txt',encoding='utf-8', mode='w') as outfile:
    separator_found = False
    for line in infile:
        if separator_found:
            outfile.write(line.strip() + '\n')
        elif line.startswith('第七节：九五至尊仙窍（下）'):
            separator_found = True      

