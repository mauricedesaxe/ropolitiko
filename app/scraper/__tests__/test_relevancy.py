from app.scraper.relevancy import is_relevant_title
import pytest  # noqa: F401
import json
from pathlib import Path

# Minimum acceptable score (percentage of correct classifications)
MIN_SCORE_THRESHOLD = 80.0

def test_relevancy_score():
    """Test the relevancy classifier and track its performance"""
    # Calculate current score
    current_score_data = calculate_score()
    current_score = current_score_data["score"]
    
    # Load previous score
    previous_data = load_previous_score()
    previous_score = previous_data["score"] if previous_data else 0
    
    # Add timestamp to score data
    from datetime import datetime
    current_score_data["timestamp"] = datetime.now().isoformat()
    
    # Save current score only if it's different from previous
    if not previous_data or current_score != previous_score:
        save_current_score(current_score_data)
    
    # Print detailed results
    print("\nRelevancy classifier performance:")
    print(f"Relevant titles: {current_score_data['relevant_correct']}/{current_score_data['relevant_total']}")
    print(f"Irrelevant titles: {current_score_data['irrelevant_correct']}/{current_score_data['irrelevant_total']}")
    print(f"Overall score: {current_score}%")
    
    if previous_data:
        print(f"Previous score: {previous_score}%")
        
    # Assert that score meets minimum threshold
    assert current_score >= MIN_SCORE_THRESHOLD, f"Score {current_score}% is below minimum threshold of {MIN_SCORE_THRESHOLD}%"
    
    # Assert that score has improved or stayed the same compared to previous
    if previous_data:
        assert current_score >= previous_score, f"Score has decreased from {previous_score}% to {current_score}%"

# Path to store historical scores
SCORES_FILE = Path("app/scraper/__tests__/latest_relevancy_score.json")

def calculate_score():
    """Calculate the percentage of correctly classified titles"""
    relevant_correct = sum(1 for title in example_relevant_titles if is_relevant_title(title))
    irrelevant_correct = sum(1 for title in example_irrelevant_titles if not is_relevant_title(title))
    
    total_titles = len(example_relevant_titles) + len(example_irrelevant_titles)
    total_correct = relevant_correct + irrelevant_correct
    
    return {
        "score": round((total_correct / total_titles) * 100, 1),
        "relevant_correct": relevant_correct,
        "relevant_total": len(example_relevant_titles),
        "irrelevant_correct": irrelevant_correct,
        "irrelevant_total": len(example_irrelevant_titles)
    }

def load_previous_score():
    """Load previous score from the JSON file"""
    if not SCORES_FILE.exists():
        return None
    
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def save_current_score(score_data):
    """Save the current score to the JSON file"""
    # Create directory if it doesn't exist
    SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Save only the latest score
    with open(SCORES_FILE, 'w') as f:
        json.dump(score_data, f, indent=2)


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
    "Guvernul României a aprobat noul buget pentru anul fiscal 2025",
    "Inflația în România a scăzut sub 3% pentru prima dată în ultimii trei ani",
    "Parlamentul a votat noua lege a pensiilor. Ce se schimbă pentru pensionari",
    "Ministrul Economiei anunță noi investiții străine în sectorul industrial românesc",
    "Protestele fermierilor români continuă la București. Cer subvenții mai mari",
    "BNR a decis menținerea dobânzii de referință. Ce impact are asupra economiei",
    "Alegeri locale 2025: Cine sunt candidații pentru primăriile marilor orașe",
    "Coaliția de guvernare se destramă după dispute pe tema reformei fiscale",
    "Președintele Iohannis critică decizia CCR privind legea securității naționale",
    "România va primi fonduri suplimentare de la UE pentru infrastructura de transport",
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
    "Cod portocaliu de vijelii în mai multe județe, marţi seara. Care sunt zonele vizate de vreme extremă",
    "Accident grav pe DN1: trei mașini implicate și cinci persoane rănite",
    "Descoperire arheologică importantă în județul Constanța. Ce au găsit cercetătorii",
    "Filmul românesc premiat la Cannes va avea premiera națională luna viitoare",
    "Echipa națională de handbal feminin s-a calificat în semifinalele Campionatului European",
    "Incendiu puternic la un centru comercial din Iași. Pompierii intervin cu mai multe autospeciale",
    "Studiu: Românii petrec în medie 6 ore pe zi pe rețelele sociale",
    "Alertă meteo: val de căldură extremă în sudul țării în următoarele zile",
    "Cazul fetiței dispărute din Botoșani ia o întorsătură neașteptată. Ce au descoperit anchetatorii",
    "Noul film Marvel a doborât recorduri de box office în România în primul weekend",
    "Medicii de familie anunță că vor intra în grevă. Care sunt revendicările",
    "Festivalul Untold 2025 anunță primii artiști internaționali care vor urca pe scenă",
]