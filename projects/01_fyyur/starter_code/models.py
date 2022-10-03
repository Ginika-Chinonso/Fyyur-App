from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String())
    website = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String())

    shows = db.relationship('Shows', backref='venue')

    def __repr__(self):
      return f"Venue {self.id} {self.name} {self.city}"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String())
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String())

    shows = db.relationship('Shows', backref='artist')

    def __repr__(self):
      return f"Artist {self.id} {self.name} {self.phone}"


class Shows(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.String())
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))

  def __repr__(self):
    return f"<Show {self.id} start_time: {self.start_time} artist_id: {self.artist_id} venue_id: {self.venue_id}>"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.