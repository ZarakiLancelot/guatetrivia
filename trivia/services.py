from trivia import db
from trivia.models import Questions
import requests
import json


class PreguntasService:
    def __init__(self, base_url):
        self.base_url = base_url

    def obtener_preguntas(self):
        preguntas_guardadas = []
        pregunta_id = 1

        while True:
            url_api = f"{self.base_url}{pregunta_id}"
            response = requests.get(url_api)
            print(f"Respuesta {response}")

            if response.status_code == 200:
                preguntas = response.json()
                if 'error' not in preguntas:
                    print(f"Las preguntas son: {preguntas}")
                    preguntas_guardadas.append(preguntas)
                    pregunta_id += 1
                else:
                    print(f"Ya no hay mas preguntas (error)")
                    break
            else:
                print(f"Ya no hay mas preguntas en la API")
                break

        return preguntas_guardadas

    def guardar_en_bd(self, pregunta_data):
        nueva_pregunta = Questions(pregunta=pregunta_data['pregunta'],
                                   opcion_a=pregunta_data['respuestas']['0'],
                                   opcion_b=pregunta_data['respuestas']['1'],
                                   opcion_c=pregunta_data['respuestas']['2'],
                                   correcta=pregunta_data['respuestas']['3'])
        db.session.add(nueva_pregunta)
        db.session.commit()
