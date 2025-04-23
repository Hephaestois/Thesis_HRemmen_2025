For Viktoria: This file is for the text (and notes) I want to present for the article presentation on 3rd April. This presentation is in Dutch, so I will adhere to that. Excuse the language inconsistency, but I work across three devices/locations, so using Github is essential.

Skelet Artikelpresentatie:
- Introductie: Ik wil wat vertellen over modellen waarmee bewegingsgedrag van dieren, op individueel- en bevolkingsniveau, beschreven wordt. 
- Concept Random Walk in één dimensie
- 'Intermezzo': Hoe een Galton board precies de link tussen 1d en 2d bechrijft.
- Afleiding Random Walk -> Diffusiemodel. 
- Diffusie én Advectie: grafieken laten zien
- 2d-geval introduceren
- Conclusie: Herhalen wat besproken is, en herhalen welk soort organisme zich zo gedraagt

Tekst Artikelpresentatie:
# Introductie



# RW in één dimensie
Het concept van een random walk is gelukkig niet heel vergezocht. Het is niet altijd het geval dat wiskundige naamgeving per sé duidelijk is, maar voor een Random Walk is dat gelukkig wel het geval. Ik wil daarom een specifiek voorbeeld geven van de klassieke ééndimensionele Random Walk, en daarvoor beginnen we met een nummerlijn. Hierop kan een organisme met een kans l een stap naar links nemen, en kans r een stap naar rechts. Het is belangrijk om te benoemen dat l+r=1, dus "de kans om naar links óf rechts te gaan is 1', dus stilstaan is geen optie! 
Omdat we een fysisch model willen maken, introduceren we twee variabelen, namelijk de stapgrootte van een organisme, delta, en de staptijd tau. We doen dit, omdat we heel graag delta en tau tegelijk naar nul willen sturen, zodat we van deze discrete nummerlijn een continu iets kunnen maken. 
Als we met 'X_n' de plek van een organisme beschrijven op stap nummer n, kunnen we de kans-vergelijking voor een random walk opstellen, namelijk:
P(x,t) = rP(x-delta, t-tau) + lP(x+delta, t-tau).
Hier zien we dus dat de kans om op tijdstip t op locatie x te zijn, gelijk is aan: de kans dat je van links op x belandt, of van rechts op x belandt. 

Als we het tijdstip met één tau later nemen, komen we op de equivalente vergelijking:
P(x,t+tau) = rP(x-delta, t) + lP(x+delta, t).
Deze vergelijking (of, de analoge ervan in 2 dimensies) is de sleutel voor de rest van de analyse die in de paper gedaan wordt.

# Intermezzo: Galton Board
Straks gaan we de limiet nemen van tau en delta, en gaan we daarmee dus ook wat wiskunde moeten verdragen, maar voordat ik dat doe wil ik graag een heel mooie intuitie bieden voor wat er nou gaat gebeuren, en ik hoop dat aan het eind van dit intermezzo, de daaropvolgende afleiding onnodig zal zijn!

Ik wil jullie graag uitnodigen om na te denken aan de plek waar deze random-walker uitkomt na een bepaald aantal, zeg 12 stappen. We stellen eigenlijk de vraag, nadat we 12 keer willekeurig kiezen om naar links of naar rechts te gaan, waar belanden we dan? Het zal blijken dat Sir Francis Galton diezelfde vraag al stelde in 1874, en daartoe heeft hij het Galton Board bedacht. En dat werkt als volgt: [VIDEO]

En daar is hij! De distributie waarvan ik wil laten zien dat het een Random Walk in de limiet beschrijft!!
Voor de wiskundigen onder ons (specifiek diegenen die zich de centrale limietstelling nog herinneren), dit is een normale verdeling, en heeft dus, met bepaalde schaalfactoren, een vorm volgens e^-x². Als we dadelijk ons model in continue tijd hebben afgeleid, zullen we zien dat dit inderdaad een oplossing is!

(Verstreken tijd: 3 minuten)

# Afleiding: Random Walk naar Diffusiemodel
Nu wil ik graag iets harder maken dat deze Random Walk inderdaad afgeleid kan worden tot een diffusiemodel, als we maar de correcte limieten van tau en delta nemen. 
Voor de leken: laat het vooral even over je heen gaan, ik ben zo weer terug met veel relevanter materiaal.



# Uitleg over wat Diffusie en Advectie is (Vooral advectie)
Met dat gezegd te hebben, (flinke pil hè?), wil ik graag ook de leken uitnodigen hun aandacht terug te brengen naar het originele random-walk model. 
Ik heb het tot dusver gehad over diffusie, maar een belangrijke term die ook in het paper voorbij komt, is advectie. In essentie kun je over het 'midden' van een groep spreken als we het hebben over het massamiddelpunt van onze verdeling. Dit midden is natuurlijk niet stationair, maar voor het geval van de 1d random walk, hebben we al gezien dat de 'piek', ofwel het midden, van de verdeling van de populatie, zich eigenlijk niet verplaatst. Dat is precies het tegenovergestelde van advectie! Als er sprake is van advectie, is er dus een zekere verplaatsing van het massamiddelpunt te vinden. Dit representeert zich natuurlijk in de Random Walk door te stellen dat de kans naar links l en de kans naar rechts r niet meer hetzelfde zijn, en je dus vaker in een bepaalde richting een stap zult zetten, en dus is de 'gemiddelde' richting van de walk niet meer 0. Ik wil dit graag in wat grafieken zetten, zodat het effect op een collectief hiervan ook duidelijk wordt. 

We beginnen met een puur diffusief proces. Er is dus een bepaalde plek waar we alle organismen laten beginnen, in ons geval beginnen we op nul. Als we vervolgens de tijd laten variëren, zien we dat de bevolking zich uit begint te spreiden. Er is een hoge kans voor een organisme om zich in het midden te bevinden, en aan de randen zien we dat die kans klein is, maar wel toeneemt. Als we de tijd nog verder laten variëren, zien we dan de verdeling platter komt te liggen, en het proces zich voortzet. Merk wel op dat al deze tijd, dit proces symmetrisch was rond 0!

Als we nu een puur advectief model beschouwen, verwachten we dat de originele verdeling constant blijft, maar dat er dus een zekere verplaatsing zal zijn van de verdeling. Inderdaad, we zien dat de verdeling dezelfde vorm houdt, maar aan de wandel is gegaan. Nu in het derde en laatste plaatje, gaan we een model met een diffusieve en advectieve term bekijken. Als ik hem gewoon laat afspelen, zien we dat de bevolking zich dus uitspreidt, maar dat er ook een trend is in de beweging van de bevolking. Met deze twee parameters, de diffusieve en de advectieve parameter, kun je de ons model in zijn geheel beschrijven! Maar dit is slechts het 'simpele' 1d-geval. Als we het hebben over dieren die niet zwemmen of vliegen, is hen gedrag toch eerder twee-dimensioneel.  

# 2d - Random Walk
Daarom wil ik nog even met jullie speculeren over de 2d Random Walk. 


# Verwijzing waar het paper écht over gaat: verschillende methoden om complexere RW's om te zetten in PDE's
Alles dat ik jullie zojuist heb verteld, is in de paper eigenlijk 'introductie', grotendeels bestaande uit hoofdstuk 2.1-2.3. Die tekst is op aan het bouwen naar de 'Fully Anisotropic Advection-Diffusion Equations', of het FAAD model. ((2) laten zien). Maak je echt geen zorgen om deze te begrijpen, daarvoor had ik een college in plaats van een presentatie moeten mogen geven. Ik wil wel benoemen dat in dit model, de advectie én diffusie termen mogen afhangen van de tijd en ruimte waarin organismen zich in bevinden. Ook zijn onderliggende orientatie-gerichte informatie of informatie uit de omgeving in zekere zin gecodeerd in \mathcal{D}. Met orientatie-gerichte informatie, bedoel ik informatie die het best geformuleerd kan worden als 'Een rennend dier blijft rennen': het is waarschijnlijker dat een dier hetzelfde doet als een moment eerder, dan dat die opeens iets anders gaat doen. Zo voorspel ik, dat de meeste van jullie hier nog even blijven zitten, aangezien dat al zo is voor een halfuurtje. Zulke informatie is ook in D gecodeerd, en dit FAAD model is dus een heel descripte beschrijving van de omgeving waarin een organisme zich bevindt.

# Conclusie: Herhaling, uitnodiging, en opening vragenronde 
En met dat gezegd te hebben, wil ik graag een bondige samenvatting geven van wat we hebben behandeld. Eerst heb ik kort laten zien wat een random walk is, en waarom deze schaalt naar een soort advectie-diffusieproces. Vervolgens heb ik jullie meegenomen op een korte uitstap naar 2d-modellen, en hebben we afgesloten met de kern van de paper, die ik graag aan jullie wilde overbrengen. 
Ik dank jullie graag voor jullie aandacht, en open bij deze de vragenronde.


