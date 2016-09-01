############################################################################################################
# Per impostare le configurazioni di default, è necessario clonare i file .template
# ed eliminare l'estensione .template, lasciando solo l'estensione .xml
#
# Configurare poi i parametri secondo i valori corretti per l'installazione.
# I file sono  il default_config.xml.template e il default_installer_config.xml.template.
# Di seguito vengono descritti.
############################################################################################################

*****************
*Default Config *
*****************

Questo file contiene i parametri di configurazione necessari a una corretta inizializzazione del sistema.
Alcuni dei paramentri sono indispensabili per il corretto funzionamento del sistema,
altri sono utili a preimpostare i valori del formo di configurazione.

Per differenziare i due casi nel seguito verranno usate due sigle:
M (mandatory) - nel caso di parametri indispensabili;
NM (not mandatory) - nel caso di parametri non indispensabili ma d'ausilio alla preconfigurazione dei campi (sono Parametri che possono essere
inseriti dall'interfaccia web di configurazione).

BrainsConfiguration : Racchiude l'intero blocco di configurazione e ha un attributo "enabled" per definire se
la configurazione va usata o meno, lasciare sempre 1 se non si è sicuri del valore da utilizzare

Drupal : sezione contenente le configurazioni relativa all'integrazione con Drupal

drupal_url (NM) : Url dell'installazioen Drupal (es: http://brains.flosslab.com/drupal)
drupal_admin_username (NM): Username dell'utente amministratore di Drupal(es: admin)
drupal_admin_password (NM): Password dell'utente amministratore di Drupal(es: admin)
drupal_api_login_path (NM): URI del Servizio REST per il login (es: restservice/login/user/login)
drupal_url_login_csv_path (NM): URI del File CSV con Utenti Drupal necessari al servizio di login (es: urllogin/userlist.csv)
drupal_workbench_path (NM): admin/workbench</drupal_workbench_path>
drupal_rest_endpoint_path (NM): restservice</drupal_rest_endpoint_path>
drupal_rest_node_alias (NM): Alias utilizzato su Drupal per i servizi legati ai nodi (es : node)
drupal_rest_user_alias (NM): Alias utilizzato su Drupal per i servizi legati agli utenti (es : user)

DrupalInstallationConf : sottosezione della configurazione Drupal contenente i parametri di collegamento al db di Drupal
drupal_mysql_host (M) : Hostname del database server ospitante il db (es : 127.0.0.1)
drupal_mysql_port (M) : Porta del database server ospitante il db (es : 3306)
drupal_mysql_user (M) : User del database server ospitante il db (es : root)
drupal_mysql_password (M) : Password del database server ospitante il db Drupal(es : admin)
drupal_mysql_dbname (M) : Nome del database Drupal(es : brains_eip_basic)
drupal_site_path (M) : Percorso sul filesystem del site default(es : /home/antonio/git/Flosslab2.0/brains_eip/sites/default)


Alfresco : sezione contenente le configurazioni relativa all'integrazione con Alfresco

alfresco_host (NM): (es : localhost)
alfresco_port (NM): (es : 8080)
alfresco_username (NM): (es : admin)
alfresco_password (NM): (es : fl055l!&amp; - da notare il carattere di escape per i caratteri speciali, essendo il file di conf un xml)
alfresco_root (NM): (es : OpenErpSpace)
alfresco_base_service_url (NM): (es : /alfresco/s/)
alfresco_site_name (NM): (es : brains)

AlfrescoInstallationConf : sottosezione della configurazione Alfresco contenente i parametri delle posizioni di alcuni file di sistema
alfresco_software_root (M) : Path della posizione dei war per Alfresco, il numero di versione viene inserito dalla procedura (es: /home/antonio/Alfresco5/Drive_Alfresco/alfresco-)
tomcat_root (M) :            Path della root di tomcat (es : /home/antonio/Alfresco5/alfresco-5.0.d/tomcat)
temp_working_dir (M) :       Path della directory temporanea nella quale verranno eseguite le operazioni per configurare i parametri
                            interni ai file interni ai jar (es :/tmp/work_alfresco_drive)

GoogleOauth: sezione contenente le configurazioni relativa all'integrazione con l'Autenticazioen di Google
google_oauth_odoo_client_id (NM): Client Id fornito dala google console in relazione a un app per goauth su odoo(es:731681660121-lrh1ktt1avj81s5pd0g8fkkhboe3neh4.apps.googleusercontent.com)
google_oauth_alfresco_client_id (NM): Client Id fornito dala google console in relazione a un app per goauth su alfresco(es:290112530364-5iu2e1jne7s3og25f2l595g8ukuuebdr.apps.googleusercontent.com)
google_oauth_alfresco_client_secret (NM): Client Secret fornito dala google console in relazione a un app per goauth su alfresco(es:N2YUcW6xpUxjwlFveZ5IU6kM)
google_drive_alfresco_client_id (NM): Client Id fornito dala google console in relazione a un app per drive su alfresco(es:290112530364-5iu2e1jne7s3og25f2l595g8ukuuebdr.apps.googleusercontent.com)
google_drive_alfresco_client_secret (NM): Client Secret fornito dala google console in relazione a un app per drive su alfresco(es:N2YUcW6xpUxjwlFveZ5IU6kM)
google_oauth_drupal_client_id (NM):Client Id fornito dala google console in relazione a un app per goauth su drupal(es: 565933281273-leo852ve46bj7iosagv2pkgeg74pftnh.apps.googleusercontent.com)
google_oauth_drupal_client_secret (NM): Client Secret fornito dala google console in relazione a un app per goauth su drupal(es:OJC2jFDU9R4Y3TdAf1-YBpY5)
google_oauth_drupal_api_key (NM): API KEY fornito dala google console in relazione a un app per goauth su drupal(es:AIzaSyDFvoeoU_60Nl0smC1z22NScT-5aDlbvNk)
google_oauth_mobileapp_client_id (NM): Client Id fornito dala google console in relazione a un app per goauth su mobile(es: 986754345436-1ihamfe1vo5n8ipd5c92nhpjp24o3j21.apps.googleusercontent.com)
google_oauth_mobileapp_client_secret (NM): Client Secret fornito dala google console in relazione a un app per goauth su mobile(es:03uhZq8SHl1MhyiWt7K_wbUk)


############################################################################################################

***************************
*Default Installer Config *
***************************

Questo file contiene i parametri di configurazione necessari a una corretta comunicazione con il sistema installer.

host : è il nome dell'host del server installatore (es: localhost)
port : è il nome della porta del server installatore (es: 58069)
db_name : è il nome del database con i dati dell'installatore