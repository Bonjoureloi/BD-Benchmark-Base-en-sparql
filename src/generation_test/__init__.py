# Importing specific functions from modules
from .dataset_to_csv import (
    load_dblp_community,
    save_graph_to_csv
)

from .cleaned_person_id import (
    format_person_id,
    person_uri_id,
    sparql_query,
    query_author_name,
    id_valide,
)

from .data_generate import (
    format_person_id,
    person_uri_id,
    sparql_query,
    query_author_name,
    fetch_author_articles,
    fetch_inproceedings_info,
    fetch_journal_info,
    fetch_book_info,
    fetch_conference_info,
    query_author_name_from_uri,
    fetch_authors,
    fetch_editors,
    read_person_ids_from_csv,
    main_generate,
    clean_dict,
    generate_node,
    generate_relationship,
    process_data,
    json_generate
)

from .neo4j import (
    log,
    random_string,
    apply_modifications,
    main
)

# Defining package-level variables
package_name = "BD_Dev_Benchmark"