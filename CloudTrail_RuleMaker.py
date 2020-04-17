import xlrd

def getListEventNames(eventNames: str) -> list:
    list = eventNames.split('/')
    return list

def processRuleNames(useCase: str) -> str:
    return useCase

def processCondition(eventNames: str):
    list = getListEventNames(eventNames)
    condition = 'eventName:\n'
    for eventName in list:
        condition = condition +\
                     '\t'*3 +\
                    '- "' +\
                     eventName +'"\n'
    return condition

def openXlsx(filepath):
    workbook = xlrd.open_workbook(filepath)
    worksheet = workbook.sheet_by_index(0)
    pairDict = {}
    for i in range(worksheet.nrows):
        useCase = worksheet.cell_value(i,1)
        eventName = worksheet.cell_value(i,2)
        pairDict[useCase]=eventName
    return pairDict

def exportRule(ruleName, data):
    fileName = './CloudTrail_Rules/' + ruleName.replace(' ', '_') + '.yml'
    print (fileName)
    file = open(fileName, 'w+')
    file.write(data)
    file.close()
    return 0


if __name__ == "__main__":
    pairDict = openXlsx('AWS Cloud Rule Cloudtrail.xlsx')
    # print (pairDict)
    for (useCase,eventNames) in pairDict.items():
        if len(eventNames) == 0:
            continue
        ruleName = processRuleNames(useCase).replace(':','')
        condition = processCondition(eventNames)
        with open('./sigma_template.yml') as file:
            data = file.read()
            data = data % (ruleName, ruleName, condition)
            # print (data)
            exportRule(ruleName, data)
        
        # break