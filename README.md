The spam.py script was created as part of the first project of a graduate Information & Network Security course.

It is a basic spam filter/analyzer. It ingests a group of email files (.eml files, in this case) and checks each of the email files
against a number of different categories of spam - if there is a preponderance of evidence that an email is spam, it is labeled as such.

A specific email is fed into the script in the terminal, like so:
<code>
py spam.py dataset/ TRAIN_00000.eml
</code>



This email will be checked, and the script will display whether the email is spam or "ham," which is to say good email. 

If the email is spam, the output will look like this:

<code>
TRAIN_00023.eml is commerce spam.
Evidence: buy buy sell order now
Spam: 32 Ham: 19
</code>


The specified email is checked seperately against the set of files ingested by the script. 

The script assumes that there is a file named "dataset" that contains the email files that will be filtered in the same directory as the 
script. The script has been tailored to work specifically with the .eml format, but other formats could be used with light modification. 

I opted to hard code the lists of spam terms into each of the categories (or "patterns") for ease of use on my part. 
spam.py uses regular expressions to check each item in a given spam category list against the text content of the email - if a certain
threshhold (indicated by a "preponderance" of evidence) is met, the spam count of the script it incremented. 

The spam_detector() method was defined to be a helper method to the spam_typer() method. The spam_typer() method is the workhorse of
the script - it is lengthy and inelegant, but it gets the job done in a timely manner (particularly with small datasets - larger datasets
may burden the brute force checking algorithm). 

The spam.py script only draws from standard Python libraries, as outlined in the project guidelines (not given here). 

Thank you for checking this out. Cheers, and happy coding! 
