import json
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

# Rechercher le nom de la personne et renvoyer un dictionnaire de la personne
def query_author_name(person_id):
    person_uri = person_uri_id(person_id)
    query = f"""
    PREFIX dblp: <https://dblp.org/rdf/schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?label
    WHERE {{
      <{person_uri}> rdfs:label ?label .
    }}
    """
    results = sparql_query(query)
    
    if results["results"]["bindings"]:
        label = results["results"]["bindings"][0]["label"]["value"]
        formatted_id = format_person_id(person_id)
        return {f"{person_uri}": {"nom": label, "elementID": f"{formatted_id}"}}
    else:
        return None

# Rechercher tous les articles d'un auteur spécifique
def fetch_author_articles(person_id):
    person_uri = person_uri_id(person_id)
    query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dblp: <https://dblp.org/rdf/schema#>

        SELECT ?article ?articleTitle ?bibtexType ?doi ?publishedInStream ?yearOfPublication ?pagination ?publishedAsPartOf
        WHERE {{
          ?article dblp:authoredBy <{person_uri}> .
          
          OPTIONAL {{ ?article dblp:title ?articleTitle . }}
          OPTIONAL {{ ?article dblp:doi ?doi . }}
          OPTIONAL {{ ?article dblp:publishedInStream ?publishedInStream . }}
          OPTIONAL {{ ?article dblp:yearOfPublication ?yearOfPublication . }}
          OPTIONAL {{ ?article rdf:type ?bibtexType . FILTER(?bibtexType != <https://dblp.org/rdf/schema#Publication>) }}
          OPTIONAL {{ ?article dblp:pagination ?pagination . }}
          OPTIONAL {{ ?article dblp:publishedAsPartOf ?publishedAsPartOf . }}
        }}
    """
    results = sparql_query(query)
    
    articles = []
    for result in results["results"]["bindings"]:
        article = {
            "article_url": result["article"]["value"],
            "title": result.get("articleTitle", {}).get("value", None),
            "article_Type": result.get("bibtexType", {}).get("value", None),
            "ee": result.get("doi", {}).get("value", None),
            "conf_journal_id": result.get("publishedInStream", {}).get("value", None),
            "article_pubyear": result.get("yearOfPublication", {}).get("value", None),
            "pages": result.get("pagination", {}).get("value", None),
            "proceeding_id": result.get("publishedAsPartOf", {}).get("value", None)
        }
        articles.append(article)
    
    return articles

# Rechercher des informations spécifiques sur le type (actes de conférence)
def fetch_inproceedings_info(proceeding_id):
    query = f"""
    PREFIX dblp: <https://dblp.org/rdf/schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>

    SELECT ?title ?isbn ?listedOnTocPage ?yearOfPublication ?publishedBy
    WHERE {{
      <{proceeding_id}> dblp:title ?title .
      OPTIONAL {{ <{proceeding_id}> dblp:isbn ?isbn . }}
      OPTIONAL {{ <{proceeding_id}> dblp:listedOnTocPage ?listedOnTocPage . }}
      OPTIONAL {{ <{proceeding_id}> dblp:yearOfPublication ?yearOfPublication . }}
      OPTIONAL {{ <{proceeding_id}> dblp:publishedBy ?publishedBy . }}
    }}
    """
    results = sparql_query(query)

    proceeding_info = {}
    for result in results["results"]["bindings"]:
        proceeding_info = {
            "title": result.get("title", {}).get("value", None),
            "isbn": result.get("isbn", {}).get("value", None),
            "listedOnTocPage": result.get("listedOnTocPage", {}).get("value", None),
            "yearOfPublication": result.get("yearOfPublication", {}).get("value", None),
            "publishedBy": result.get("publishedBy", {}).get("value", None)
        }
    return proceeding_info

# Rechercher des informations spécifiques sur le type (journal)
def fetch_journal_info(conf_journal_id):
    query = f"""
    PREFIX dblp: <https://dblp.org/rdf/schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?label ?iso4 ?issn 
    WHERE {{
      <{conf_journal_id}> rdfs:label ?label .
      OPTIONAL {{ <{conf_journal_id}> dblp:iso4 ?iso4 . }}
      OPTIONAL {{ <{conf_journal_id}> dblp:issn ?issn . }}
    }}
    """
    results = sparql_query(query)
    
    journal_info = {}
    for result in results["results"]["bindings"]:
        journal_info = {
            "label": result.get("label", {}).get("value", None),
            "iso4": result.get("iso4", {}).get("value", None),
            "issn": result.get("issn", {}).get("value", None)
        }
    return journal_info

def fetch_book_info(article_url):
    query = f"""
    PREFIX dblp: <https://dblp.org/rdf/schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?label ?isbn ?publishedBy ?yearOfPublication
    WHERE {{
      <{article_url}> rdfs:label ?label .
      OPTIONAL {{ <{article_url}> dblp:isbn ?isbn . }}
      OPTIONAL {{ <{article_url}> dblp:publishedBy ?publishedBy . }}
      OPTIONAL {{ <{article_url}> dblp:yearOfPublication ?yearOfPublication . }}
    }}
    """
    results = sparql_query(query)

    book_info = {}
    for result in results["results"]["bindings"]:
        book_info = {
            "label": result.get("label", {}).get("value", None),
            "isbn": result.get("isbn", {}).get("value", None),
            "publishedBy": result.get("publishedBy", {}).get("value", None),
            "yearOfPublication": result.get("yearOfPublication", {}).get("value", None)
        }
    return book_info

# Rechercher des informations sur la conférence
def fetch_conference_info(conf_journal_id):
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dblp: <https://dblp.org/rdf/schema#>

    SELECT ?title
    WHERE {{
      <{conf_journal_id}> rdfs:label ?title .
    }}
    """
    results = sparql_query(query)

    conference_info = {}
    if results["results"]["bindings"]:
        conference_info = {
            "title": results["results"]["bindings"][0].get("title", {}).get("value", None)
        }
    return conference_info

# Rechercher le nom et l'identifiant de l'auteur
def query_author_name_from_uri(author_uri):
    query = f"""
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?label
    WHERE {{
      <{author_uri}> rdfs:label ?label .
    }}
    """
    results = sparql_query(query)
    
    author_info = {}
    if results["results"]["bindings"]:
        author_info = {
            "label": results["results"]["bindings"][0].get("label", {}).get("value", None)
        }
    return author_info

# Rechercher les co-auteurs de l'article/livre
def fetch_authors(article_uri):
    query = f"""
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dblp: <https://dblp.org/rdf/schema#>

    SELECT ?author
    WHERE {{
      <{article_uri}> dblp:authoredBy ?author .
    }}
    """
    results = sparql_query(query)

    authors = []
    for result in results["results"]["bindings"]:
        author_uri = result["author"]["value"]
        author_info = query_author_name_from_uri(author_uri)
        if author_info:
            authors.append(author_info)
    
    return authors

def fetch_editors(article_uri):
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dblp: <https://dblp.org/rdf/schema#>

    SELECT ?editor
    WHERE {{
      <{article_uri}> dblp:editedBy ?editor .
    }}
    """
    results = sparql_query(query)
    
    editors = []
    for result in results["results"]["bindings"]:
        editor_uri = result["editor"]["value"]
        editor_info = query_author_name_from_uri(editor_uri)
        if editor_info:
            editors.append(editor_info)
    return editors
    
def read_person_ids_from_csv(csv_file):
    person_ids = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # S'assurer que la ligne n'est pas vide
                person_ids.append(row[0])  # La structure du fichier CSV est une seule colonne person_id
    return person_ids

def main_generate():
    DBLP_dico = {}

    # Lire la liste des person_id à partir du fichier CSV
    
    person_ids = read_person_ids_from_csv(csv_file)

    for person_id in person_ids:
        person_uri = person_uri_id(person_id)
        author_info = query_author_name(person_id)

        if author_info:
            DBLP_dico[person_uri] = author_info[person_uri]
            DBLP_dico[person_uri]["proceeding_journal_article"] = []
            DBLP_dico[person_uri]["book"] = []

            articles = fetch_author_articles(person_id)
            for article in articles:
                article_url = article["article_url"]
                article_type = article["article_Type"]

                if article_type == 'https://dblp.org/rdf/schema#Inproceedings':
                    proceeding_id = article["proceeding_id"]
                    proceeding = fetch_inproceedings_info(proceeding_id)
                    proceeding_article = {
                        article_url: {
                            'title': article["title"],
                            'pages': article["pages"],
                            'year': article["article_pubyear"],
                            'ee': article["ee"],
                            'proceeding_id': proceeding_id,
                            'url': article_url,
                            'proceedings': {
                                'proceeding_id': proceeding_id,
                                'title': proceeding.get("title"),
                                'isbn': proceeding.get("isbn"),
                                'ee': proceeding.get("doi"),
                                'year': proceeding.get("yearOfPublication"),
                                'editors': fetch_editors(proceeding_id)
                            },
                            'publisher': {
                                'name': proceeding.get("publishedBy")
                            },
                            'conference': {
                                article["conf_journal_id"]: {
                                    'title': fetch_conference_info(article["conf_journal_id"])
                                }
                            },
                            'authors': fetch_authors(article_url)
                        }
                    }
                    DBLP_dico[person_uri]["proceeding_journal_article"].append(proceeding_article)

                elif article_type == 'https://dblp.org/rdf/schema#Article':
                    journal_id = article["conf_journal_id"]
                    journal = fetch_journal_info(journal_id)
                    journal_article = {
                        article_url: {
                            'title': article["title"],
                            'pages': article["pages"],
                            'year': article["article_pubyear"],
                            'ee': article["ee"],
                            'journal': {
                                'journal_id': journal_id,
                                'title': journal.get("label"),
                                'iso4': journal.get("iso4"),
                                'issn': journal.get("issn")
                            },
                            'publisher': {
                                'name': journal.get("publishedBy")
                            },
                            'authors': fetch_authors(article_url)
                        }
                    }
                    DBLP_dico[person_uri]["proceeding_journal_article"].append(journal_article)

                elif article_type == 'https://dblp.org/rdf/schema#Books':
                    book_info = fetch_book_info(article_url)
                    book_article = {
                        article_url: {
                            'title': book_info.get("label"),
                            'isbn': book_info.get("isbn"),
                            'volume': book_info.get("pagination"),
                            'year': book_info.get("yearOfPublication"),
                            'authors': fetch_authors(article_url),
                            'publisher': {
                                'name': book_info.get("publishedBy")
                            }
                        }
                    }
                    DBLP_dico[person_uri]["book"].append(book_article)

    return DBLP_dico

 #Supprimez les paires clé-valeur dans lesquelles les valeurs sont vides ou les listes/dictionnaires sont vides
def clean_dict(input_dict):
    cleaned_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, dict):
            cleaned_value = clean_dict(value)
            if cleaned_value:  # Check if cleaned_value is not empty
                cleaned_dict[key] = cleaned_value
        elif isinstance(value, list):
            cleaned_value = [clean_dict(item) for item in value if item is not None]
            cleaned_value = [item for item in cleaned_value if item]  # Remove empty items
            if cleaned_value:  # Check if cleaned_value is not empty
                cleaned_dict[key] = cleaned_value
        elif value is not None:
            cleaned_dict[key] = value

    return cleaned_dict

# Fonction pour générer des nœuds
def generate_node(identity, labels, properties, elementId):
    return {
        "n": {
            "identity": identity,
            "labels": labels,
            "properties": properties,
            "elementId": elementId
        }
    }

# Fonction pour générer des relations
def generate_relationship(identity, start, end, rel_type, startNodeElementId, endNodeElementId):
    return {
        "r": {
            "identity": identity,
            "start": start,
            "end": end,
            "type": rel_type,
            "properties": {},
            "startNodeElementId": startNodeElementId,
            "endNodeElementId": endNodeElementId
        }
    }

# Traiter les données, générer des nœuds et des relations
def process_data(data):
    result = []
    stats = {
        'persons': 0,
        'nodes': 0,
        'relationships': 0
    }

    for person_url, person_data in data.items():
        person_id = person_data['elementID']
        person_name = person_data['nom']
        person_identity = f"Person_{person_id}"
        person_elementId = f"4:68e17dce-ea76-4056-93c0-be7230818442:{person_id}"
        
        person_node = generate_node(person_identity, ["Person"], {"elementID": person_id, "name": person_name}, person_elementId)
        result.append(person_node)
        stats['persons'] += 1
        stats['nodes'] += 1
        
        for article_data in person_data['proceeding_journal_article']:
            article_url = list(article_data.keys())[0]
            article = article_data[article_url]
            article_id = article_url.split('/')[-1]
            article_identity = f"Article_{article_id}"
            article_elementId = f"4:68e17dce-ea76-4056-93c0-be7230818442:{article_id}"
            
            article_properties = {k: article[k] for k in article if k not in ['proceedings', 'journal', 'conference', 'authors']}
            
            article_node = generate_node(article_identity, ["Article"], article_properties, article_elementId)
            result.append(article_node)
            stats['nodes'] += 1
            
            wrote_relationship = generate_relationship(f"Wrote_{person_id}_{article_id}", person_identity, article_identity, "WROTE", person_elementId, article_elementId)
            result.append(wrote_relationship)
            stats['relationships'] += 1
            stats['nodes'] += 1

            if 'proceedings' in article:
                proc = article['proceedings']
                proc_id = proc['proceeding_id'].split('/')[-1]
                proc_identity = f"Proceeding_{proc_id}"
                proc_elementId = f"4:68e17dce-ea76-4056-93c0-be7230818442:{proc_id}"
                
                proc_properties = {k: proc[k] for k in proc}
                
                proc_node = generate_node(proc_identity, ["Proceeding"], proc_properties, proc_elementId)
                result.append(proc_node)
                stats['nodes'] += 1
                
                collected_relationship = generate_relationship(f"CollectedIn_{article_id}_{proc_id}", article_identity, proc_identity, "COLLECTED_IN", article_elementId, proc_elementId)
                result.append(collected_relationship)
                stats['relationships'] += 1
                stats['nodes'] += 1
                
                if 'conference' in article:
                    conf = article['conference']
                    for conf_url, conf_data in conf.items():
                        conf_id = conf_url.split('/')[-1]
                        conf_identity = f"Conference_{conf_id}"
                        conf_elementId = f"4:68e17dce-ea76-4056-93c0-be7230818442:{conf_id}"
                        
                        conf_properties = {"title": conf_data['title']['title']}
                        
                        conf_node = generate_node(conf_identity, ["Conference"], conf_properties, conf_elementId)
                        result.append(conf_node)
                        stats['nodes'] += 1
                        
                        part_relationship = generate_relationship(f"PartOf_{proc_id}_{conf_id}", proc_identity, conf_identity, "PART_OF", proc_elementId, conf_elementId)
                        result.append(part_relationship)
                        stats['relationships'] += 1
                        stats['nodes'] += 1
            
            # Traiter les auteurs
            for author in article['authors']:
                author_name = author['label']
                author_id = f"Author_{author_name.replace(' ', '_')}_{article_id}"
                author_elementId = f"4:68e17dce-ea76-4056-93c0-be7230818442:{author_id}"
                
                author_node = generate_node(author_id, ["Person"], {
                    "name": author_name
                }, author_elementId)
                result.append(author_node)
                stats['nodes'] += 1
                
                cooperate_relationship = generate_relationship(f"CooperateWith_{person_id}_{author_id}", person_identity, author_id, "COOPERATE_WITH", person_elementId, author_elementId)
                result.append(cooperate_relationship)
                stats['relationships'] += 1
                stats['nodes'] += 1
    
    return result, stats

# Générer un fichier JSON
def json_generate():
    final_result = []
    final_stats = {
        'persons': 0,
        'nodes': 0,
        'relationships': 0
    }

    result, stats = process_data(cleaned_dict)
    final_result.extend(result)
    final_stats['persons'] += stats['persons']
    final_stats['nodes'] += stats['nodes']
    final_stats['relationships'] += stats['relationships']
    
    # Écrire les résultats dans un fichier JSON

    with open(json_data_input, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)
    
    # Imprimer les informations statistiques
    print(f"Écriture terminée, {final_stats['persons']} personnes，{final_stats['nodes']} Noeds {final_stats['relationships']} relations")

if __name__ == "__main__":
    cleaned_idfile = "noeds_valides/name/of/your/file"# Chercher le fichier cleaned_person_id dans le dossier noeds_valides et le modifier
    csv_file = f"noeds_valides/{cleaned_idfile}"
    json_data_input = f"basic_json/{cleaned_idfile}.json"
    DBLP_dico = main_generate()
    cleaned_dict = clean_dict(DBLP_dico)
    json_generate()
