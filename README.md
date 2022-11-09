# NCARDDatabase Setup

 1. Install Python, Docker Desktop and Docker Compose (which might be included).
 2. Clone this repo.
 3. Run `gen_secrets.py` in the `NCARDDatabase/secrets` folder in order to generate the necessary secret keys.
 4. Open a shell in the top-level `NCARDDatabase` directory.
 5. `docker compose build`
 6. `docker compose up`
 7. Wait for MySQL to initialise, if applicable.
    Look for `/usr/sbin/mysqld: ready for connections.`
 8. Open a shell inside the currently running `ncarddatabase-web-1` container, then run:
    * `python manage.py migrate`
    * `python manage.py collectstatic`
    * `python manage.py createsuperuser` - Set the username and password to whatever you like. The email address does not matter.
 9. Try navigating to http://localhost/, then log in with the username and password. You should see the dashboard of the app.
 
## To make code changes

1. **Create a new branch in Git.**
2. Modify/create/delete code files as necessary.
3. If the server is running, you must also modify `NCARDDatabase/NCARDDatabase/wsgi.py`, e.g. by adding or removing a blank line.
   This notifies the server to pick up the code changes.
4. When you've made a change, commit it (e.g. using GitHub Desktop) and push the branch.
5. Open a pull request with the new branch.
6. Notify Edward Giles and he will review the code.
 
## To stop the server (development)

1. Press Ctrl+C (not Command+C on Mac) to stop the server. Wait about 10 seconds.
2. Run `docker compose down`.

## To start the server (development)

1. Inside the `NCARDDatabase` directory, run `docker compose up`.

## Debugging tips

* Open a shell inside `ncarddatabase-web-1`, then run: `tail -f /var/log/apache2/error.log`
  It will show the last ten lines of the log file, and then live-update with any new errors the web server runs into.
* If you find any more good advice, add it using a pull request.

## To refresh the code running on the web server (production)

**WARNING:** Ensure the code on the main branch is fully working before running these commands.

1. SSH into the web server.
2. Run `sudo su` to achieve root access.
3. Run these commands as root, to pull the changes from GitHub:
```
cd ~/NCARDDatabase
git restore sites-available/ncard-database.conf
git pull
/bin/cp sites-available/ncard-database-prod.conf sites-available/ncard-database.conf
```
4. Run these commands as root, to restart the server using the new code. **This will cause the server to go offline temporarily.**
```
docker-compose down
docker-compose build
docker-compose up --detach
```