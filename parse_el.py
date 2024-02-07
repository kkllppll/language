from el_lexer import lex
from  el_lexer import tableOfSymb #, tableOfVar, tableOfConst

lex()
# print('-'*30)
# print('tableOfSymb:{0}'.format(tableOfSymb))
# print('-'*30)

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow=1

# довжина таблиці символів програми
# він же - номер останнього запису
len_tableOfSymb=len(tableOfSymb)
print(('len_tableOfSymb',len_tableOfSymb))

# Функція для розбору за правилом
# Program = program StatementList end
# читає таблицю розбору tableOfSymb
def parseProgram():
    try:
        #перевірити наявність ключового слова 'program'
        parseToken('program','keyword','')

        # перевірити наявність імені програми
        parseProgramName()
        parseToken('var','keyword','\t')
        parseDeclarList()
        parseToken('begin','keyword','\t')
        parseDoBlock()
        # перевірити наявність ключового слова 'end'
        parseToken('end','keyword','')

        # повідомити про синтаксичну коректність програми
        print('Parser: Синтаксичний аналіз завершився успішно')
        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('Parser: Аварійне завершення програми з кодом {0}'.format(e))


# Функція перевіряє, чи у поточному рядку таблиці розбору
# зустрілась вказана лексема lexeme з токеном token
# параметр indent - відступ при виведенні у консоль
def parseToken(lexeme,token,indent):
    # доступ до поточного рядка таблиці розбору
    global numRow
    
    # перевірити, чи є ще записи в таблиці розбору
    # len_tableOfSymb - кількість лексем (записів) у таблиці розбору
    if numRow > len_tableOfSymb :
        failParse('неочікуваний кінець програми',(lexeme,token,numRow))

    # прочитати з таблиці розбору 
    # номер рядка програми, лексему та її токен
    numLine, lex, tok = getSymb() 

    # тепер поточним буде наступний рядок таблиці розбору
    numRow += 1

    # чи збігаються лексема та токен таблиці розбору з заданими
    if (lex, tok) == (lexeme,token):
        # вивести у консоль номер рядка програми та лексему і токен
        print(indent+'parseToken: В рядку {0} токен {1}'.format(numLine,(lexeme,token)))
        return True
    else:
        # згенерувати помилку та інформацію про те, що 
        # лексема та токен таблиці розбору (lex,tok) відрізняються від
        # очікуваних (lexeme,token)
        failParse('невідповідність токенів',(numLine,lex,tok,lexeme,token))
        return False


# Прочитати з таблиці розбору поточний запис
# Повертає номер рядка програми, лексему та її токен
def getSymb():
    if numRow > len_tableOfSymb :
            failParse('getSymb(): неочікуваний кінець програми',numRow)
    # таблиця розбору реалізована у формі словника (dictionary)
    # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
    numLine, lexeme, token, _ = tableOfSymb[numRow]	
    return numLine, lexeme, token 


# Обробити помилки
# вивести поточну інформацію та діагностичне повідомлення 
def failParse(str,tuple):
    if str == 'неочікуваний кінець програми':
        (lexeme,token,numRow)=tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format((lexeme,token),numRow))
        exit(1001)
    if str == 'getSymb(): неочікуваний кінець програми':
        numRow=tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(numRow,tableOfSymb[numRow-1]))
        exit(1002)
    elif str == 'невідповідність токенів':
        (numLine,lexeme,token,lex,tok)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(numLine,lexeme,token,lex,tok))
        exit(1)
    elif str == 'невідповідність інструкцій':
        (numLine,lex,tok,expected)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
        exit(2)
    elif str == 'невідповідність у Expression.Factor':
        (numLine,lex,tok,expected)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
        exit(3)

def parseProgramName():
    print('parseProgramName():')
    parseIdent(1)



def parseDeclSection():
    print('parseDeclSection:')
    parseToken('var', 'keyword', '\t')
    parseDeclarList()
    return True
# DeclarList = Declaration { ’;’ Declaration }
def parseDeclarList():
    print('\t parseDeclarList():')
    # перевірити синтаксичну коректність списку інструкцій Declaration
    while parseDeclaration():
        pass
    

# IdenttList = Ident {’,’ Ident}
def parseDeclaration():
    
    numLine, lex, tok = getSymb()
    if (lex, tok) == ('begin', 'keyword'):
        F = False
        return F
    if parseIdentList():
        parseToken(':', 'decl_op', '\t')
        parseType()
        parseToken(';', 'punct_op', '\t')
        
        return True
    else:
        return False


# Type = integer | real | boolean
def parseType():
    global numRow
    print('\t'*3 + 'parseType():')
    numLine, lex, tok = getSymb()
    if tok == 'keyword' and lex in ('integer', 'real', 'boolean'):
        numRow += 1
        print('+'+'\t'*4 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        return True
    # зустріли кінець списку оголошень змінних
    elif (lex, tok) == ('begin', 'keyword'):
        return False
    else:
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'keyword'))
        return False
    
   


# IdentList = Ident {';' Ident }
def parseIdentList():
    global numRow
    print('\t'*3 + 'parseIdentList():')
    
    parseIdent(4)

    F = True
    while F:
        numLine, lex, tok = getSymb()
        if (lex, tok) == (';', 'punct_op'):
            numRow += 1
            print('+'+'\t'*4 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            # Перевірка на наступну лексему 'begin'
            numLine, lex, tok = getSymb()
            if (lex, tok) == ('begin', 'keyword'):
                F = False  # Якщо знайдено 'begin', виходимо з циклу
                print('+'+'\t'*5 + 'знайдено "begin", виходимо з циклу')
                break
            else:
                parseIdent(5)
        else:
            F = False

    return True



# DoBlock = '{' StatementList '}'
def parseDoBlock():
    print('\t parseDoBlock():')
    
    # перевірити синтаксичну коректність списку інструкцій StatementList
    parseStatementList()
    
    
    

# StatementList = Statement {’;’ Statement } ';'
def parseStatementList():
    print('\t\tparseStatementList():')
    while parseStatement():
        pass
    return True


def parseStatementBlock():
    print('\t\tparseStatementBlock():')
    while parseStatement() :
        pass
    return True


# Statement = Assign | Inp | Out | ForStatement | IfStatement
def parseStatement():
    global numRow
    print('\t\t\tparseStatement():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор
    # обробити інструкцію присвоювання
  
    if tok == 'ident':
        return parseAssign()

    # якщо лексема - ключове слово 'if'
    # обробити інструкцію розгалуження
    elif (lex, tok) == ('if','keyword'):
        parseIf()
        return True
    
    elif (lex, tok) == ('rof','keyword'):
   
        return False

    # якщо лексема - ключове слово 'for'
    # обробити інструкцію повторення
    elif (lex, tok) == ('for','keyword'):
        parseFor()
        return True
        

    elif (lex, tok) == ('read', 'keyword'):
        parseInp()
        return True

    elif (lex, tok) == ('write', 'keyword'):
        parseOut()
        return True
    
    # тут - ознака того, що всі інструкції були коректно
    # розібрані і була знайдена остання лексема блоку DoBlock.
    # тому parseStatement() має завершити роботу
    

    elif (lex, tok) == ('end','keyword'):
        return False
    
    elif (lex, tok) == ('}','par_op'):
        return False
    
    

    else:
        # жодна з інструкцій не відповідає
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій',(numLine,lex,tok,'ident або keyword'))
        return False




# Assign = Ident ’=’ Expression
def parseAssign():
    # номер запису таблиці розбору
    print('\t'*4+'parseAssign():')

    parseIdent(5)

    # якщо була прочитана лексема - '='
    if parseToken('=','assign_op','\t'*5):
        # розібрати Expression
        parseExpression()
        
        parseToken(';','punct_op','\t'*6)
        return True
    else: return False

# розбір логічного виразу за правилом
# BoolExpr = Expression
def parseBoolExpr():
    print('\t'*3+'parseBoolExpr():')

    parseExpression()

    return True

# Expression = ArithmExpression { RelOp ArithmExpression }
def parseExpression():
    global numRow
    print('\t'*6 + 'parseExpression():')

    if not parseArithmExpression():
        # якщо досягнуто кінець Expression (тобто ';')
        return False

    F = True

    while F:
        numLine, lex, tok = getSymb()
        if tok in ('rel_op'):
            numRow += 1
            print('+'+'\t'*7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            if not parseArithmExpression():
                # якщо досягнуто кінець Expression (тобто ';')
                return False
        else:
            F = False
    return True


# ArithmExpression = [Sign] Term {AddOp Term}
def parseArithmExpression():
    global numRow
    print('\t'*7 + 'parseArithmExpr():')

    # символи '+' або '-'
    numLine, lex, tok = getSymb()
    if (tok == 'add_op'):
        numRow += 1
        print('+'+'\t'*8 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))

    if not parseTerm():
        # якщо досягнуто кінця Expression (тобто ';')
        return False

    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            print('+'+'\t'*7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            if not parseTerm():
                # якщо досягнуто кінця Expression (тобто ';')
                return False
        else:
            F = False
    return True


# Term = Chunk {MultOp Chunk}
def parseTerm():
    global numRow
    print('\t'*8+'parseTerm():')

    if not parseChunk():
        # якщо досягнуто кінця Expression (тобто ';')
        return False

    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('mult_op'):
            numRow += 1
            numLine1, lex1, tok1 = getSymb()  
            if lex == '/' and lex1 == '0':
                failParse('ділення на 0',(numLine))
            print('\t'*8+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            if not parseChunk():
                # якщо досягнуто кінця Expression (тобто ';')
                return False
        else:
            F = False
    return True



# Chunk = Factor {PowerOp Factor}
def parseChunk():
    global numRow
    print('\t'*9+'parseChunk():')

    if not parseFactor():
        # якщо досягнуто кінця Expression (тобто ';')
        return False

    F = True
    # продовжувати розбирати Частини (Chunk)
    # розділені лексемою '^'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('power_op'):
            numRow += 1
            print('\t'*9+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            if not parseFactor():
                # якщо досягнуто кінця Expression (тобто ';')
                return False
        else:
            F = False
    return True

# Factor = Ident | Const | '(' ArithmExpression ')'
def parseFactor():
    global numRow
    print('\t'*10+'parseFactor():')
    numLine, lex, tok = getSymb()
    print('\t'*10+'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine,(lex, tok)))

    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('integer', 'real', 'boolvar', 'ident'):
        numRow += 1
        print('\t'*10+'в рядку {0} - {1}'.format(numLine,(lex, tok)))

    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex=='(':
        numRow += 1
        parseExpression()
        
        parseToken(')','par_op','\t'*7)
        print('\t'*10+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # четверта альтернатива для Factor
    # якщо досягнуто лексеми ';' - повертаємо False
    # це свідчить про кінець Expression
    elif lex==';':
        return False
    else:
        failParse('невідповідність у Expression.Factor',(numLine,lex,tok,'integer, real, boolvar, ident або \'(\' Expression \')\''))
        # return False
    return True

# розбір інструкції розгалуження за правилом
# IfStatement = if (Condition)  StatemenBlock }
def parseIf():
    global numRow
    print('\t'*4+'parseIf():')
    _, lex, tok = getSymb()
    if lex == 'if' and tok == 'keyword':
        numRow += 1
        parseToken('(', 'par_op', '\t'*5)
        parseCondition()
        parseToken(')', 'par_op', '\t'*5)
        parseStatementBlock()
       
        return True
    else:
        return False

    
def parseCondition():
    print('\t'*10+'parseCondition():')
    parseExpression()
    return True

# ForStatement = for '(' IndExpr ')' do DoBlock rof
#IndExpr = Ident ’=’ ArithmExpression1 by ArithmExpression2 to ArithmExpression3
# ArithmExpression1 = ArithmExpression
# ArithmExpression2 = ArithmExpression
# ArithmExpression3 = ArithmExpression
def parseFor():
    global numRow
    print('\t'*4+'parseFor():')
    _, lex, tok = getSymb()
    if lex == 'for' and tok == 'keyword':
        
        parseToken('for', 'keyword', '\t'*5)
        parseToken('(', 'par_op', '\t'*5)
        parseIndExpr()
        parseToken(')', 'par_op', '\t'*5)
        parseToken('do', 'keyword', '\t'*5)
        parseDoBlock()
        parseToken('rof', 'keyword', '\t'*5)
        
        return True
    else:
        return False

def parseIndExpr():
    global numRow
    print('\t'*4 + 'parseIndExpr():')
    parseIdent(5)
    
    parseToken('=','assign_op','\t'*5)
    parseExpression()
    parseToken('by','keyword','\t'*5)
    parseExpression()
    parseToken('to','keyword','\t'*5)
    parseExpression()


def parseInp():
    print('\t'*4 + 'parseInp():')
    F = parseToken('read', 'keyword', '\t'*3)
    if F:
        F = (parseToken('(', 'par_op', '\t'*3) and
            parseIdentList() and
            parseToken(')', 'par_op', '\t'*3))
    return F

def parseOut():
    print('\t'*4 + 'parseOut():')
    F = parseToken('write', 'keyword', '\t'*3)
    if F:
        F = parseToken('(', 'par_op', '\t'*3)
        _, lex, tok = getSymb()
        if (lex, tok) != (')', 'par_op'):
            # Парсимо список ідентифікаторів
            parseIdentList()
        F = F and parseToken(')', 'par_op', '\t'*3)
        # Після цього очікуємо точку з комою ';'
        F = F and parseToken(';', 'punct_op', '\t'*3)
    return F



def parseIdent(indent=3):
    global numRow
    print('\t'*indent + 'parseIdent():')
    # отримуємо поточну лексему з таблиці розбору
    numLine, lex, tok = getSymb()
    
    if tok == 'ident':
        numRow += 1
        print('+'+'\t'*(indent + 1) + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    else:
        return

# запуск парсера
parseProgram()