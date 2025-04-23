
None selected

Skip to content
Using Gmail with screen readers
1 of 4,512
(no subject)
Inbox
Hazel Remmen <jurian.remmen@gmail.com>
	
16:25 (0 minutes ago)
	
to me
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
Hallo allemaal! Vandaag wil ik jullie iets vertellen over de Random Walk. De Random Walk is een wiskundig model dat onder andere het gedrag van de aandelenmarkt, de beweging van deeltjes, maar ook de beweging van dieren kan beschrijven. In het artikel, waar ik jullie zo over wil vertellen, wordt precies dit laatste gedaan. Er wordt een model voorgesteld voor het beschrijven van dierlijk gedrag, in deze paper specifiek de manier waarop cellen zich bewegen op een bepaalde structuur, en hoe zeeschildpadden in de goede zeestromen blijven zwemmen. Ik hoop dat ik aan het eind van deze presentatie jullie heb kunnen uitleggen wat een Random Walk precies is, en waarom de wiskunde niet alleen mooi en elegant is, maar ook nog eens breed toepasbaar is. Om jullie daarvan te overtuigen, zal ik eerst moeten uitleggen wat een random walk ís.


# RW in één dimensie
Het concept van een random walk is gelukkig niet heel vergezocht. Het is niet altijd het geval dat wiskundige naamgeving per sé duidelijk is, maar voor een Random Walk is dat gelukkig wel het geval. Ik wil daarom een specifiek voorbeeld geven van de klassieke ééndimensionele Random Walk, en daarvoor beginnen we met een nummerlijn. Hierop kan een organisme met een kans l een stap naar links nemen, en kans r een stap naar rechts. Het is belangrijk om te benoemen dat l+r=1, dus "de kans om naar links óf rechts te gaan is 1', dus stilstaan is geen optie!
Omdat we een fysisch model willen maken, introduceren we twee variabelen, namelijk de stapgrootte van een organisme, delta (dat is dus de markeringen die we al de hele tijd op de assen zien), en de staptijd tau. We doen dit, omdat we heel graag delta en tau tegelijk naar nul willen sturen, zodat we van deze discrete nummerlijn een continu iets kunnen maken.
Als we met 'p(x,t)' kans dat en organisme zicht bevindt op plaats x op 'tijd' t, kunnen we de kans-vergelijking voor een random walk opstellen, namelijk:
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
Ik ben bang dat ik dit gedeelte grotendeels voor de wiskundigen onder ons besluit te presenteren, maar ik vind het belangrijk om de wiskundige onderbouwing aan het licht te brengen. Als je er niets van begrijpt, is dat helemaal okay! Bovendien wil ik even benoemen: ik heb het tot dusver slechts over diffusiemodellen gehad. We gaan een extra advectieterm zien in het model dat we gaan afleiden, en wát advectie precies is, vertel ik na de afleiding.

Om de afleiding te beginnen, moeten we eerst een aantal Taylorreeksen ontwikkelen. Het doel is om overal functies in p(x,t), en afgeleides daarvan te krijgen, zodat we termen kunnen wegstrepen en een partiële differentiaalvergelijking overhouden. We gaan de taylorreeks in t tot twee termen ontwikkelen, dat ziet er zo uit, en de taylorreeks in x gaan we tot drie termen ontwikkelen. De rest van de termen noteren we met deze 'hogere orde termen', termen die even snel als \tau^2 of \delta^3 groeien. Als we dit allemaal substitueren, krijgen we een heel uitgebreide vergelijking! Maar, we zien veel termen in p, dus laten we alles herordenen in termen van afgeleides van p. Dat ziet er dan zo uit: [herorden]

Wat we nu zien is dat heel veel mooi gaat wegvallen. De termen in p zijn opgeteld nul, dus die strepen we weg. De termen voor p_x kunnen we allemaal samentrekken, om te bereiken: [G], en de termen voor p_xx tellen op naar \delta/2. Nu kunnen we links en rechts delen door \tau, en zijn we bijna klaar. Ik heb het al de hele presentatie over 'delta' en 'tau' die goed schalen. Dit is precies de stap waar ik dan op doel. Voor het model om 'logisch' te zijn, vereisen we dat \delta en \tau op zó'n manier naar nul gaan, dat a=... en d=... bestaan. Als één van deze twee termen nul is, krijg je een puur diffusie of puur advectiemodel. Als ze allebei niet nul zijn, dan krijg je een advectie-diffusiemodel.

# Uitleg over wat Diffusie en Advectie is (Vooral advectie)
Met dat gezegd te hebben, (flinke pil hè?), wil ik graag ook de leken uitnodigen hun aandacht terug te brengen naar het originele random-walk model.
Ik heb het tot dusver gehad over diffusie, maar een belangrijke term die ook in het paper voorbij komt, is advectie. In essentie kun je over het 'midden' van een groep spreken als we het hebben over het massamiddelpunt van onze verdeling. Dit midden is natuurlijk niet stationair, maar voor het geval van de 1d random walk, hebben we al gezien dat de 'piek', ofwel het midden, van de verdeling van de populatie, zich eigenlijk niet verplaatst. Dat is precies het tegenovergestelde van advectie! Als er sprake is van advectie, is er dus een zekere verplaatsing van het massamiddelpunt te vinden. Dit representeert zich natuurlijk in de Random Walk door te stellen dat de kans naar links l en de kans naar rechts r niet meer hetzelfde zijn, en je dus vaker in een bepaalde richting een stap zult zetten, en dus is de 'gemiddelde' richting van de walk niet meer 0. Ik wil dit graag in wat grafieken zetten, zodat het effect op een collectief hiervan ook duidelijk wordt.

We beginnen met een puur diffusief proces. Er is dus een bepaalde plek waar we alle organismen laten beginnen, in ons geval beginnen we op nul. Als we vervolgens de tijd laten variëren, zien we dat de bevolking zich uit begint te spreiden. Er is een hoge kans voor een organisme om zich in het midden te bevinden, en aan de randen zien we dat die kans klein is, maar wel toeneemt. Als we de tijd nog verder laten variëren, zien we dan de verdeling platter komt te liggen, en het proces zich voortzet. Merk wel op dat al deze tijd, dit proces symmetrisch was rond 0!

Als we nu een puur advectief model beschouwen, verwachten we dat de originele verdeling constant blijft, maar dat er dus een zekere verplaatsing zal zijn van de verdeling. Inderdaad, we zien dat de verdeling dezelfde vorm houdt, maar aan de wandel is gegaan. Nu in het derde en laatste plaatje, gaan we een model met een diffusieve en advectieve term bekijken. Als ik hem gewoon laat afspelen, zien we dat de bevolking zich dus uitspreidt, maar dat er ook een trend is in de beweging van de bevolking.

Met deze twee parameters, de diffusieve en de advectieve parameter, kun je het model dus in zijn geheel beschrijven! Maar dit is slechts het 'simpele' 1d-geval. Als we het hebben over dieren die niet zwemmen of vliegen, is hen gedrag toch eerder twee-dimensioneel.  

# 2d - Random Walk
Daarom wil ik jullie nog iets vertellen over de 2d Random Walk. We hebben het daarnet over een ééndimensionele RW gehad, en jullie zullen je vast kunnen voorstellen hoe het twee-dimensionele geval eruit ziet. De wiskunde van de random walk is in principe niet meer zo interessant om hier te presenteren, maar ik wil eigenlijk wel een visuele introductie, (of intuitie), laten zien waarom er weer sprake is van een advectie-diffusie-probleem, als we correct onze ruimte- en tijds-stapgroote schalen.

Laten we even kijken naar drie willekeurig gegenereerde twee-dimensionele Random Walks. Ik heb drie simulaties gedaan, met elk een kans van 0.25 om naar boven, onder, links óf rechts te gaan. Dus gelijke kans in alle richtingen. Let wederom op: stilstaan is geen optie!

Op de eerste zien we één loper die 2000 stappen heeft gezet. Het is even het benoemen waard dat ik elk lijnstukje met 50% doorzichtigheid teken. Als een lijnstuk dus donkerder is, is het minder vaak belopen. Dat kan, omdat over je eigen stappen teruglopen niet een 'illegale' actie is. Als we doorkijken naar de tweede afbeelding, zien we dat een loper die 10.000 stappen heeft gezet. We zien nu het eerste schaalverschijnsel. Het lijkt alsof de stappen die de loper neemt niet meer 'discreet' zijn, maar meer op Brownian motion begint te lijken. De invloeden van links, rechts, omhoog en omlaag zouden net zo goed uniform verdeeld kunnen zijn over alle richtingen in het vlak. In de laatste afbeelding, met 100.000 stappen, is dit het duidelijkst. In zekere zin is de 'resolutie' zo hoog geworden dat individuele stappen eigenlijk niet meer te onderscheiden zijn.

We hebben dus een vermoeden dat er weer een zekere schaling komt als we kleinere en kleinere stapjes in tijd en ruimte nemen. Dit maakt dan een verdeling, en laten we kijken wat die zal zijn!

In de afbeelding die je nu ziet, hebben 10 lopers elk een walk van 500 stappen gemaakt, beginnend uit hetzelfde punt (0, 0). Wat je ziet is dat ze eigenlijk allemaal een beetje hun eigen kant opgaan, en dat het totaalbeeld wel uitschieters heeft, maar dat er een zekere concentratie van massa is rond (0,0), omdat het blijkbaar waarschijnlijker is dat je daar in de buurt blijft, dan dat je een voorkeur hebt voor één richting.

In de volgende afbeelding, hebben 100 lopers elk 2000 stappen gezet. En nu zien we eigenlijk al duidelijk wat ik wil laten zien: in de limiet krijgen we een 2d-normale verdeling. De derde afbeelding heeft 1000 lopers met elk 10.000 stappen, het beeld dat ik wil schetsen is hopelijk wel duidelijk.

Een leuke laatste vraag die we kunnen stellen is: wat als de kans om een bepaalde richting op te lopen niet precies 0.25 is? Voor de mensen die die vraag hadden heb ik goed nieuws, want die heb ik ook gemaakt!

Links zien we dus nogsteeds het geval van 1000 lopers, met 10.000 stappen elk. Dat blijft onveranderd voor de volgende plaatjes. Als we de kans op een stap naar rechts met één procent hoger maken, dus 0.26 in plaats van 0.25, en we verlagen de kans om naar links te gaan naar 0.24, zodat de kansen alsnog optellen naar 1, dan krijgen we het volgende:
We zien nu dat advectiegedrag van een dimensie terug in twee dimensies! precies zoals we hoopten.

Laten we dat nog een keer doen, dus nog een extra procent kans om naar rechts te gaan, en:
[volgend plaatje]
Nou, van aesthetische waarde heeft het onderzoek in mijn mening geen tekort.
Maar van enkel aesthetiek moeten we het niet hebben. Kan dit model eigenlijk wel de complexe 'echte' wereld coderen??

# Verwijzing waar het paper écht over gaat: verschillende methoden om complexere RW's om te zetten in PDE's
[Nou, ] Alles dat ik jullie zojuist heb verteld, is in de paper eigenlijk 'introductie', grotendeels bestaande uit hoofdstuk 2.1-2.3. Die tekst is op aan het bouwen naar de afleiding van het 'Fully Anisotropic Advection-Diffusion Equations', of het FAAD model. ((2) laten zien). Maak je echt geen zorgen om deze te begrijpen, daarvoor had ik een volwaardig college in plaats van een presentatie moeten mogen geven. Ik wil wel benoemen dat in dit model, de advectie én diffusie termen mogen afhangen van de tijd en ruimte waarin organismen zich in bevinden. Vandaar dat we a(x,t) en D(x,t) schrijven. Ook zijn onderliggende orientatie-gerichte informatie of informatie uit de omgeving in zekere zin gecodeerd in \mathcal{D}. Met orientatie-gerichte informatie, bedoel ik informatie die het best geformuleerd kan worden als 'Een rennend dier blijft rennen': het is waarschijnlijker dat een dier hetzelfde doet als een moment eerder, dan dat die opeens iets anders gaat doen. Zo voorspel ik, dat de meeste van jullie hier nog even blijven zitten, aangezien dat al zo is voor het recente verleden. Zulke informatie is ook in D gecodeerd, en dit FAAD model is dus een heel descripte beschrijving van de omgeving waarin een organisme zich bevindt, en hoe dat organisme zich doorsnee gedraagt.

# Conclusie: Herhaling, uitnodiging, en opening vragenronde
En met dat gezegd te hebben, wil ik graag een bondige samenvatting geven van wat we hebben behandeld. Eerst heb ik kort laten zien wat een random walk is, en waarom deze schaalt naar een soort advectie-diffusieproces. Vervolgens heb ik jullie meegenomen op een korte uitstap naar 2d-modellen, en hebben we afgesloten met de kern van de paper, die ik graag aan jullie wilde overbrengen.
Ik dank jullie graag voor jullie aandacht, en open bij deze de vragenronde.




	
