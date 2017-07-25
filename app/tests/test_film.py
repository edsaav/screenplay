import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
import film

SAMPLES = [
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sample1.txt')
]

def test_title():
    f = film.Film(SAMPLES[0])
    assert f.title == 'SAMPLE MOVIE'

def test_number_of_scenes():
    f = film.Film(SAMPLES[0])
    assert f.number_of_scenes() == 1

def test_characters():
    f = film.Film(SAMPLES[0])
    assert len(f.characters) == 3
