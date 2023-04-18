# Moni Challenge
Technical test for Python Developer job.

## Run Locally

Clone the project.
```bash
git clone https://github.com/facuvegaa/moni_challenge.git
```

Go to the project directory.
```bash
cd moni_challenge
```

Build images from the application and database.
```bash
docker-compose build
```

Run the generated images.
```bash
docker-compose up
```

CTRL+C to stop and run the migrations.
```bash
docker-compose run web python manage.py migrate
```

Create the admin user
```bash
docker-compose run web python manage.py createsuperuser
```

Run the generated images again.
```bash
docker-compose up
```

## Tech Stack

**Language:**
- Python (Django)

**Database:**
- PostgresSQL

**Others:**
- Docker Compose
- Pre-Commit

## Author

- [@FacundoVega](https://github.com/facuvegaa)
