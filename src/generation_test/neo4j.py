import os
import random
import string
import json
from datetime import datetime, timedelta

# Définir la fonction d'enregistrement des journaux
def log(message, level="INFO"):
    print(f"{level}: {message}")

# Définir la fonction de génération de chaînes aléatoires
def random_string(min_length=3, max_length=10):
    letters = string.ascii_letters
    length = random.randint(min_length, max_length)
    random_str = ''.join(random.choice(letters) for _ in range(length))
    return random_str.upper() if random.choice([True, False]) else random_str.capitalize()

# Définir la fonction d'application des modifications
def apply_modifications(data, selected_modifications, modification_percentage):
    total_modifications = int(len(data) * modification_percentage / 100)
    log(f"Total des modifications à appliquer : {total_modifications}")

    for _ in range(total_modifications):
        modification = random.choice(selected_modifications)
        log(f"Application de la modification : {modification}")

        try:
            if modification == "add_publisher":
                name = random_string()
                publisher_id = random_string()
                data.append({"n": {"identity": publisher_id, "labels": ["Publisher"], "properties": {"name": name}}})
            elif modification == "add_establishment_node":
                name = random_string()
                node_id = random_string()
                data.append({"n": {"identity": node_id, "labels": ["Establishment"], "properties": {"name": name}}})
            elif modification == "delete_collaboration":
                collab_rels = [item for item in data if 'r' in item and item['r']['type'] == "COLLABORER"]
                if collab_rels:
                    rel = random.choice(collab_rels)
                    data.remove(rel)
            elif modification == "delete_supervised":
                supervised_rels = [item for item in data if 'r' in item and item['r']['type'] == "SUPERVISED"]
                if supervised_rels:
                    rel = random.choice(supervised_rels)
                    data.remove(rel)
            elif modification == "merge_conference":
                name = random_string()
                conference_id = random_string()
                data.append({"n": {"identity": conference_id, "labels": ["Conference"], "properties": {"name": name}}})
                person_nodes = [item['n'] for item in data if 'n' in item and "Person" in item['n']["labels"]]
                for _ in range(random.randint(1, 5)):
                    if person_nodes:
                        person_node = random.choice(person_nodes)
                        data.append({"r": {"identity": random_string(), "start": person_node["identity"], "type": "ATTENDED", "end": conference_id, "properties": {}}})
            elif modification == "add_workshop":
                name = random_string()
                data.append({"n": {"identity": random_string(), "labels": ["Workshop"], "properties": {"name": name}}})
            elif modification == "add_citation":
                article_nodes = [item for item in data if 'm' in item and "Article" in item['m']["labels"]]
                if article_nodes:
                    article_node = random.choice(article_nodes)
                    article_node['m']['properties']['citations'] = article_node['m']['properties'].get('citations', 0) + 1
            elif modification == "add_doi":
                article_nodes = [item for item in data if 'm' in item and "Article" in item['m']["labels"]]
                if article_nodes:
                    article_node = random.choice(article_nodes)
                    article_node['m']['properties']['DOI'] = f"10.1234/{random_string(8)}"
            elif modification == "add_author_tag":
                wrote_rels = [item for item in data if 'r' in item and item['r']['type'] == "WROTE"]
                if wrote_rels:
                    rel = random.choice(wrote_rels)
                    start_node_id = rel['r']['start']
                    for node_item in data:
                        if 'n' in node_item and node_item['n']['identity'] == start_node_id:
                            if "Author" not in node_item["n"]["labels"]:
                                node_item["n"]["labels"].append("Author")
            elif modification == "add_editor_tag":
                edited_rels = [item for item in data if 'r' in item and item['r']['type'] == "EDITED"]
                if edited_rels:
                    rel = random.choice(edited_rels)
                    start_node_id = rel['r']['start']
                    for node_item in data:
                        if 'n' in node_item and node_item['n']['identity'] == start_node_id:
                            if "Editor" not in node_item["n"]["labels"]:
                                node_item["n"]["labels"].append("Editor")
            elif modification == "add_mdate":
                article_nodes = [item for item in data if 'm' in item and "Article" in item['m']["labels"]]
                if article_nodes:
                    article_node = random.choice(article_nodes)
                    article_node['m']['properties']['mdate'] = str(datetime.now().date())
            elif modification == "add_citation_count":
                article_nodes = [item for item in data if 'm' in item and "Article" in item['m']["labels"]]
                if article_nodes:
                    article_node = random.choice(article_nodes)
                    article_node['m']['properties']['citationCount'] = article_node['m']['properties'].get('citationCount', 0) + 1
            elif modification == "change_author_name":
                person_nodes = [item for item in data if 'n' in item and "Person" in item['n']["labels"]]
                if person_nodes:
                    person_node = random.choice(person_nodes)
                    if 'properties' in person_node:
                        person_node['n']['properties']['name'] = random_string()
                    else:
                        log(f"Modification de change_author_name ignorée, 'properties' non trouvé dans {person_node}", level="ERROR")
            elif modification == "limit_keywords":
                article_nodes = [item for item in data if 'm' in item and "Article" in item['m']["labels"]]
                if article_nodes:
                    article_node = random.choice(article_nodes)
                    if 'keywords' in article_node['m']['properties']:
                        article_node['m']['properties']['keywords'] = article_node['m']['properties']['keywords'][:5]
            elif modification == "change_establishment":
                person_nodes = [item for item in data if 'n' in item and "Person" in item['n']["labels"]]
                if person_nodes:
                    person_node = random.choice(person_nodes)
                    if 'properties' in person_node:
                        person_node['n']['properties']['establishment'] = random_string()
                    else:
                        log(f"Modification de change_establishment ignorée, 'properties' non trouvé dans {person_node}", level="ERROR")
        except KeyError as e:
            log(f"KeyError lors de la modification {modification}: {e}", level="ERROR")
        except Exception as e:
            log(f"Exception lors de la modification {modification}: {e}", level="ERROR")

    return data

# Logique principale du programme
def main():
    base_path = r"json_genere"
    json_file_path = r"../preparation_json/basic_json/your_json_file_name.json"

    modifications = [
        "add_publisher", "add_establishment_node", "delete_collaboration",
        "delete_supervised", "merge_conference", "add_workshop", "add_citation",
        "add_doi", "add_author_tag", "add_editor_tag", "add_mdate", "add_citation_count",
        "change_author_name", "limit_keywords", "change_establishment"
    ]

    if not os.path.exists(json_file_path):
        log(f"Erreur : Le fichier {json_file_path} n'existe pas.", level="ERROR")
        return

    try:
        with open(json_file_path, 'r', encoding='utf-8-sig') as f:
            initial_data = json.load(f)
    except Exception as e:
        log(f"Erreur lors de la lecture du fichier {json_file_path}: {e}", level="ERROR")
        return

    base_data_point_count = len(initial_data)
    log(f"Nombre de points de données de base : {base_data_point_count}")

    try:
        modification_percentage = float(input("Entrez le pourcentage de points de données à modifier (0-100) : "))
        if modification_percentage < 0 or modification_percentage > 100:
            log("Erreur : Le pourcentage doit être entre 0 et 100.", level="ERROR")
            return

        random_or_specific = input("Voulez-vous choisir un nombre aléatoire de types de modification ou spécifier le nombre ? (aléatoire/spécifique) : ").strip().lower()

        if random_or_specific == "spécifique":
            num_modification_types = int(input("Entrez le nombre de types de modification à appliquer (1-14) : "))
            if num_modification_types < 1 or num_modification_types > 14:
                log("Erreur : Le nombre de types de modification doit être entre 1 et 14.", level="ERROR")
                return
        else:
            num_modification_types = random.randint(1, 14)

        num_files = int(input("Entrez le nombre de fichiers à générer : "))
        if

 num_files < 1:
            log("Erreur : Le nombre de fichiers doit être supérieur à 0.", level="ERROR")
            return

        selected_modifications = random.sample(modifications, num_modification_types)
        log(f"Modifications sélectionnées : {selected_modifications}")

        start_year = 2021
        current_date = datetime(start_year, 1, 1)

        for file_count in range(num_files):
            log(f"Modification des données pour le {current_date.strftime('%Y-%m-%d')}")
            folder_path = os.path.join(base_path, f"{current_date.year}/{current_date.month:02d}/{current_date.day:02d}")
            os.makedirs(folder_path, exist_ok=True)
            log(f"Dossier créé : {folder_path}")

            modified_data = apply_modifications(initial_data[:], selected_modifications, modification_percentage)
            log(f"Données après modifications (affichage de jusqu'à 5 enregistrements) : {json.dumps(modified_data[:5], indent=2)}")

            try:
                with open(os.path.join(folder_path, "data.json"), "w", encoding='utf-8') as f:
                    json.dump(modified_data, f, indent=4)
                log(f"Fichier exporté avec succès : {os.path.join(folder_path, 'data.json')}")
            except Exception as e:
                log(f"Erreur lors de l'exportation du fichier : {e}", level="ERROR")

            current_date += timedelta(days=1)

    except Exception as e:
        log(f"Erreur : {e}", level="ERROR")

if __name__ == "__main__":
    main()
