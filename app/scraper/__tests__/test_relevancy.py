from app.scraper.relevancy import is_relevant_title
import pytest

example_relevant_titles = [
    "Nicușor Dan, primar al Bucureștiului, a ieșit pe locul doi în primul tur",
    "George Simion a câștigat primul tur al alegerilor prezidențiale din România",
    "Ce crede cu adevărat Călin Georgescu despre Vladimir Putin. A spus asta înainte de a candida la președinție",
    "Câți bani au primit influencerii care l-au promovat pe Călin Georgescu pe TikTok",
    "Viktor Orban nu-l mai susține pe George Simion",
    "Alegeri prezidențiale și referendum național",
    "Ne alegem presedintele! Vezi declaratiile oamenilor politici!",
    "Nicușor Dan şi-a invitat susținătorii în Piața Victoriei. Organizatorul a precizat că mitingul este despre direcția țării",
    "Ce spune Nicușor Dan după ce a vorbit cu susținătorii lui George Simion: ”Îi înțeleg foarte bine”",
    "AUR se dezice de scrisorile care incitau la violență și abuz. ”Sunt contrafăcute, atribuite în mod fals”",
    "Nicuşor Dan: Voi lupta pentru o Românie în care copiii romi au aceleaşi şanse ca oricare alt copil",
    "Prima zi de campanie pentru prezidențiale: Simion a făcut o vizită în Londra, iar Nicușor Dan a participat la o ceremonie",
    "Ce spun ungurii despre rezultatul alegerilor prezidențiale din România. L-au descris pe George Simion într-un singur cuvânt",
    "Băsescu: Ar fi groaznic pentru România să avem un şef de galerie care ajunge preşedinte fără să fi practicat nicio meserie",
    "Rezultate alegeri prezidențiale 2025. Cum „și-au împărțit lumea” candidații la prezidențiale. Harta cu votul din Diaspora",
    "Când a mai pierdut alegerile candidatul de pe primul loc în primul tur. Șansele ca Nicușor Dan să ajungă la Cotroceni",
    "George Simion, întrebat dacă îl va numi premier pe Călin Georgescu: Da. Este angajamentul pe care mi l-am luat faţă de români",
    "Reacția lui Marcel Ciolacu după primele exit poll-uri: „Ponta e un om neserios. Dacă nu candida, Crin era pe primul loc”",
    "Ce înseamnă pentru economia României o depreciere a monedei naționale. Vor fi creșteri de prețuri pentru noi toți",

]

example_irrelevant_titles = [
    "Prințul William, mișcare strategică. Decizia luată poate reaprinde războiul cu Prințul...",
    "Mărirea și decăderea unei prietenii. Ce s-a întâmplat între David Beckham și Harry, după ce Meghan Markle a apărut în viața prințului",
    "Ei sunt cei trei concurenți care au reușit să impresioneze publicul în cea de-a doua semifinală Românii au talent și merg mai departe în Marea...",
    "WSJ: Kim Jong Un ar fi făcut „cadou” Rusiei 15.000 de muncitori. Condițiile extreme în care lucrează nord-coreenii",
    "Șoferiță de 22 de ani, grav rănită după ce a fost lovită de trenul care venea de la Vaslui",
    "Cod galben de furtuni, vânt puternic și grindină în 25 de județe. ANM anunță vreme rea în toată țara până joi. HARTĂ",
    "Horoscop săptămânal cu Cristina Demetrescu. Ce ne rezervă astrele între 5 și 11 mai 2025. Lecții, tensiuni și decizii mari",
    "Motivul pentru care a fost închisă de urgență Salina Praid. Avertismentul ISU",
    "Reacția șefului armatei ucrainene, după ce trupele sale ar fi fost gonite de ruși de pe frontul din Kursk: „Ca o surpriză”",
    "Trump și Erdogan, discuție „foarte productivă” despre războiul din Ucraina. Preşedintele SUA vrea să pună capăt conflictului",
    "Viciul fără de care mulți români nu-și pot închipui azi viața vine de la americani. Mesajul Ambasadei SUA",
    "Metoda prin care produsele „Made în China” evită taxele vamale din SUA. Tot mai mulți producători o folosesc",
    "Cod portocaliu de vijelii în mai multe județe, marţi seara. Care sunt zonele vizate de vreme extremă"
]

@pytest.mark.parametrize("title", example_relevant_titles)
def test_relevant_titles_are_identified(title):
    assert is_relevant_title(title), f"Should identify as relevant: {title}"

@pytest.mark.parametrize("title", example_irrelevant_titles)
def test_irrelevant_titles_are_filtered(title):
    assert not is_relevant_title(title), f"Should identify as irrelevant: {title}"