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
        print ('rule_prefix.py -i <input directory> -p <prefix> -l <slack link>')
        sys.exit(2)
    if(not opts):
        print ('Syntax: rule_prefix.py -i <input directory> -p <prefix> -l <slack link>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('rule_prefix.py -i <input directory> -p <prefix> -l <slack link>')
            sys.exit()
        elif opt in ("-i", "--indir"):
            inputdir = arg
        elif opt in ("-p", "--prefix"):
            prefix = arg
        elif opt in ("-l", "--link"):
            link = arg        
    files= os.listdir(inputdir)
    print(type(files))
    for file in files:
        if file.endswith('.yaml'):
            rule_prefix(inputdir + file, prefix, link)

def rule_prefix(file, prefix,link):
    s= open(file,"r+").read()
    
    if "alert:\n- debug\n" in s:
        print (file)
        s = s.replace('name: ', 'name: '+prefix + '_')
        s = s.replace('alert:\n- debug\n', '')
        s = s + '\nalert: "slack"\n'
        s = s + 'slack_webhook_url: "' + link + '"'
        print (s)
    f = open(file, 'w')
    f.write(s)
    f.close()

if __name__ == "__main__":
   main(sys.argv[1:])

