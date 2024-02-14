### Mage Homework

First rename `dev.env` to simply `.env`— this will _ensure_ the file is not committed to Git by accident, since it _will_ contain credentials in the future.

Then we build the container
```bash
docker-compose build
```

Then we start the Docker container (detached mode is optional):
```bash
docker-compose up -d
```

Navigate to http://localhost:6789 in your browser to access the Mage dashboard
(If you're deploying in a VM, remember to forward the port 6789 first)

For GCP we'll need to set up a service account (and it's corresponding key).
I used the one I made for the terraform part of week 1 homework.