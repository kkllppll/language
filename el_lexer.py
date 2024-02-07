 	
# Таблиця лексем мови
tableOfLanguageTokens = {'program':'keyword', 'begin':'keyword', 'var':'keyword', 'end':'keyword',
						 'if':'keyword', 'for':'keyword', 'to':'keyword', 'by':'keyword', 'do':'keyword', 'rof':'keyword', 
						 'boolean':'keyword', 'true':'boolvar', 'false':'boolvar','read':'keyword', 'write':'keyword', 'real':'keyword', 'integer':'keyword',
						 '=':'assign_op', 
						 '+':'add_op', '-':'add_op',
						 '*':'mult_op', '/':'mult_op',
						 '^':'power_op',
						 '>':'rel_op',
						 '<':'rel_op',
						 '<=':'rel_op',
						 '>=':'rel_op',
						 '==':'rel_op', 
                         '!=':'rel_op',
						 '(':'par_op', ')':'par_op',
						 '{':'par_op', '}':'par_op',
						 ',':'punct_op', ';':'punct_op',
						 '_':'punct_op', ':':'decl_op',
						 '.':'dot', 
						 ' ':'ws', '\t':'ws', '\n':'nl'}



# Решту токенів визначаємо не за лексемою, а за заключним станом
tableIdentFloatInt = {2:'ident', 14:'integer',  17:'real', 21:'real'}

# Діаграма станів
#               Q                                                                                          q0          F
# M = ({0, 1, 2, 4, 5, 6, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 101, 102, 103, 104, 105}, Σ,  δ , 0 , {0, 1, 2, 4, 5, 6, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 101, 102, 103, 104, 105})

# δ - state-transition_function
stf={(0,'Letter'):1,  (1,'Letter'):1, (1,'Digit'):1, (1, 'UnderScore'):1,  (1,'other'):2,\
	 
     (0,'Digit'):13, (13,'Digit'):13, (13,'other'):14,  (13,'dot'):15, (15,'Digit'):16, (15,'other'):102, (16,'Digit'):16, (16,'E'):18, (16,'other'):17, (18,'Digit'):20, (18,'+'):19, (18,'-'):19, (18,'other'):103, 
	 (19,'Digit'):20, (19,'other'):105, (20,'Digit'):20, (20,'other'):21, \
	 
     (0, ':'):3, (3,'='):5, (3,'other'):4, \
	 (0,'='):6, (0,'<'):6, (0,'>'):6, (6,'other'):7, (6,'='):8,
	
	 (0,'!'):9, (9,'='):10, (9,'other'):104, \
    		  
     (0, 'ws'):0, \

     (0, 'nl'):12, \
     (0, '+'):11, (0, '-'):11, (0, '*'):11, (0, '^'):11, (0, '('):11, (0, ')'):11, (0, '{'):11, (0, '}'):11, (0, ';'):11, (0, ':'):11,  (0, ','):11, (0, '.'):11, (0, '/'):11,  \
     (0, 'other'):101
}


initState = 0   # q0 - стартовий стан
F = {2, 4, 5, 7, 8, 10, 11, 12, 14, 17, 21, 101, 102, 103, 104, 105}
Fstar = {2, 4, 7, 14, 17, 21}   # зірочка
Ferror = {101, 102, 103, 104, 105}# обробка помилок
 

tableOfId={}   # Таблиця ідентифікаторів
tableOfConst={} # Таблиць констант
tableOfSymb={}  # Таблиця символів програми (таблиця розбору)


state=initState # поточний стан

f = open('test.my_lang', 'r')
sourceCode=f.read()
f.close()

# FSuccess - ознака успішності розбору
FSuccess = (True,'Lexer')

lenCode=len(sourceCode)-1       # номер останнього символа у файлі з кодом програми
numLine=1                       # лексичний аналіз починаємо з першого рядка
numChar=-1                      # з першого символа (в Python'і нумерація - з 0)
char=''                         # ще не брали жодного символа
lexeme=''                       # ще не починали розпізнавати лексеми


def lex():
	global state,numLine,char,lexeme,numChar,FSuccess
	try:
		while numChar<lenCode:
			char=nextChar()					# прочитати наступний символ
			classCh=classOfChar(char)		# до якого класу належить 
			state=nextState(state,classCh)	# обчислити наступний стан
			if (is_final(state)): 			# якщо стан заключний
				processing()				# виконати семантичні процедури
				# if state in Ferror:	    # якщо це стан обробки помилки  
					# break					#      то припинити подальшу обробку 
			elif state==initState:lexeme=''	# якщо стан НЕ заключний, а стартовий - нова лексема
			else: lexeme+=char		# якщо стан НЕ закл. і не стартовий - додати символ до лексеми
		print('Lexer: Лексичний аналіз завершено успішно')
	except SystemExit as e:
		# Встановити ознаку неуспішності
		FSuccess = (False,'Lexer')
		# Повідомити про факт виявлення помилки
		print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))

def processing():
	global state,lexeme,char,numLine,numChar, tableOfSymb
	if state==12:		# \n
		numLine+=1
		state=initState
	if state in (2, 4, 7, 14, 17, 21):	# keyword, ident, float, int
		token=getToken(state,lexeme) 
		if token!='keyword' and token !='assign_op' and token != 'rel_op': # не keyword
			index=indexIdConst(state,lexeme)
			print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,index)
		else: # якщо keyword
			print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token)) #print(numLine,lexeme,token)
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme=''
		numChar=putCharBack(numChar) # зірочка
		state=initState
	
	if state in (5, 8, 10, 11, 12): 
		lexeme+=char
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme='' 
		state=initState
	if state in Ferror:  #(101,102,103,104,105):  # ERROR
			fail()

def fail():
	global state,numLine,char
	print(numLine)
	if state == 101:
		print('Lexer: у рядку ',numLine,' неочікуваний символ '+char)
		exit(101)
	if state == 102:
		print('Lexer: у рядку ',numLine,' очікувався Digit,а не '+char)
		exit(102)
	if state == 103:
		print('Lexer: у рядку ',numLine,' очікувався Digit або "+", або "-", а не '+char)
		exit(103)
	if state == 104:
		print('Lexer: у рядку ',numLine,' очікувався символ =, а не '+char)
		exit(104)
	if state == 105:
		print('Lexer: у рядку ',numLine,' очікувався Digit,а не '+char)
		exit(105)
		
def is_final(state):
	if (state in F):
		return True
	else:
		return False

def nextState(state,classCh):
	try:
		return stf[(state,classCh)]
	except KeyError:
		return stf[(state,'other')]

def nextChar():
	global numChar
	numChar+=1
	return sourceCode[numChar]

def putCharBack(numChar):
	return numChar-1

def classOfChar(char):
    if char in '.':
        res = "dot"
    elif char in 'abcdefghijklmnopqrstuvwxyz':
        res = "Letter"
    elif char in "0123456789":
        res = "Digit"
    elif char in "_":
        res = "UnderScore"
    elif char in " \t":
        res = "ws"
    elif char in "\n":
        res = "nl"
    elif char in "+-:=^*/(){}<>!;,Ee":
        res = char
    else:
        res = 'символ не належить алфавіту'
    return res


def getToken(state,lexeme):
	try:
		return tableOfLanguageTokens[lexeme]
	except KeyError:
		return tableIdentFloatInt[state]

def indexIdConst(state,lexeme):
	indx=0
	if state==2 and lexeme not in {"true", "false"}:
		indx=tableOfId.get(lexeme)
#		token=getToken(state,lexeme)
		if indx is None:
			indx=len(tableOfId)+1
			tableOfId[lexeme]=indx
	elif state == 14 or state == 17 or state == 21 or lexeme in {"true", "false"}:
		indx=tableOfConst.get(lexeme)
		if indx is None:
			indx=len(tableOfConst)+1
			tableOfConst[lexeme]=indx
	


# запуск лексичного аналізатора	
lex()

# Таблиці: розбору, ідентифікаторів та констант
print('-'*30)
#print('tableOfSymb:{0}'.format(tableOfSymb))
#print('tableOfId:{0}'.format(tableOfId))
#print('tableOfConst:{0}'.format(tableOfConst))

