import sys, getopt
import os
# def main(argv):
#     return 0



def main(argv):
    inputdir = ''
    prefix = ''
    link = ''
    try:
        opts, args = getopt.getopt(argv,"hi:p:l:",["indir=","prefix=","link="])
    except getopt.GetoptError:
        print ('rule_prefix.py -i <input directory> -p <prefix> -l <mattermost link>')
        sys.exit(2)
    if(not opts):
        print ('Syntax: rule_prefix.py -i <input directory> -p <prefix> -l <mattermost link>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('rule_prefix.py -i <input directory> -p <prefix> -l <mattermost link>')
            print ('Ex: python3 rule_prefix.py -i sigma/rules/VuNX/Elast_Rules/ -p \'VIETL***\' -l \'https://spidey.security.fis.vn/hoo/..\'')
            sys.exit()
        elif opt in ("-i", "--indir"):
            inputdir = arg
        elif opt in ("-p", "--prefix"):
            prefix = arg
        elif opt in ("-l", "--link"):
            link = arg        
    files= os.listdir(inputdir)
    if(inputdir[-1]!='/'):
        inputdir= inputdir + '/'
    print(prefix)
    if not os.path.exists(prefix):
        print ('Non')
        print (inputdir + prefix)
        os.makedirs(inputdir + prefix)

    for file in files:
        if file.endswith('.yaml') or file.endswith('.yml'):
            new_file = (inputdir + prefix + '/' + prefix + '_' + file)
            rule_prefix(inputdir + file, prefix, link, new_file)

def rule_prefix(file, prefix,link, new_file):
    s= open(file,"r+").read()
    
    if "alert:\n- debug\n" in s:
        print (file)
        s = s.replace('name: ', 'name: '+prefix + '_')
        s = s.replace('alert:\n- debug\n', '')
        s = s + '\nalert: "mattermost"\n'
        s = s + 'mattermost_webhook_url: "' + link + '"'
        print (s)
    f = open(new_file, 'w+')
    f.write(s)
    f.close()

if __name__ == "__main__":
   main(sys.argv[1:])

