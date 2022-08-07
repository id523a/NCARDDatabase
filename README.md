# NCARDDatabase Setup

 1. Install Docker Desktop and Docker Compose (which might be included).
 2. Clone this repo.
 3. Open a shell in the top-level `NCARDDatabase` directory.
 4. `docker compose build`
 5. `docker compose up`
 6. Wait for MySQL to initialise, if applicable.
    Look for `/usr/sbin/mysqld: ready for connections.`
 7. Try navigating to http://localhost:8000. You should see a success page from Django.
 8. Open a shell inside the currently running `ncarddatabase-web-1` container, then run:
    * `python manage.py migrate`
    * `python manage.py collectstatic`
    * `python manage.py createsuperuser` - Set the username and password to whatever you like. The email address does not matter.
 9. Try navigating to http://localhost:8000/admin, then log in with the username and password.
 
## To stop the server

1. Press Ctrl+C (not Command+C on Mac) to stop the server. Wait about 10 seconds.
2. Run `docker compose down`.

## To start the server

1. Inside the `NCARDDatabase` directory, run `docker compose up`.