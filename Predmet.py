## klasa Item predstavlja predmete

class Item(object):
    
    properties_number = 0                           ## broj svojstava, odnosno 'tezina' predmeta
        
    def __init__(self, name, value, *properties):   ## konstruktor koji za svaki predmet prima njegovo ime, vrijednost te polje u kojem su sadrzane sve tezine predmeta

            global properties_number
            properties_number = len(properties)

            self.name = name
            self.value = value

            ## prolazimo kroz dane tezine te za i-tu tezinu iz polja properties dodajemo atribut property{i} s pripadnom vrijednosti
            ## npr. za properties_number = 3, svaki ce objekt klase Item imati atribute property1, property2, property3
            for indeks, weight in enumerate(properties):
                setattr(self, 'property{}'.format(indeks + 1), int(weight))

    ## predmete sortiramo po omjeru njihove vrijednosti i ukupne tezine
    def ratio(self):
        suma = 0

        for i in range(properties_number):
            suma += getattr(self, 'property{}'.format(i+1))
        
        return self.value / suma

    ## overloadamo operator == da bismo mogli usporedivati objekte klase Item
    def __eq__(self, another_item):
        result = self.name == another_item.name and self.value == another_item.value    ## predmeti moraju imati ista imena i vrijednosti
        
        ## vrijednosti svih tezina moraju biti jednake
        for i in range (properties_number):
            result = getattr(self, 'property{}'.format(i + 1)) == getattr(another_item, 'property{}'.format(i + 1)) and result

        return result