from app import db

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String())

    shows = db.relationship('Shows', backref='venue')

    def __repr__(self):
      return f"Venue {self.id} {self.name} {self.city}"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    shows = db.relationship('Shows', backref='artist')

    def __repr__(self):
      return f"Artist {self.id} {self.name} {self.phone}"


class Shows(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime())
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

  def __repr__(self):
    return f"<Show {self.id} start_time: {self.start_time} artist_id: {self.artist_id} venue_id: {self.venue_id}>"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.