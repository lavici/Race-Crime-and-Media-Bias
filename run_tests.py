import naivebayes

for x in [False, True]:
    naivebayes.main(directory='articles/', useTfIdf=x, useHispanic=True) # all documents we have
    naivebayes.main(directory='articles/', useTfIdf=x, useHispanic=False) # black and white only
    naivebayes.main(directory='articles-even/', useTfIdf=x, useHispanic=True) # all 3 same quantity
    naivebayes.main(directory='articles-noFox/', useTfIdf=x, useHispanic=False) # all 3 same quantity
    naivebayes.main(directory='articles-noBrit/', useTfIdf=x, useHispanic=False) # all 3 same quantity
