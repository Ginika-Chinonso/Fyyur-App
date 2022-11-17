#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate



# TODO: connect to a local postgresql database




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Importing the models from models.py
# with app.app_context:
from models import Venue, Artist, Shows


migrate = Migrate(app, db)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  all_venues = Venue.query.order_by(Venue.city, Venue.state).all()
  
  cities = db.session.query(Venue.city, Venue.state).order_by(Venue.city).distinct()


  res = []
  for venue in cities:
    res.append({
      "city": venue.city,
      "state": venue.state,
      "venues": []
    })
  for venue in all_venues:
    for x in res:
      if venue.city == x['city']:
        x['venues'].append({
          "id": venue.id,
          "name": venue.name,
        })

  return render_template('pages/venues.html', areas=res)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": Venue.query.filter(Venue.name.ilike('%' + request.form.get('search_term', '') + '%')).count(),
    "data": Venue.query.filter(Venue.name.ilike('%' + request.form.get('search_term', '') + '%')).all()
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  data = vars(venue)
  upcomingShows = Shows.query.join(Artist, Venue).add_columns(Artist.image_link.label('artist_image_link'), Artist.id.label('artist_id'), Shows.start_time.label('start_time')).filter(Shows.venue_id == venue_id, Shows.start_time > str(datetime.now())).all()
  pastShows = Shows.query.join(Artist, Venue).add_columns(Artist.image_link.label('artist_image_link'), Artist.id.label('artist_id'), Shows.start_time.label('start_time')).filter(Shows.venue_id == venue_id, Shows.start_time < str(datetime.now())).all()

  data['upcoming_shows'] = upcomingShows
  data['upcoming_shows_count'] = len(upcomingShows)
  data['past_shows'] = pastShows
  data['past_shows_count'] = len(pastShows)

  return render_template('pages/show_venue.html', venue= data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm(request.form)

  try:
    venue = Venue(
      name= form.name.data, 
      city= form.city.data, 
      state= form.state.data, 
      address= form.address.data, 
      phone= form.phone.data, 
      image_link= form.image_link.data, 
      genres= form.genres.data, 
      facebook_link= form.facebook_link.data, 
      website= form.website_link.data, 
      seeking_talent = form.seeking_talent.data,
      seeking_description= form.seeking_description.data
    )
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was successfully listed!')
  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    db.session.query(Venue).filter_by(venue_id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data= Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": Artist.query.filter(Artist.name.ilike('%' + request.form.get('search_term', '') + '%')).count(),
    "data": Artist.query.filter(Artist.name.ilike('%' + request.form.get('search_term', '') + '%')).all()
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  artist = Artist.query.get(artist_id)
  data = vars(artist)

  pastShows = Shows.query.join(Artist, Venue).add_columns(Venue.image_link.label('venue_image_link'), Venue.id.label('venue_id'), Shows.start_time.label('start_time')).filter(Shows.artist_id == artist_id, Shows.start_time < str(datetime.now())).all()

  upcomingShows = Shows.query.join(Artist).filter(Shows.artist_id == artist_id, Shows.start_time > str(datetime.now())).all()

  data['upcoming_shows'] = upcomingShows
  data['upcoming_shows_count'] = len(upcomingShows)
  data['past_shows'] = pastShows
  data['past_shows_count'] = len(pastShows)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist= Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  
  try:
    artist = Artist.query.get(artist_id)
    if form.name:
      artist.name = form.name.data,
    if form.city:
      artist.city= form.city.data, 
    if form.state:
      artist.state= form.state.data, 
    if form.phone:
      artist.phone= form.phone.data, 
    if form.genres:
      artist.genres= form.genres.data, 
    if form.website:
      artist.website= form.website_link.data,
    if form.facebook_link:
      artist.facebook_link= form.facebook_link.data, 
    if form.image_link:
      artist.image_link= form.image_link.data,
    if form.seeking_venue:
      artist.seeking_venue= form.seeking_venue.data 
    if form.seeking_description:
      artist.seeking_description= form.seeking_description.data

    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue= Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)

  try:
    venue = Venue.query.get(venue_id)
    if form.name:
      venue.name = form.name.data
    if form.city:
      venue.city= form.city.data
    if form.state:
      venue.state= form.state.data
    if form.address:
      venue.address= form.address.data 
    if form.phone:
      venue.phone= form.phone.data 
    if form.image_link:
      venue.image_link= form.image_link.data 
    if form.genres:
      venue.genres= form.genres.data 
    if form.facebook_link:
      venue.facebook_link= form.facebook_link.data
    if form.website:
      venue.website= form.website.data
    if form.seeking_talent:
      venue.seeking_talent = form.seeking_talent.data
    if form.seeking_description:
      venue.seeking_description= form.seeking_description.data

    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)

  try:
    artist = Artist(
      name= form.name.data, 
      city= form.city.data, 
      state= form.state.data, 
      phone= form.phone.data, 
      genres= form.genres.data, 
      website= form.website_link.data, 
      facebook_link= form.facebook_link.data, 
      image_link= form.image_link.data, 
      seeking_description= form.seeking_description.data
      )
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    db.session.rollback()
    flash('An error occured. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = db.session.query(Shows, Artist, Venue).filter(Shows.artist_id == Artist.id, Shows.venue_id == Venue.id).all()

  data = []

  for show in shows:
    item = {
      "venue_id": show[0].venue_id,
      "venue_name": show[2].name,
      "artist_id": show[0].artist_id,
      "artist_name": show[1].name,
      "artist_image_link": show[1].image_link,
      "start_time": show[0].start_time
      }
    data.append(item)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)

  try:
    show = Shows(
      artist_id= form.artist_id.data, 
      venue_id= form.venue_id.data, 
      start_time= form.start_time.data
      )

    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error   instead.
    # e.g., flash('An error occurred. Show could not be   listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/  flashing/
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(host='localhost')

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
