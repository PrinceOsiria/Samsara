############################################################
#Custom Alphabet Generator
#*Returns alphabet as a list
def create_alphabet(AlphabetKey):
    #initializes variables for alphabet key cleaner
    i = 0
    StrippedAlphabetKey = ""
    Alphabet = list("abcdefghijklmnopqrstuvwxyz")
    AlphabetKey = clean_text(AlphabetKey.lower(), Alphabet)

    #cleans alphabet key
    while i < len(AlphabetKey):
      if AlphabetKey[i] not in StrippedAlphabetKey:
          StrippedAlphabetKey = StrippedAlphabetKey + AlphabetKey[i]
      i = i + 1
      
    #initializes variables for alphabet generator
    AlphabetKey = list(StrippedAlphabetKey)

    #Cleans standard alphabet
    i = 0
    while i < len(AlphabetKey):
      x = (ord(AlphabetKey[i]) - 97)
      Alphabet[x] = " "
      i = i + 1

    #creates alphabet and cleans for export
    Alphabet = "".join(Alphabet)
    AlphabetKey = "".join(AlphabetKey)
    Alphabet = AlphabetKey + Alphabet
    Alphabet = Alphabet.replace(" ", "")
    Alphabet = list(Alphabet)

    #Returns alphabet as a list
    return (Alphabet)
############################################################



############################################################
#Text standardization
#*Returns cleaned text in lowercase string by checking to see if each char exists in a given alphabet
def clean_text(DirtyText, Alphabet):
    #initializes text cleaner
    CleanText = ""
    DirtyText = list(DirtyText)

    #cleans text
    x = 0
    while x < len(DirtyText):
      if DirtyText[x] in Alphabet:
          CleanText = CleanText + DirtyText[x]
      elif DirtyText[x] == "~":#Used to clean keys without losing layers
          CleanText = CleanText + DirtyText[x]
      x = x + 1

    #returns cleaned text in lowercase string
    return CleanText
############################################################



############################################################
#Hels Labyrinth Brute Force Attacker
#*Exports results.txt + outputs verbose results
def brute_hels(Alphabet, Keys, CipherText):
    #Imports a thing
    from itertools import permutations
      
    #Initializes Variables
    Keys = Keys.split()
    Combos = []
    file = open("testfile.txt","w") 

    #Shuffles through combinations of keys
    x = 1
    while x <= len(Keys):
      for i in permutations(Keys, x): 
          tmp = " ".join(list(i))
          foo = decode_hels(Alphabet, tmp, CipherText)
          print("\n" + "keys:" + str(tmp) + "|" + "result:" + str(foo))
          file.write("\n" + "keys:" + str(tmp) + "|" + "result:" + str(foo))    
      x = x + 1
    file.close()
############################################################



############################################################
#Hels Labyrinth Decoder
#*Returns lowercase cleartext
def decode_hels(Alphabet, Keys, CipherText):
    #Cycles through each key
    x = 0
    while x < len(Keys):

      #Initializes Variables
      CipherText = list(CipherText)#splits ciphertext into letters
      Keys[x] = list(Keys[x])#splits key into letters
      NumberKey = []
      NumberText = []
      
      #Assigns each letter in the key a number (Based on alphabet given)
      i = 0
      while i < len(Keys[x]):
          tmp = Keys[x][i]
          foo = Alphabet.index(tmp)
          NumberKey.append(foo)
          i = i + 1

      #Assigns each letter in the ciphertext a number (Based on alphabet given)
      i = 0
      while i < len(CipherText):
          tmp = CipherText[i]
          foo = Alphabet.index(tmp)
          NumberText.append(foo)
          i = i + 1

      #Initializes Variables
      Message = []

      #If the key is longer than the ciphertext...
      if len(NumberKey) >= len(NumberText):

          #Generates "Masterkey"
          i = 0
          while i < len(NumberText):
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = tmp - foo

            NumberKey.append(bar)

            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(NumberKey):
            if NumberKey[i] < 0:
                NumberKey[i] = NumberKey[i] + 26
            else:
                i = i + 1

          #Uses "Masterkey"
          i = 0
          while i < len(NumberText):
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = tmp - foo
            Message.append(bar)
            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(Message):
            if Message[i] < 0:
                Message[i] = Message[i] + 26
            else:
                i = i + 1

          #Converts numbers to letters
          i = 0
          while i < len(Message):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1
          Message = "".join(Message)

      #If the key is shorter than the ciphertext...
      elif len(NumberKey) < len(NumberText):
          #Initializes Variable
          Difference = (len(NumberText) - len(NumberKey))

          #Generates "Masterkey"
          i = 0
          while i < Difference:
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = tmp - foo
            NumberKey.append(bar)

            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(NumberKey):
            if NumberKey[i] < 0:
                NumberKey[i] = (NumberKey[i] + 26)
                i = i + 1
            elif NumberKey[i] > 25:
                NumberKey[i] = NumberKey[i] - 26
            else:
                i = i + 1

          #Uses Masterkey
          i = 0
          while i < len(NumberKey):
            tmp = NumberKey[i]
            foo = NumberText[i]
            bar = foo - tmp

            Message.append(bar)

            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(Message):
            if Message[i] < 0:
                Message[i] = (Message[i] + 26)
                i = i + 1
            elif Message[i] > 25:
                Message[i] = Message[i] - 26
            else:
                i = i + 1

          #Converts numbers to letters
          i = 0
          while i < len(NumberKey):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1

          #Converts message from a list of letters to a string
          Message = "".join(Message)

      #Initializes Variables
      NumberText = []
      CipherText = Message

      x = x + 1
      #Loops through next key if applicable

    #Returns cleartext as a lowercase string
    return CipherText
############################################################



############################################################
#Hels Labyrinth Encoder
#*Returns lowercase ciphertext
# input = 
# alphabet as list
# keys as list
# Cleantext as lowercase string
def encode_hels(Alphabet, Keys, CipherText):
    #Loops through keys
    x = 0
    while x < len(Keys):
      #Initializes Variables
      CipherText = list(CipherText)
      Keys[x] = list(Keys[x])
      NumberKey = []
      NumberText = []

      #Assigns each letter in each key to numbers based on given alphabet
      i = 0
      while i < len(Keys[x]):
          tmp = Keys[x][i]
          foo = Alphabet.index(tmp)
          NumberKey.append(foo)
          i = i + 1

      #Assigns each letter in the cleartext to numbers based on given alphabet
      i = 0
      while i < len(CipherText):
          tmp = CipherText[i]
          foo = Alphabet.index(tmp)
          NumberText.append(foo)
          i = i + 1

      #Initializes Variables
      Message = []

      if len(NumberKey) >= len(NumberText):

          i = 0
          while i < len(NumberText):
            tmp = NumberText[i]
            foo = NumberKey[i]

            Message.append(tmp + foo)

            i = i + 1
          i = 0
          while i < len(Message):
            if Message[i] > 25:
                Message[i] = Message[i] - 26
                i = i + 1
            else:
                i = i + 1

          i = 0
          while i < len(Message):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1
          Message = "".join(Message)

      elif len(NumberKey) < len(NumberText):
          Difference = (len(NumberText) - len(NumberKey))

          i = 0
          while i < Difference:
            tmp = NumberText[i]
            NumberKey.append(tmp)

            i = i + 1

          i = 0
          while i < len(NumberKey):
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = foo + tmp
            Message.append(bar)
            i = i + 1

          i = 0
          while i < len(NumberKey):
            if Message[i] > 25:
                Message[i] = (Message[i] - 26)
                i = i + 1
            else:
                i = i + 1

          i = 0
          while i < len(NumberKey):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1

          Message = "".join(Message)

      NumberText = []
      CipherText = Message

      x = x + 1
      
    return CipherText
############################################################



############################################################
#ROT13
#*returns lowercase cleartext
def rot13(CipherText):
    #Imports a thing 
    import codecs

    #Initializes Decoding Variables
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    CipherText = clean_text(CipherText, alphabet)

    #Run decoding program
    return(codecs.decode(CipherText, 'rot_13'))
############################################################



############################################################
#XIO Decoder
#*Returns lowercase cleartext
def decode_xio(message):
    #Initializes variables
    MORSE_CODE_DICT = { 'A':'XI', 'B':'IXXX', 'C':'IXIX', 'D':'IXX', 'E':'X', 'F':'XXIX', 'G':'IIX', 'H':'XXXX', 'I':'XX', 'J':'XIII', 'K':'IXI', 'L':'XIXX', 'M':'II', 'N':'IX', 'O':'III', 'P':'XIIX', 'Q':'IIXI', 'R':'XIX', 'S':'XXX', 'T':'I', 'U':'XXI', 'V':'XXXI', 'W':'XII', 'X':'IXXI', 'Y':'IXII', 'Z':'IIXX', '1':'XIIII', '2':'XXIII', '3':'XXXII', '4':'XXXXI', '5':'XXXXX', '6':'IXXXX', '7':'IIXXX', '8':'IIIXX', '9':'IIIIX', '0':'IIIII', ', ':'IIXXII', '?':'XXIIXX', '/':'IXXIX', '-':'IXXXXI', '!':'IXIXII'}
    decipher = '' 
    citext = ''

    #decodes XIO 
    for letter in message: 
      if letter != 'O': 
          citext += letter
      elif letter == 'O':
            if citext in MORSE_CODE_DICT.values():
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = '' 
      elif letter != ' ':
          citext += letter
      elif letter == ' ':
          if citext in MORSE_CODE_DICT.values():
            decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
            decipher += ' '
            citext = ''
      else:
            print(citext, " = ??? ")
            decipher +=" ??? "
            citext = ''
      
    #Returns lowercase cleartext
    return decipher
############################################################



############################################################
#XIO Encoder
#*Returns lowercase ciphertext
def encode_xio(message):
    #Initializes variables
    MORSE_CODE_DICT = { 'XI':'A', 'IXXX':'B', 'IXIX':'C', 'IXX':'D', 'X':'E', 'XXIX':'F', 'IIX':'G', 'XXXX':'H', 'XX':'I', 'XIII':'J', 'IXI':'K', 'XIXX':'L', 'II':'M', 'IX':'N', 'III':'O', 'XIIX':'P', 'IIXI':'Q', 'XIX':'R', 'XXX':'S', 'I':'T', 'XXI':'U', 'XXXI':'V', 'XII':'W', 'IXXI':'X', 'IXII':'Y', 'IIXX':'Z', 'XIIII':'1', 'XXIII':'2', 'XXXII':'3', 'XXXXI':'4', 'XXXXX':'5', 'IXXXX':'6', 'IIXXX':'7', 'IIIXX':'8', 'IIIIX':'9', 'IIIII':'0', 'IIXXII':', ', 'XXIIXX':'?', 'IXXIX':'/', 'IXXXXI':'-', 'IXIXII':'!'}
    decipher = '' 

    #encodes XIO 
    for letter in message: 
      if letter != ' ':
            if letter in MORSE_CODE_DICT.values():
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(letter)]
                decipher += "O"
            #Replaces unknown chars with " ??? "
            else:
                print(letter, ' = ??? ')
                decipher += ' ??? '
            
      #Allows for spaces
      elif letter == ' ':
          decipher += ' '
      
    #Returns lowercase cleartext
    return decipher
############################################################
