from app.scraper.relevancy import is_relevant_title
import pytest

example_relevant_titles = [
    "Nicușor Dan, primar al Bucureștiului, a ieșit pe locul doi în primul tur",
    "George Simion a câștigat primul tur al alegerilor prezidențiale din România",
    "Cautăm un expert în domeniul geopolitica",
]

example_irrelevant_titles = [
    "Prințul William, mișcare strategică. Decizia luată poate reaprinde războiul cu Prințul...",
    "Mărirea și decăderea unei prietenii. Ce s-a întâmplat între David Beckham și Harry, după ce Meghan Markle a apărut în viața prințului",
    "Ei sunt cei trei concurenți care au reușit să impresioneze publicul în cea de-a doua semifinală Românii au talent și merg mai departe în Marea...",
]

@pytest.mark.parametrize("title", example_relevant_titles)
def test_relevant_titles_are_identified(title):
    assert is_relevant_title(title), f"Should identify as relevant: {title}"

@pytest.mark.parametrize("title", example_irrelevant_titles)
def test_irrelevant_titles_are_filtered(title):
    assert not is_relevant_title(title), f"Should identify as irrelevant: {title}"