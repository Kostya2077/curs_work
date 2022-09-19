from os.path import abspath, dirname
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Accept": "text/html"
}
response = requests.request("GET", url='https://planetazdorovo.ru/catalog/lekarstva-i-bad/prostuda-i-gripp/protivovirusnye-immunokorrektory/arbidol-protivovirusnoe-ot-gri-23565203/',
                            cookies={"qrator_jsid": "1663591154.256.U4IDdLhLAIupKxIx-aod0vmtu2ej5h4jgkthmkrlh22rls5q2"}
                            )
a=1

