import csv
from SPARQLWrapper import SPARQLWrapper, JSON

# Formatter le person_id
def format_person_id(person_id):
    person_id_str = str(person_id)
    formatted_id = f"{person_id_str[:2]}/{person_id_str[2:]}"
    return formatted_id


# Construire l'URI complet pour la personne
def person_uri_id(person_id):
    formatted_id = format_person_id(person_id)
    person_uri = f"https://dblp.org/pid/{formatted_id}"
    return person_uri


# Fonction d'exécution des requêtes SPARQL
def sparql_query(query):
    sparql = SPARQLWrapper("https://sparql.dblp.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

# Rechercher le nom de la personne et renvoyer une valeur booléenne indiquant si elle existe
def query_author_name(person_id):
    person_uri = person_uri_id(person_id)
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE {{
      <{person_uri}> rdfs:label ?label .
    }}
    """
    results = sparql_query(query)
    
    if results["results"]["bindings"]:
        return True
    else:
        return False

def id_valide():
    valid_ids = []

    # Lire le fichier CSV original
    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(valid_ids) >= target_count:
                break
            person_id = row[0]
            # Vérifier si l'ID existe et peut obtenir son nom
            if len(person_id) >= 3 and int(person_id) >= 100 and query_author_name(person_id):
                valid_ids.append(person_id)

    # Écrire les IDs valides dans un nouveau fichier CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for person_id in valid_ids:
            writer.writerow([person_id])

    print(f"Écriture terminée, cleaned_person_id.csv contient {len(valid_ids)} IDs valides")

if __name__ == "__main__":
    target_count = 100000 # à modifier: le nombre de person_ids validées que vous voulez obtenir
    str_count = str(target_count)
    load_dblp_file = "dataset/name/of/your/file"# chercher le fichier dans le dossier dataset
    noeds_export = f"{load_dblp_file}_noeds.csv"
    input_file = f"noeds_edge/{noeds_export}" # à modifier
    output_file = f"noeds_valides/cleaned_person_id{str_count}.csv"
    id_valide()
