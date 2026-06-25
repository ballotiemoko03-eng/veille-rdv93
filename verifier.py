import os
import requests

URL = ("https://rdv.anct.gouv.fr/prendre_rdv?departement="
       "&motif_name_with_location_type=renouvellement_de_recepisses_arrives_a_echeance_-public_office"
       "&public_link_organisation_id=2458")

# Phrase affichée quand il n'y a AUCUN créneau.
# Si elle disparaît, c'est qu'un créneau est probablement apparu.
PHRASE_AUCUN_CRENEAU = "zzzphrasebidonzzz"

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def envoyer_telegram(texte):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api, data={"chat_id": CHAT_ID, "text": texte}, timeout=30)

def verifier():
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/149.0.0.0 Safari/537.36"),
        "Accept-Language": "fr-FR,fr;q=0.9",
    }
    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()
    page = r.text.lower()

    if PHRASE_AUCUN_CRENEAU in page:
        print("Aucun créneau pour le moment.")
    else:
        message = ("🟢 Un créneau RDV récépissé semble DISPONIBLE !\n\n"
                   "Va vite réserver ici :\n" + URL)
        envoyer_telegram(message)
        print("Créneau potentiel détecté → notification envoyée.")

if __name__ == "__main__":
    verifier()
