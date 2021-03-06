# tsoha-ravintolasovellus

Aineopintojen harjoitustyö: [Tietokantasovellus](https://hy-tsoha.github.io/materiaali/)  
Testaa sovellusta [Herokussa!](https://tsoha-2022-ravintolasovellus.herokuapp.com/)

```
Ylläpitäjän käyttäjätunnukset testausta varten:
Tunnus: admin
Salasana: 12345
```

## Ravintolasovellus

Sovelluksessa näkyy kartta Helsingin alueen ravintoloista. Sovelluksessa on myös lista ravintoloista arvosteluiden mukaisessa järjestyksessä. Ravintoloita klikkaamalla pääsee sen omalle sivulle. Ravintolan omalla sivulla on lisätietoa ravintolasta, sekä arvostelu-osio.

Sovellukseen pystyy luomaan käyttäjän. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä. Peruskäyttäjä pystyy jättämään yhden arvostelun per ravintola. Peruskäyttäjä pystyy myös poistamaan oman arvostelun ravintolalta. Ylläpitäjä pystyy jättämään yhden arvostelun per ravintola. Ylläpitäjä pystyy poistamaan kenen tahansa arvostelun ravintolalta. Ylläpitäjä pystyy myös luomaan uusia ryhmiä ja ravintoloita sovellukseen.

- [x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- [x] Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat)
- [x] Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita
- [x] Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot
- [x] Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana
- [x] Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti
- [x] Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion
- [x] Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään

## Asennus

Kloonaa tämä projekti konellesi.  
Varmista, että sinulla on asennettuna [Python](https://www.python.org/).  
Varmista, että sinulla on asennettuna [PostgreSQL](https://www.postgresql.org/).

### venv

Projekti ajetaan Python -virtuaaliympäristössä.  
Avaa projektin kansio terminaalissa.  
Aja terminaalissa komento: `python3 -m venv venv`  
Tämä luo kansioon uuden Python -virtuaaliympäristön.  
Käynnistä virtuaaliympäristö komennolla: `source venv/bin/activate`

### Riippuvuudet

Virtuaaliympäristöön täytyy seuraavaksi asentaa projektin riippuvuudet.  
Aja terminaalissa komento: `pip install -r requirements.txt`  
Nyt projektin riippuvuudet on asennettu.

### .env -tiedosto

Projekti käyttää ympäristömuuttujia konfigurointiin.
Lisää projektin juureen `.env` -niminen tiedosto.  
Kirjoita tiedostoon sisällöksi seuraavat avaimet, joihin kirjoitat = merkin jälkeen avaimen arvon.

**Avaimet:**  
DATABASE_URL=[PostgreSQL connection string](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)  
SECRET_KEY=satunnainen tekstijono

Tiedosto näyttää lopuksi kutakuinkin tältä:

```
DATABASE_URL=postgresql:///roni
SECRET_KEY=supersalainenavain8fdsajrf78hgv
```

### Tietokanta

Projekti käyttää PostgreSQL -tietokantaa.  
Aja terminaalissa komento: `psql < schema.sql`  
Nyt tietokanta on alustettu sovellusta varten.

### Käynnistys

Projektin alustamisen jälkeen, sen saa virtuaaliympäristössä käyntiin ajamalla komennon: `flask run`

## Julkaisu

Ohjeet projektin julkaisuun Heroku -alustalle.

### Heroku kirjautuminen

Asenna [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).  
Suorita komentoriviltä `heroku login` ja kirjaudu palveluun.

### Sovelluksen luonti

Luo uusi projekti komennolla: `heroku apps:create (nimi)`  
Liitä projektin git remote Herokuun: `heroku git:remote -a (nimi)`

### Tietokanta Herokussa

Lisää PostgreSQL tietokanta Herokuun: `heroku addons:create heroku-postgresql -a (nimi)`  
Aja alustuskomennot tietokannalle: `heroku psql -a (nimi) < schema.sql`

### Ympäristömuuttujat Herokussa

Lisää projektin ympäristömuuttujat Herokuun: `heroku config:set SECRET_KEY=(arvo) -a (nimi)`

### Projektin julkaisu

Poista riippuvuus `pkg-resources` requirements.txt -tiedostosta.  
Puske projekti Herokuun: `git push heroku main`
