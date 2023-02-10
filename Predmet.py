## klasa Item koja predstavlja Predmet
class Item(object):

    properties_number = 0  ## broj svojstava, odnosno 'težina' predmeta

    def __init__(self, name, value, *properties):  ## konstruktor koji za svaki predmet prima njegovo ime, vrijednost te polje u kojem je sadržano properties_number težina
        
        global properties_number
        properties_number = len(properties)

        self.name = name
        self.value = value

        ## prolazimo kroz dane tezine te za i-tu tezinu iz polja properties predmetu dodajemo atribut property{i} s pripadnom vrijednosti
        ## npr za properties_number = 3 svaki ce objekt klase Item imati atribute property1, property2, property3
        for ind, val in enumerate(properties):
            setattr(self, 'property{}'.format(ind+1), int(val)) 

    ## not sure hocemo li trebati ovu operaciju
    ## def ratio(self):
    ##    sum = 0
    ##    for i in range(properties_number):
    ##        sum += getattr(self, 'property{}'.format(i+1))
    ##    return self.value / sum

    ## overloadamo operator == da bismo metodu usporedivanja dva predmeta
    def __eq__(self, item2):
        result = self.name == item2.name and self.value == item2.value ## predmeti moraju imati ista imena i vrijednosti
        ## sva svojstva predmeta, odnosno sve tezine moraju biti jednake
        for i in range(properties_number):
            result = result and getattr(self, 'property{}'.format(i+1)) == getattr(item2, 'con{}'.format(i+1))
        return result

