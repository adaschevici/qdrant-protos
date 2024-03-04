## I have started a set of notes as I dig into Qdrant vector database. I hope time allows me to maintain these updated without breaking backwards changes.

To run these you need to create a python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# I added poetry for easier dependency management and update flow
poetry install
# you will most likely want to spin up a qudrant docker instance to play with
docker-compose up
```

Then you can run the notebooks with jupyter

```bash
jupyter notebook
```
