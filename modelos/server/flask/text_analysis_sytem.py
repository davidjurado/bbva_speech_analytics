import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk


class _Text_Analysis_System:

    _instance = None
    dict_task = None
    tokenizer = None
    stop_words = None

    def preprocess_text(self, input_text):
        input_text = input_text.lower()
        nltk_tokenizer = nltk.RegexpTokenizer(r"\w+")
        new_words = nltk_tokenizer.tokenize(input_text)
        new_row = [word for word in new_words  if word not in self.stop_words]
        
        final_sentence = " ".join(new_row)
        return final_sentence

    def pad_text(self, input_text):
        sequence = self.tokenizer.texts_to_sequences([input_text])
        
        max_length = 320
        trunc_type='post'
        padding_type='post'

        padded = pad_sequences(sequence, maxlen=max_length, padding=padding_type, truncating=trunc_type)
        return padded

    
    def get_verb(self, input_text):
        line3 = "vacío"

        line = input_text.lower()
        ini = [line.find(a) for a in ['mira','mire','el motivo','quiero','gustaria','quisiera','llamo para','necesito','llamo porque','estuve','ayudar?','lo que pasa']]
        ini_words = [a for a in ini if a!=-1]
        if len(ini_words) != 0:
            line2 = line[min([a for a in ini if a!=-1]):]
            line3 = ''.join(line2.split('.')[0:3])
        else:
            line3 = ''.join(line.split('?')[1:3])
        
        if line3 != "":
            return line3
        else:
            return "vacío"


    def predict_text(self, input_text, input_model, label_map):

        final_sentence = self.preprocess_text(input_text)

        padded =self. pad_text(final_sentence)
        
        result = input_model.predict(padded)
        result = np.array(result[0])
        top_ind = result.argsort()[::-1][:3]
        result_index = np.argmax(result)
        predicted_class = label_map[result_index]
        top_classes = [label_map[i] for i in top_ind]
        top_values = result[top_ind]*100
        response = {top_classes[0]: f"{top_values[0]:.2f}%",
                top_classes[1]: f"{top_values[1]:.2f}%",
                top_classes[2]: f"{top_values[2]:.2f}%"}
        
        return response

    def analyze_text(self, input_text):
        final_response = {}
        for column, (model, labels) in self.dict_task.items():
            result = self.predict_text(input_text, model, labels)
            final_response[column] = result
        final_response["Verbalizacion del cliente"] = self.get_verb(input_text)
        return final_response


def load_tokenizer():
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer

        
def load_stop_words():
    with open('all_stop_words.pickle', 'rb') as handle:
        all_stop_words = pickle.load(handle)
    return all_stop_words


def load_model_data():
    model_prod = tf.keras.models.load_model('model_producto.h5')
    model_int = tf.keras.models.load_model('model_intencion.h5')
    model_mov = tf.keras.models.load_model('model_movimiento.h5')
    model_contx1 = tf.keras.models.load_model('model_contexto_1.h5')
    model_contx2 = tf.keras.models.load_model('model_contexto_2.h5')
    model_detalle = tf.keras.models.load_model('model_detalle.h5')
        
    with open('index_to_label_prod.pickle', 'rb') as handle:
        index_to_label_prod = pickle.load(handle)
    with open('index_to_label_prod.pickle', 'rb') as handle:
        index_to_label_prod = pickle.load(handle)
    with open('index_to_label_int.pickle', 'rb') as handle:
        index_to_label_int = pickle.load(handle)
    with open('index_to_label_mov.pickle', 'rb') as handle:
        index_to_label_mov = pickle.load(handle)
    with open('index_to_label_contx1.pickle', 'rb') as handle:
        index_to_label_contx1 = pickle.load(handle)
    with open('index_to_label_contx2.pickle', 'rb') as handle:
        index_to_label_contx2 = pickle.load(handle)
    with open('index_to_label_detalle.pickle', 'rb') as handle:
        index_to_label_detalle = pickle.load(handle)

    dict_task = {}
    dict_task["Producto"] = (model_prod, index_to_label_prod)
    dict_task["Intención"] = (model_int, index_to_label_int)
    dict_task["Tipo de movimiento"] = (model_mov, index_to_label_mov)
    dict_task["Contexto 1"] = (model_contx1, index_to_label_contx1)
    dict_task["Contexto 2"] = (model_contx2, index_to_label_contx2)
    dict_task["Detalle 1"] = (model_detalle, index_to_label_detalle)
    
    return dict_task

def Text_Analysis_System():

    if _Text_Analysis_System._instance is None:
        _Text_Analysis_System._instance = _Text_Analysis_System()
        _Text_Analysis_System.dict_task = load_model_data()
        _Text_Analysis_System.tokenizer = load_tokenizer()
        _Text_Analysis_System.stop_words = load_stop_words()

    return _Text_Analysis_System._instance

if __name__ == "__main__":
    tas = Text_Analysis_System()
    input_text = "Hola, soy asesor de línea de bebé A Tengo el gusto. Sí, mucho gusto, señorita. Agradecemos su paciencia debido a la contingencia. El número de asesores disponibles reducido. En qué puedo ayudarla? Si mire, lo que pasa es que hace ratito marque. Me dijeron que regresaría la llamada más o menos entre tres y siete de la noche. Por qué? Porque el día de ayer que la reposición de mi tarjeta ese es de la S o la de débito se ahorra. Entonces es que tenía yo en la tarjeta el día de ciento cuarenta y cuatro pesos retenidos hemos sido ocupado para hacer lo del pago porque lo que dicen que en cuanto se hacen depósitos de descuenta lo del pago de la tarjeta correcto. El día de hoy me hicieron donde Pues tío de seiscientos treinta y siete supone que la tarjeta el plástico costaba ciento ochenta. Entonces treinta y siete del depósito veo y los ciento cuarenta y cuatro que tenía que ya con eso completaba hoy Marco para checar mi saldo y me dicen que tengo cuatrocientos noventa y dos. Se supone que tenía que haber quedado seiscientos pesos y quería ver qué es lo que pasó muy bien. Le comento No se activó la tarjeta. El día de hoy me aparece la activación. Bueno, la activación aparece hasta el día de hoy, nueve de septiembre del dos mil veinte. Bueno, ya me entregaron el plato y me dijeron que fuera el casero hacerlo de la activación. Correcto. Muy bien. El día de hoy recibe un abono por seiscientos treinta y siete pesos. Correcto. La tarjeta literalmente estaba en ceros. El día de hoy recibe una buena por seiscientos treinta y siete pesos. Pero si alguien revisa la tarjeta y estaba en silencio ahí, en ciento cuarenta y cuatro, pero estaba el número negativo, es decir, al momento de activarla, se genera el pago, el cobro y el cobro se genera, pero en saldo negativo. Es decir, usted activa la tarjeta y en ese mismo instante, sistema le carga el monto de ciento cuarenta y cuatro presos con sesenta y tres centavos. Saldo negativo que se estaría cobrando el cobro de la tarjeta, que son ciento cuarenta y cinco pesos. Se manejan los ciento cuarenta y cuatro pesos con sesenta y tres centavos aquí. Al parecer, usted tenía un saldo disponible de cero seis centavos. Entonces el cero seis centavos se cobran estos ciento cuarenta y cuatro pesos, con sesenta y tres centavos se quedan en saldo negativo. Porque porque la tarjeta está literalmente en cero. Al momento de que usted le deposita la cantidad de seiscientos treinta y siete pesos, se toman los ciento cuarenta y cuatro punto sesenta y tres para cubrir el cargo del la reposición de tarjeta y usted se queda un saldo con cuatrocientos, noventa y dos pesos con treinta y siete centavos. Muy probablemente usted pensó que tenía los ciento cuarenta y cuatro pesos con sesenta y tres centavos a favor, pero no sé, ya los tenía en saldo negativo porque su cuenta estaba en cero. Es lo que yo tenía duda. Pues sí, era lo que yo tenía ahí de saldo de que ya tiene tiempo de la tarjeta o eran por lo ahora, por lo que se cobraba. Correcto, Es usted. Es decir, usted no tenía ni un solo centavo en bueno, tenía la Navidad de seis centavos en la cuenta, por lo cual pues únicamente le realizan el cargo de cuatro ciento cuarenta y cuatro pesos, con sesenta y tres centavos, ya que el cargo original es de ciento cuarenta y cinco pesos. En este caso se queda el restante. Por los centavos que se toman se queda el mensaje de ciento cuarenta y cuatro pesos, con sesenta y tres centavos de los cuales, como aparecen en saldo negativo, le tuvieron que tuvo que haber aparecido el signo de negativo de menos la pobreza. Saldo negativo. Entonces, al momento de que usted le deposita en la cantidad de seiscientos treinta y siete pesos, pues ese saldo se convierte en positivo, se cobra. Y usted se le descuenta la cantidad de ciento treinta y siete y se queda con el disponible de cuatrocientos noventa y dos punto treinta y siete. Ah, bueno, si es que yo tenía la duda de que bueno, se supone que alguien ciento cuarenta y cuatro. Ciento cuarenta y cuatro. Entonces, qué pasó? Ajá. Pero no está bien si nomas quería quitarme la verdad correcto, señorita, alguna otra información que puede apoyarla? Tendría que ir a tendría que ir al banco si quisiera que me lleguen las notificaciones de mi celular, del, de la de los depósitos. Muy bien, vamos a validar la información. No tiene usted activada la aplicación? Es que que creo que mi celular no me agarra la aplicación. Muy bien. En este caso, necesitaríamos que para que le lleguen las notificaciones o las alertas inicialmente, tener la aplicación móvil para que a partir de ahí se activó en las alertas y le lleguen todas las notificaciones respecto algún cargo, algún cobro, alguna compra por pensar que normal no llegarían. Podría ser con las alertas, señorita. Pero en este caso tendría que ser y activarlas directamente en sucursal. Bueno, sería todo entonces. Por último, su opinión es muy importante para nosotros. En las próximas horas en veremos a su correo electrónico una breve encuesta para calificar el servicio proporcionado en esta llamada. Sus comentando que ayudan a mejorar la atención en cada contacto. Puedo contar con usted, señorita? Bueno, y para poder a nombre de encuesta. Se lo agradecería bastante. Reitero mi nombre es Ismael. Asesor de línea de de uve A. Pase una excelente tarde. Igualmente. Gracias. Hasta luego."
    result = tas.analyze_text(input_text)
    print("RESULTADO:\n")
    print(result)