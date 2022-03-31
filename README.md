# tsoha-ravintolasovellus

Aineopintojen harjoitustyö: [Tietokantasovellus](https://hy-tsoha.github.io/materiaali/)

## Ravintolasovellus

Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

- [ ] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- [ ] Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat)
- [ ] Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita
- [ ] Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot
- [ ] Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana
- [ ] Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti
- [ ] Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion
- [ ] Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään

## Asennus

Kloonaa tämä projekti konellesi.  
Varmista, että sinulla on asennettuna [Python](https://www.python.org/).  
Varmista, että sinulla on asennettuna [PostgreSQL](https://www.postgresql.org/).

### venv

Projekti ajetaan Python -virtuaaliympäristössä.  
Avaa projektin kansio terminaalissa.  
Aja terminaalissa komento: `python -m venv venv`.  
Tämä luo kansioon uuden Python -virtuaaliympäristön.  
Käynnistä virtuaaliympäristö komennolla: `source/venv/bin/activate`

### Riippuvuudet

Virtuaaliympäristöön täytyy seuraavaksi asentaa projektin riippuvuudet.  
Aja terminaalissa komento: `pip install -r requirements.txt`.  
Nyt projektin riippuvuudet on asennettu.

### .env -tiedosto

Projekti käyttää ympäristömuuttujia konfigurointiin.
Lisää projektin juureen `.env` -niminen tiedosto.  
Kirjoita tiedostoon sisällöksi seuraavat avaimet, joihin korvaat <> -sisällön avaimen arvolla.

**Avaimet:**  
DATABASE*URL=[PostgreSQL connection string](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)
SECRET_KEY=\_satunnainen tekstijono*

Tiedosto näyttää lopuksi kutakuinkin tältä:

```
DATABASE_URL=postgresql:///roni
SECRET_KEY=supersalainenavain8fdsajrf78hgv
```

### Tietokanta

Projekti käyttää PostgreSQL -tietokantaa.  
Aja terminaalissa komento: `psql < schema.sql`.  
Nyt tietokanta on alustettu sovellusta varten.

### Käynnistys

Projektin alustamisen jälkeen, sen saa virtuaaliympäristössä käyntiin ajamalla komennon: `flask run`
