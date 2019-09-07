#The re library is necessary for processing regular expressions.
import re
#The glob library allows the processing of multiple files.
import glob
#The os library allows for us to use relative file paths.
import os 
#The sys library allows the parsing of command-line arguments
import sys

#This block of code allows us to use relative file paths in our code, and fetches the file path and target file name from the CLI.
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "./" + sys.argv[1])
target_filename = os.path.join(filename, sys.argv[2])

#This line fetches all of the .eml files in the indicated directory.
filenames = glob.glob(filename + "/*.eml")

#These are the (mostly global) variables that are used in this program.
spam_count = 0
email_count = 0
evidence = ""
preponderance = 0
spam_flag = False

#The spam_detector() method reduces redundancy in the spam_typer() method.
#In short, it checks the email against each item housed in a pattern, a pattern being spam words in a given category.
#If possible spam is detected, the guilty word is concatenated to a string of evidence words, 
#and the preponderance is incremented.
def spam_detector(pattern, email):
    
    global evidence
    global preponderance

    for item in pattern:
        if re.search(item, email):
            evidence += " " + item
            preponderance += 1

#The spam_typer() method ingests an email and categorizes what kind of spam, if any, it is.
#Each of the patterns contains a list of words associated with a category of spam.
#The spam_detector() method is used to check the ingested email against the particular pattern.
#If a preponderance of evidence is reached, the spam_count is incremented. 
#If verbosity is set to True, a message will be displayed, indicating what kind of spam a particular email is, and the evidence for that identification.
def spam_typer(email, verbosity):
    
    global spam_count
    global evidence
    global preponderance
    global spam_flag
    
    #This block of code contains all of the designated spam patterns. Hard-coded for efficiency!
    commerce_pattern = ["as seen on", "buy", "buy direct", "buying judgments", "clearance", "order", "order status", "orders shipped by", "shopper", "self employed"]
    personal_pattern = ["dig up dirt on friends", "singles", "score with babes"]
    employment_pattern = ["additional income", "be your own boss", "compete for your business", "double your", "earn $", "earn extra cash", "earn per week", "expect to earn", "extra income", "home based", "home employment", "homebased", "homebased business", "income from home", "make money"]
    financial_general_pattern = ["$$$", "affordable", "bargain", "beneficiary", "best price", "big bucks", "cash", "cash bonus", "cashcashcash", "cents on the dollar", "cheap", "check", "claims," "collect", "compare rates", "cost", "credit", "credit bureaus", "discount", "earn", "easy terms", "f r e e", "fast cash", "for just $", "hidden assets", "hidden charges", "income", "incredible deal", "insurance", "investment", "loans", "lowest price", "million dollars", "money", "money back", "mortgage", "mortgage rates", "no cost", "no fees", "one hundred percent free", "only $", "pennies a day", "price", "profits", "pure profit", "quote", "refinance", "save $", "save big money", "save up to", "serious cash", "subject to credit", "they keep your money", "unsecured debt", "US dollars", "why pay more"]
    general_pattern = ["acceptance", "accordingly", "avoid", "chance", "dormant", "freedom", "here", "hidden", "home", "leave", "lifetime", "lose", "maintained", "medium", "miracle", "never", "passwords", "problem", "remove", "reverses", "sample", "satisfaction", "stop", "solution", "wife", "success", "teen"]
    financial_business_pattern = ["accept credit cards", "cards accepted", "check or money order", "credit card offers", "explode your business", "full refund", "investment decision", "no credit check", "no hidden costs", "no investment", "requires initial investment", "sent in compliance", "stock alert", "stock disclaimer statement", "stock pick"]
    financial_personal_pattern = ["avoid bankruptcy", "calling creditors", "collect child support", "consolidate debt and credit", "consolidate your debt", "eliminate bad credit", "get paid", "eliminate debt", "financially independent", "get out of debt", "lower interest rate", "lower monthly payment", "lower your mortgage rate", "lowest insurance rates", "pre-approved", "refinance home", "social security number", "your income"]
    greetings_pattern = ["dear ", "friend", "hello"]
    marketing_pattern = ["ad", "auto email removal", "bulk email", "click", "click below", "click here", "click to remove", "direct email", "direct marketing", "email harvest", "email marketing", "form", "increase sales", "increase traffic", "increase your sales", "internet market", "internet marketing", "marketing", "marketing solutions", "mass email", "member", "month trial offer", "more internet traffic", "multi level marketing", "notspam", "not spam", "one time mailing", "online marketing", "open", "opt in", "performance", "removal instructions", "sale", "sales", "search engine listings", "search engines", "subscribe", "the following form", "this isn't junk", "this isn't spam", "undisclosed recipient", "unsubscribe", "visit our website", "we hate spam", "web traffic", "will not believe your eyes"]
    medical_pattern = ["cures baldness", "diagnostics", "fast viagra delilvery", "human growth hormone", "life insurance", "lose weight", "lose weight spam", "medicine", "no medical exams", "online pharmacy", "removes wrinkles", "reverses aging", "stop snoring", "valium", "viagra", "vicodin", "weight loss", "xanax"]
    numbers_pattern = ["#1", "100% free", "100% satisfied", "4u", "50% off", "billion", "billion dollars", "join millions", "join millions of americans", "million", "one hundred percent guaranteed", "thousands"]
    offers_pattern = ["being a member", "billing address", "call", "cannot be combined with any other offer", "confidentiality on all orders", "deal", "financial freedom", "gift certificate", "giving away", "guarantee", "have you been turned down?", "if only it were that easy", "important information regarding", "in accordance with the laws", "long distance phone offer", "mail in order form", "message contains", "name brand", "nigerian", "no age restrictions", "no catch", "no claim forms", "no disappointment", "no experience", "no gimmick", "no inventory", "no middleman", "no obligation", "no purchase necessary", "no questions asked", "no selling", "no strings attached", "no-obligation", "not intended", "obligation", "off shore", "offer", "per day", "per week", "priority mail", "prize", "prizes", "produced and sent out", "reserves the right", "shopping spree", "stuff on sale", "terms and conditions", "the best rates", "they're just giving it away", "trial", "unlimited", "unsolicited", "vacation", "vacation offers", "warranty", "we honor all", "weekend getaway", "what are you waiting for?", "who really wins?", "win", "winner", "winning", "won", "you are a winner!", "you have been selected", "you're a winner!"]
    cta_pattern = ["cancel at any time", "compare copy accurately", "get", "give it away", "print form signature", "print out and fax", "see for yourself", "sign up free today"]
    free_pattern = ["free", "free access", "free cell phone", "free consultation", "free dvd", "free gift", "free grant money", "free hosting", "free installation", "free instant", "free investment", "free leads", "free membership", "free money", "free offer", "free preview", "free priority mail", "free quote", "free sample", "free trial", "free website"]
    descriptions_pattern = ["all natural", "all new", "amazing", "certified", "congratulations", "drastically reduced", "fantastic deal", "for free", "guaranteed", "it's effective", "outstanding values", "promise you", "real thing", "risk free", "satisfaction guaranteed"]
    urgency_pattern = ["access", "act now!", "apply now", "apply online", "call free", "call now", "can't live without", "do it today", "don't delete", "don't hesitate", "for instant access", "for only", "for you", "get it now", "get started now", "great offer", "info you requested", "information you requested", "instant limited time", "new customers only", "now", "now only", "offer expires", "once in lifetime", "one time", "only", "order now", "order today", "please read", "special promotion", "supplies are limited", "take action now", "time limited", "urgent", "while supplies last"]
    nouns_pattern = ["addresses on cd", "beverage", "bonus", "brand new pager", "cable converter", "casino", "celebrity", "copy dvds", "laser printer", "legal", "luxury car", "new domain extensions", "phone", "rolex", "stainless steel"]

    spam_detector(commerce_pattern, email)
    if preponderance > 2:
        spam_count += 1
        spam_flag = True
        if verbosity == True:
            print(sys.argv[2] + " is commerce spam. \nEvidence: " + evidence + ".")
    preponderance = 0
    evidence = ""
    
    spam_detector(personal_pattern, email)
    if preponderance > 0:
        if verbosity == True:
            print(sys.argv[2] + " is personal spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""
   
    spam_detector(employment_pattern, email)
    if preponderance > 0:
        if verbosity == True:
            print(sys.argv[2] + " is employment spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""
    
    spam_detector(financial_general_pattern, email)
    if preponderance > 4:
        if verbosity == True:
            print(sys.argv[2] + " is financial - general spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""
    
    spam_detector(general_pattern, email)
    if preponderance > 4:
        if verbosity == True:
            print(sys.argv[2] + " is general spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(financial_business_pattern, email)
    if preponderance > 0:
        if verbosity == True:
            print(sys.argv[2] + " is financial - business spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(financial_personal_pattern, email)
    if preponderance > 0:
        if verbosity == True:
            print(sys.argv[2] + " is financial - personal spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(greetings_pattern, email)
    if preponderance > 1:
        if verbosity == True:
            print(sys.argv[2] + " is greeting spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(marketing_pattern, email)
    if preponderance > 5:
        if verbosity == True:
            print(sys.argv[2] + " is marketing spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(medical_pattern, email)
    if preponderance > 0:
        if verbosity == True:
            print(sys.argv[2] + " is medical spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""
    
    spam_detector(numbers_pattern, email)
    if preponderance > 1:
        if verbosity == True:
            print(sys.argv[2] + " is numbers spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(offers_pattern, email)
    if preponderance > 3:
        if verbosity == True:
            print(sys.argv[2] + " is offers spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(cta_pattern, email)
    if preponderance > 1:
        if verbosity == True:
            print(sys.argv[2] + " is calls-to-action spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(free_pattern, email)
    if preponderance > 1:
        if verbosity == True:
            print(sys.argv[2] + " is free spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(descriptions_pattern, email)
    if preponderance > 0:
        if verbosity == True:
            print(sys.argv[2] + " is descriptions/adjectives spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(urgency_pattern, email)
    if preponderance > 3:
        if verbosity == True:
            print(sys.argv[2] + " is sense of urgency spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    spam_detector(nouns_pattern, email)
    if preponderance > 1:
        if verbosity == True:
            print(sys.argv[2] + " is nouns spam. \nEvidence: " + evidence + ".")
        spam_count += 1
        spam_flag = True
    preponderance = 0
    evidence = ""

    if verbosity is True:
        spam_count = 0

#This block determines what type (if any) of spam a designated email is.
spam_typer(open(target_filename).read().lower(), True)
if spam_flag is False:
    print(sys.argv[2] + " is ham.")

#This for-loop loops through all of the emails in the directory and checks them against the spamword patterns.
for f in filenames:
    email_count += 1
    spam_typer(open(f).read().lower(), False)
            
#This prints out the grand total of both spam and ham emails.
print("Spam: " + str(spam_count) + " Ham: " + str(email_count - spam_count) + ".")
